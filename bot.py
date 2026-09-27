from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# =========================
# PayP2P - Basic MVP
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🟢 Buy USDT", callback_data="buy"),
            InlineKeyboardButton("🔴 Sell USDT", callback_data="sell"),
        ],
        [
            InlineKeyboardButton("📋 My Orders", callback_data="orders"),
            InlineKeyboardButton("💼 Wallet", callback_data="wallet"),
        ],
        [
            InlineKeyboardButton("👤 Profile", callback_data="profile"),
            InlineKeyboardButton("🆘 Support", callback_data="support"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "💰 *Welcome to PayP2P*\n\n"
        "Buy & Sell USDT with BDT.\n"
        "Fast • Simple • Secure\n\n"
        "👇 Choose an option:",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "buy":
        keyboard = [
            [InlineKeyboardButton("💵 Buy USDT", callback_data="buy_usdt")],
            [InlineKeyboardButton("⬅️ Back", callback_data="home")],
        ]

        await query.edit_message_text(
            "🟢 *Buy USDT*\n\n"
            "Currently available payment methods:\n\n"
            "💳 bKash\n"
            "💳 Nagad\n"
            "🏦 Bank\n\n"
            "Choose an option below.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif query.data == "sell":
        keyboard = [
            [InlineKeyboardButton("💵 Sell USDT", callback_data="sell_usdt")],
            [InlineKeyboardButton("⬅️ Back", callback_data="home")],
        ]

        await query.edit_message_text(
            "🔴 *Sell USDT*\n\n"
            "Create a sell advertisement and receive BDT.\n\n"
            "⚠️ Real trading/escrow will be added in the next version.",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )

    elif query.data == "buy_usdt":
        await query.edit_message_text(
            "💵 *Buy USDT*\n\n"
            "No seller advertisements are available yet.\n\n"
            "Next version will show:\n"
            "• Seller rate\n"
            "• Available USDT\n"
            "• Payment method\n"
            "• Seller rating\n"
            "• Buy button",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="home")]
            ]),
            parse_mode="Markdown",
        )

    elif query.data == "sell_usdt":
        await query.edit_message_text(
            "💵 *Sell USDT*\n\n"
            "Seller advertisement system will be added next.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="home")]
            ]),
            parse_mode="Markdown",
        )

    elif query.data == "orders":
        await query.edit_message_text(
            "📋 *My Orders*\n\n"
            "You don't have any orders yet.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="home")]
            ]),
            parse_mode="Markdown",
        )

    elif query.data == "wallet":
        await query.edit_message_text(
            "💼 *Wallet*\n\n"
            "USDT Balance: `0.00 USDT`\n"
            "BDT Balance: `৳0.00`",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="home")]
            ]),
            parse_mode="Markdown",
        )

    elif query.data == "profile":
        user = query.from_user

        await query.edit_message_text(
            f"👤 *Profile*\n\n"
            f"Name: {user.first_name}\n"
            f"Username: @{user.username if user.username else 'Not set'}\n"
            f"User ID: `{user.id}`\n\n"
            f"Orders: 0\n"
            f"Success Rate: 100%",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="home")]
            ]),
            parse_mode="Markdown",
        )

    elif query.data == "support":
        await query.edit_message_text(
            "🆘 *PayP2P Support*\n\n"
            "For help with an order, contact the administrator.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="home")]
            ]),
            parse_mode="Markdown",
        )

    elif query.data == "home":
        keyboard = [
            [
                InlineKeyboardButton("🟢 Buy USDT", callback_data="buy"),
                InlineKeyboardButton("🔴 Sell USDT", callback_data="sell"),
            ],
            [
                InlineKeyboardButton("📋 My Orders", callback_data="orders"),
                InlineKeyboardButton("💼 Wallet", callback_data="wallet"),
            ],
            [
                InlineKeyboardButton("👤 Profile", callback_data="profile"),
                InlineKeyboardButton("🆘 Support", callback_data="support"),
            ],
        ]

        await query.edit_message_text(
            "💰 *PayP2P*\n\n"
            "Buy & Sell USDT with BDT.\n"
            "Fast • Simple • Secure\n\n"
            "👇 Choose an option:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown",
        )


def main():
    # Token will be added later through environment variable
    import os

    TOKEN = os.getenv("BOT_TOKEN")

    if not TOKEN:
        raise ValueError("BOT_TOKEN is not set!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("PayP2P Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
