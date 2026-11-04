async def onboard(uid: int, first_name: str, send):
    """Obuna tasdiqlangach, foydalanuvchini ismi bilan kutib olish."""

    name = (first_name or "").strip() or "aziz birodar"

    await send(
        "Assalomu alaykum va rohmatullohi va barokatuh! 🤲\n\n"
        f"Xush kelibsiz, {name}!\n\n"
        "TAQVO PRO MAX loyihasiga xush kelibsiz."
    )

    city = await pool.fetchval(
        "SELECT city FROM users WHERE id=$1",
        uid
    )

    if city:
        await send(APP_TEXT, app_kb())
    else:
        await send(ASK_COUNTRY, countries_kb())


@dp.message(CommandStart())
async def start(m: Message):
    uid = m.from_user.id

    await pool.execute(
        """
        INSERT INTO users(id, first_name)
        VALUES($1, $2)
        ON CONFLICT (id)
        DO UPDATE SET first_name=$2, enabled=TRUE
        """,
        uid,
        m.from_user.first_name
    )

    sub = await is_subscribed(uid)

    if sub is None:
        await m.answer(CANT_CHECK)

    elif sub:
        await onboard(
            uid,
            m.from_user.first_name,
            lambda text, markup=None: m.answer(
                text,
                reply_markup=markup
            )
        )

    else:
        await m.answer(
            SUBSCRIBE_TEXT,
            reply_markup=subscribe_kb()
        )


@dp.callback_query(F.data == "check")
async def check(c: CallbackQuery):
    sub = await is_subscribed(c.from_user.id)

    if sub is None:
        await c.answer(CANT_CHECK, show_alert=True)
        return

    if not sub:
        await c.answer(
            "Avval kanalga obuna bo‘ling.",
            show_alert=True
        )
        return

    await c.answer("Obuna tasdiqlandi!")

    await pool.execute(
        """
        INSERT INTO users(id, first_name)
        VALUES($1, $2)
        ON CONFLICT (id)
        DO UPDATE SET first_name=$2, enabled=TRUE
        """,
        c.from_user.id,
        c.from_user.first_name
    )

    await c.message.delete()

    await onboard(
        c.from_user.id,
        c.from_user.first_name,
        lambda text, markup=None: c.bot.send_message(
            c.from_user.id,
            text,
            reply_markup=markup
        )
    )
