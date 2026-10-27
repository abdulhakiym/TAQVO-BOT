import os
import json
import hmac
import hashlib
import time
import sqlite3
import urllib.parse

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CHANNEL = os.getenv("TELEGRAM_CHANNEL", "@hakiymqalb")
DATABASE_PATH = os.getenv("DATABASE_PATH", "taqvo.db")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

app = FastAPI(title="TAQVO PRO MAX API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    con = sqlite3.connect(DATABASE_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with get_db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                telegram_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                score INTEGER NOT NULL DEFAULT 0,
                updated_at INTEGER NOT NULL
            )
        """)
        con.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id TEXT PRIMARY KEY,
                name TEXT,
                subscribed INTEGER NOT NULL DEFAULT 0,
                updated_at INTEGER NOT NULL
            )
        """)


init_db()


def validate_init_data(raw: str) -> dict:
    if not BOT_TOKEN or not raw:
        raise HTTPException(
            status_code=401,
            detail="Telegram initData yoki BOT_TOKEN sozlanmagan."
        )

    try:
        values = dict(
            urllib.parse.parse_qsl(raw, keep_blank_values=True)
        )

        received_hash = values.pop("hash", None)
        auth_date = int(values.get("auth_date", "0"))

        if not received_hash:
            raise ValueError("hash missing")

        if time.time() - auth_date > 86400 or auth_date > time.time() + 60:
            raise ValueError("initData expired")

        check_string = "\n".join(
            f"{key}={value}"
            for key, value in sorted(values.items())
        )

        secret_key = hmac.new(
            b"WebAppData",
            BOT_TOKEN.encode(),
            hashlib.sha256
        ).digest()

        calculated_hash = hmac.new(
            secret_key,
            check_string.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(calculated_hash, received_hash):
            raise ValueError("hash mismatch")

        user = json.loads(values["user"])

        if not user.get("id"):
            raise ValueError("user missing")

        return user

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Telegram ma’lumotlarini tekshirish muvaffaqiyatsiz."
        )


async def is_subscribed(user_id: int) -> bool:
    if not BOT_TOKEN:
        raise HTTPException(
            status_code=503,
            detail="Render sozlamalarida BOT_TOKEN yo‘q."
        )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                url,
                params={
                    "chat_id": CHANNEL,
                    "user_id": user_id
                }
            )

        data = response.json()

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="Telegram serveriga ulanib bo‘lmadi."
        )

    if response.status_code != 200 or not data.get("ok"):
        return False

    status = data.get("result", {}).get("status")

    return status in {
        "creator",
        "administrator",
        "member",
        "restricted"
    }


class InitDataInput(BaseModel):
    init_data: str = ""


class ScoreInput(BaseModel):
    init_data: str = ""
    name: str = "Foydalanuvchi"
    score: int = Field(ge=0, le=100000)


class AskInput(BaseModel):
    init_data: str = ""
    question: str = Field(min_length=1, max_length=4000)


@app.get("/")
def home():
    return {
        "ok": True,
        "service": "TAQVO PRO MAX API"
    }


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/api/subscription")
async def check_subscription(payload: InitDataInput):
    user = validate_init_data(payload.init_data)
    subscribed = await is_subscribed(int(user["id"]))

    with get_db() as con:
        con.execute("""
            INSERT INTO users
                (telegram_id, name, subscribed, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                name = excluded.name,
                subscribed = excluded.subscribed,
                updated_at = excluded.updated_at
        """, (
            str(user["id"]),
            user.get("first_name", "Foydalanuvchi"),
            int(subscribed),
            int(time.time())
        ))

    return {"subscribed": subscribed}


@app.post("/api/score")
async def save_score(payload: ScoreInput):
    user = validate_init_data(payload.init_data)
    user_id = int(user["id"])

    if not await is_subscribed(user_id):
        raise HTTPException(
            status_code=403,
            detail="@hakiymqalb kanaliga obuna bo‘ling."
        )

    name = (
        user.get("first_name")
        or payload.name
        or "Foydalanuvchi"
    )[:64]

    with get_db() as con:
        con.execute("""
            INSERT INTO scores
                (telegram_id, name, score, updated_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                name = excluded.name,
                score = MAX(scores.score, excluded.score),
                updated_at = excluded.updated_at
        """, (
            str(user_id),
            name,
            payload.score,
            int(time.time())
        ))

    return {"ok": True}


@app.get("/api/ranking")
def get_ranking():
    with get_db() as con:
        rows = con.execute("""
            SELECT name, score
            FROM scores
            ORDER BY score DESC, updated_at ASC
            LIMIT 100
        """).fetchall()

    return {"items": [dict(row) for row in rows]}


@app.post("/api/ask")
async def ask_ai(payload: AskInput):
    user = validate_init_data(payload.init_data)

    if not await is_subscribed(int(user["id"])):
        raise HTTPException(
            status_code=403,
            detail="@hakiymqalb kanaliga obuna bo‘ling."
        )

    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Render’da OPENAI_API_KEY sozlanmagan."
        )

    body = {
        "model": OPENAI_MODEL,
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Siz TAQVO AI, Islomiy savollarga ehtiyotkor "
                    "javob beruvchi yordamchisiz. Qur’on oyati yoki "
                    "hadis manbasini to‘qib chiqarmang. Manbani "
                    "aniq bilmasangiz, buni ayting. Fiqhiy masalalarda "
                    "mazhablar o‘rtasidagi farqlarni hisobga oling. "
                    "O‘zingizni mufti deb tanishtirmang. "
                    "O‘zbek tilida javob bering."
                )
            },
            {
                "role": "user",
                "content": payload.question.strip()
            }
        ]
    }

    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=body
            )

        if response.status_code >= 400:
            raise HTTPException(
                status_code=502,
                detail="AI provayderida xatolik. Kalit va limitni tekshiring."
            )

        data = response.json()
        answer = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
        )

        return {"answer": answer or "Javob olinmadi."}

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="AI xizmatiga ulanib bo‘lmadi."
        )