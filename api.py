import hashlib
import hmac
import json
import logging
import time

from urllib.parse import parse_qsl

from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import get_pool


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TAQVO_API")

app = FastAPI(
    title="TAQVO PRO MAX API",
    version="1.0.0",
    description="TAQVO PRO MAX backend API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://abdulhakiym.github.io",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


def verify_telegram_init_data(
    init_data: str,
) -> dict:
    if not init_data:
        raise HTTPException(
            status_code=401,
            detail="Telegram initData mavjud emas",
        )

    try:
        parsed = dict(parse_qsl(
            init_data,
            keep_blank_values=True,
        ))

        received_hash = parsed.pop("hash", None)

        if not received_hash:
            raise ValueError("Hash mavjud emas")

        auth_date = int(parsed.get("auth_date", "0"))

        current_time = int(time.time())

        if auth_date <= 0 or current_time - auth_date > 3600:
            raise ValueError("initData muddati tugagan")

        data_check_string = "\n".join(
            f"{key}={value}"
            for key, value in sorted(parsed.items())
        )

        secret_key = hmac.new(
            b"WebAppData",
            settings.BOT_TOKEN.encode(),
            hashlib.sha256,
        ).digest()

        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(
            calculated_hash,
            received_hash,
        ):
            raise ValueError("Telegram hash noto‘g‘ri")

        user = json.loads(parsed["user"])

        if not user.get("id"):
            raise ValueError("Telegram user ID mavjud emas")

        return user

    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        raise HTTPException(
            status_code=401,
            detail="Telegram foydalanuvchisi tasdiqlanmadi",
        ) from exc


@app.get("/")
async def root():
    return {
        "name": "TAQVO PRO MAX",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    try:
        pool = get_pool()

        async with pool.acquire() as connection:
            await connection.fetchval("SELECT 1")

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception:
        logger.exception("Health check xatosi")

        raise HTTPException(
            status_code=503,
            detail="Database bilan aloqa yo‘q",
        )


@app.get("/api/me")
async def get_my_profile(
    authorization: str | None = Header(default=None),
):
    if not authorization or not authorization.startswith("tma "):
        raise HTTPException(
            status_code=401,
            detail="Telegram autentifikatsiyasi talab qilinadi",
        )

    init_data = authorization[4:]

    telegram_user = verify_telegram_init_data(init_data)

    pool = get_pool()

    row = await pool.fetchrow(
        """
        SELECT
            id,
            first_name,
            username,
            language,
            country,
            city,
            timezone,
            subscribed
        FROM users
        WHERE id = $1
        """,
        telegram_user["id"],
    )

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Foydalanuvchi topilmadi",
        )

    return {
        "user": dict(row),
    }
