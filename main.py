
import os
import json
import hmac
import hashlib
import asyncio
import sqlite3
import time
from urllib.parse import parse_qsl
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CHANNEL = os.getenv("CHANNEL_USERNAME", "@hakiymqalb").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()
DATABASE = os.getenv("DATABASE_PATH", "taqvo.db")

bot = Bot(BOT_TOKEN) if BOT_TOKEN else None
dp = Dispatcher()
polling_task = None


def db():
    con = sqlite3.connect(DATABASE, timeout=20)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with db() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS users (
          telegram_id INTEGER PRIMARY KEY,
          display_name TEXT NOT NULL DEFAULT 'Foydalanuvchi',
          points INTEGER NOT NULL DEFAULT 0,
          activity_count INTEGER NOT NULL DEFAULT 0,
          last_active INTEGER NOT NULL DEFAULT 0,
          reminders_enabled INTEGER NOT NULL DEFAULT 1,
          created_at INTEGER NOT NULL
        )
        """)
        con.execute("""
        CREATE TABLE IF NOT EXISTS activity (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          telegram_id INTEGER NOT NULL,
          activity_type TEXT NOT NULL,
          created_at INTEGER NOT NULL
        )
        """)
        con.execute("""
        CREATE TABLE IF NOT EXISTS quiz_sessions (
          session_id TEXT PRIMARY KEY,
          telegram_id INTEGER NOT NULL,
          answered INTEGER NOT NULL DEFAULT 0,
          score INTEGER NOT NULL DEFAULT 0,
          completed INTEGER NOT NULL DEFAULT 0,
          created_at INTEGER NOT NULL
        )
        """)


def verify_webapp_data(init_data: str):
    if not BOT_TOKEN or not init_data:
        raise HTTPException(status_code=401, detail="Telegram Mini App orqali kiring.")

    values = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = values.pop("hash", None)
    if not received_hash:
        raise HTTPException(status_code=401, detail="Telegram tasdiqlash ma’lumoti yo‘q.")

    auth_date = int(values.get("auth_date", "0") or "0")
    if auth_date < int(time.time()) - 86400 or auth_date > int(time.time()) + 60:
        raise HTTPException(status_code=401, detail="Kirish ma’lumoti eskirgan. Mini App’ni qayta oching.")

    data_check = "\n".join(f"{k}={v}" for k, v in sorted(values.items()))
    secret = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    calculated = hmac.new(secret, data_check.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculated, received_hash):
        raise HTTPException(status_code=401, detail="Telegram tasdiqlashi muvaffaqiyatsiz.")

    try:
        user = json.loads(values["user"])
        telegram_id = int(user["id"])
    except (KeyError, ValueError, TypeError, json.JSONDecodeError):
        raise HTTPException(status_code=401, detail="Telegram foydalanuvchisi aniqlanmadi.")

    return user, telegram_id


async def require_subscriber(init_data: str):
    user, telegram_id = verify_webapp_data(init_data)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot tokeni serverda sozlanmagan.")

    try:
        member = await bot.get_chat_member(CHANNEL, telegram_id)
        if member.status in ("left", "kicked"):
            raise HTTPException(status_code=403, detail="Davom etish uchun @hakiymqalb kanaliga obuna bo‘ling.")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=503, detail="Kanal obunasini tekshirib bo‘lmadi. Keyinroq urinib ko‘ring.")

    name = user.get("first_name") or "Foydalanuvchi"
    with db() as con:
        con.execute("""
        INSERT INTO users(telegram_id, display_name, created_at, last_active)
        VALUES(?,?,?,?)
        ON CONFLICT(telegram_id) DO UPDATE SET
          display_name=excluded.display_name,
          last_active=excluded.last_active
        """, (telegram_id, name, int(time.time()), int(time.time())))

    return user, telegram_id


@dp.message(CommandStart())
async def start_handler(message: Message):
    name = message.from_user.first_name if message.from_user else "do‘stim"
    await message.answer(
        f"Assalomu alaykum va rohmatulloh, {name}! 🌿\n\n"
        "TAQVO PRO MAX’ga xush kelibsiz.\n"
        f"Avval {CHANNEL} kanaliga obuna bo‘ling, so‘ng Mini App menyusidan foydalaning.\n\n"
        "Kanal: https://t.me/hakiymqalb"
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    global polling_task
    init_db()
    if bot:
        try:
            info = await bot.get_webhook_info()
            if not info.url:
                polling_task = asyncio.create_task(dp.start_polling(bot))
        except Exception as exc:
            print("Telegram polling ishga tushmadi:", str(exc))
    yield
    if polling_task:
        polling_task.cancel()
        try:
            await polling_task
        except asyncio.CancelledError:
            pass
    if bot:
        await bot.session.close()


app = FastAPI(title="TAQVO PRO MAX API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://abdulhakiym.github.io",
        "https://taqvo-bot-api.onrender.com",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=3000)
    init_data: str = Field(min_length=1)


class ActivityRequest(BaseModel):
    init_data: str = Field(min_length=1)
    activity_type: str = Field(pattern="^(quran|dhikr|quiz_correct|quiz_complete)$")


@app.get("/")
async def home():
    return {
        "name": "TAQVO PRO MAX API",
        "status": "running",
        "channel": CHANNEL,
        "database": "SQLite",
        "ai_configured": bool(OPENAI_API_KEY),
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/me")
async def me(init_data: str):
    user, telegram_id = await require_subscriber(init_data)
    with db() as con:
        row = con.execute(
            "SELECT points, activity_count, reminders_enabled FROM users WHERE telegram_id=?",
            (telegram_id,),
        ).fetchone()
    return {
        "id": telegram_id,
        "name": user.get("first_name", "Foydalanuvchi"),
        "points": row["points"],
        "activity_count": row["activity_count"],
        "reminders_enabled": bool(row["reminders_enabled"]),
    }


@app.post("/api/ask")
async def ask(req: AskRequest):
    await require_subscriber(req.init_data)
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=503, detail="AI xizmati sozlanmagan: OPENAI_API_KEY kerak.")

    system_prompt = """
Siz TAQVO AI nomli islomiy ma'lumot yordamchisisiz, shayx yoki mufti emassiz.
Javobni o'zbek tilida bering. Qur'on oyatlari va hadis manbalarini aniq bilsangizgina keltiring.
Manba, hadis raqami yoki hukmni uydirmang. To'rt mazhab — Hanafiy, Molikiy,
Shofi'iy va Hanbaliy — qarashlari farq qilsa, farqlarni ajrating va ishonchsizlikni
ochiq ayting. Murakkab fatvo yoki shaxsiy holatda malakali olimga murojaat qilishni tavsiya qiling.
"""
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                json={
                    "model": OPENAI_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": req.question},
                    ],
                    "temperature": 0.2,
                },
            )
        if response.status_code >= 400:
            raise HTTPException(status_code=502, detail="AI provayderidan javob olinmadi.")
        data = response.json()
        answer = data["choices"][0]["message"]["content"]
        return {"answer": answer, "disclaimer": "TAQVO AI — AI yordamchi, malakali olim o‘rnini bosmaydi."}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=502, detail="AI xizmatiga ulanishda xato yuz berdi.")


@app.post("/api/activity")
async def activity(req: ActivityRequest):
    _, telegram_id = await require_subscriber(req.init_data)
    now = int(time.time())
    points = {"quran": 1, "dhikr": 1, "quiz_correct": 20, "quiz_complete": 0}[req.activity_type]

    with db() as con:
        # Takroriy bosishlardan ball yig‘ishni cheklash: bir xil tur uchun
        # eng ko‘pi bilan bitta qayd 30 soniyada.
        last = con.execute(
            "SELECT created_at FROM activity WHERE telegram_id=? AND activity_type=? ORDER BY id DESC LIMIT 1",
            (telegram_id, req.activity_type),
        ).fetchone()
        if last and now - last["created_at"] < 30:
            return {"ok": True, "awarded": 0, "message": "Bu amal yaqinda qayd etilgan."}

        con.execute(
            "INSERT INTO activity(telegram_id, activity_type, created_at) VALUES(?,?,?)",
            (telegram_id, req.activity_type, now),
        )
        con.execute(
            "UPDATE users SET points=points+?, activity_count=activity_count+1, last_active=? WHERE telegram_id=?",
            (points, now, telegram_id),
        )
    return {"ok": True, "awarded": points}


@app.get("/api/ranking")
async def ranking(init_data: str):
    _, telegram_id = await require_subscriber(init_data)
    with db() as con:
        top = con.execute(
            "SELECT telegram_id, display_name, points FROM users ORDER BY points DESC, last_active DESC LIMIT 20"
        ).fetchall()
        own = con.execute(
            "SELECT COUNT(*)+1 AS rank FROM users WHERE points > (SELECT points FROM users WHERE telegram_id=?)",
            (telegram_id,),
        ).fetchone()
    return {
        "top": [{"name": r["display_name"], "points": r["points"]} for r in top],
        "my_rank": own["rank"] if own else None,
    }


@app.get("/api/prayer-times")
async def prayer_times(city: str):
    if not city.strip():
        raise HTTPException(status_code=400, detail="Shahar nomi kerak.")
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.get(
                "https://api.aladhan.com/v1/timingsByCity",
                params={"city": city, "country": "", "method": 3},
            )
        response.raise_for_status()
        data = response.json()["data"]["timings"]
        return {
            "city": city,
            "times": {
                "Bomdod": data["Fajr"],
                "Peshin": data["Dhuhr"],
                "Asr": data["Asr"],
                "Shom": data["Maghrib"],
                "Xufton": data["Isha"],
            },
        }
    except Exception:
        raise HTTPException(status_code=502, detail="Namoz vaqtlari provayderidan ma’lumot olinmadi.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")))
