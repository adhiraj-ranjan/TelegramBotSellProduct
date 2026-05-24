import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========================= CONFIG =========================
TOKEN = "8636995466:AAFhMbp4RFMaaJibem2QJJ91ArTxZLN-zQo"   # ← Get from @BotFather

OWNER_ID = 6141569999            # ← REPLACE WITH YOUR TELEGRAM USER ID

# Product Image
PRODUCT_IMAGE = "img.jpg"

# Payment QR Code Image
PAYMENT_QR_IMAGE = "qr.jpg"

PRODUCT_CAPTION = """
𝟱𝟱𝗞 𝗣𝗥𝗘𝗠𝗜𝗨𝗠 𝗤𝗨𝗔𝗟𝗜𝗧𝗬 𝗩𝗜𝗗𝗘𝗢 𝗚𝗥𝗢𝗨𝗣
 𝗘𝗞 𝗕𝗔𝗥 𝗕𝗨𝗬 𝗞𝗔𝗥𝗢 𝗟𝗜𝗙𝗘 𝗧𝗜𝗠𝗘 𝗞𝗔 𝗝𝗨𝗚𝗔𝗔𝗗  💋

𝘿𝙄𝙍𝙀𝘾𝙏 𝙑𝙄𝘿𝙀𝙊 𝙏𝙀𝙇𝙀𝙂𝙍𝘼𝙈 𝙋𝙀𝙍 𝙈𝙄𝙇𝙀𝙂𝘼 𝙉𝙊 𝘼𝘿𝙎 𝙉𝙊 𝙇𝙄𝙉𝙆 𝘿𝙄𝙍𝙀𝘾𝙏 𝙊𝙋𝙀𝙉 𝙑𝙄𝘿𝙀𝙊 😍😍

Is Group me ye saara exclusive content milega 
👇👇👇
• Desi Bhabhi
• Mom-Son
• Couple Videos
• Snapchat Leaked Snaps
• Instagram Viral Reels
• Aur bohot kuch ⏩⏩

🎀 Just pay and get entry... Direct video No Link - No Ads Sh#t 🔥
Validity :- Lifetime🔥 Click on get premium to join 🥳


𝗣𝗥𝗜𝗖𝗘 𝗝𝗨𝗦𝗧 :- ₹49 ONLY
"""

PAYMENT_CAPTION = """
⚡ 𝐏𝐀𝐘𝐌𝐄𝐍𝐓 𝐆𝐀𝐓𝐄𝐖𝐀𝐘

📛 𝐀𝐜𝐜𝐞𝐬𝐬: Lifetime VIP
💵 𝐀𝐦𝐨𝐮𝐧𝐭: ₹46
🏦 𝐔𝐏𝐈 𝐈𝐃: BHARATPE.9M0H0Q0A6Q387178@unitype

1️⃣ 𝐒𝐜𝐚𝐧 𝐐𝐑 𝐂𝐨𝐝𝐞
2️⃣ 𝐏𝐚𝐲 𝐮𝐬𝐢𝐧𝐠 𝐔𝐏𝐈
3️⃣ 𝐂𝐥𝐢𝐜𝐤 𝐛𝐮𝐭𝐭𝐨𝐧 𝐛𝐞𝐥𝐨𝐰
"""

# Track users waiting for proof
user_states = {}

# ========================================================

async def notify_owner(context: ContextTypes.DEFAULT_TYPE, message: str):
    try:
        await context.bot.send_message(chat_id=OWNER_ID, text=message)
    except Exception as e:
        logger.error(f"Failed to notify owner: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Notify owner about new user
    user_info = f"""
🆕 New User Started Bot

👤 Name: {user.first_name} {user.last_name or ''}
🔹 Username: @{user.username if user.username else 'None'}
🆔 User ID: <code>{user.id}</code>
📅 Time: {update.message.date}
    """
    await notify_owner(context, user_info.strip())

    keyboard = [
        [InlineKeyboardButton("💎 Buy Premium", callback_data="buy_premium")],
        [InlineKeyboardButton("👀 View Demo", url="https://t.me/SwanChestowner")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_photo(
            photo=PRODUCT_IMAGE,
            caption=PRODUCT_CAPTION,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    elif update.callback_query:
        await update.callback_query.message.reply_photo(
            photo=PRODUCT_IMAGE,
            caption=PRODUCT_CAPTION,
            parse_mode='HTML',
            reply_markup=reply_markup
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "buy_premium":
        keyboard = [
            [InlineKeyboardButton("✅ I have paid", callback_data="paid_proof")],
            # [InlineKeyboardButton("❌ Cancel Order", callback_data="cancel_order")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_photo(
            photo=PAYMENT_QR_IMAGE,
            caption=PAYMENT_CAPTION,
            parse_mode='HTML',
            reply_markup=reply_markup
        )

    elif query.data == "cancel_order":
        await query.message.reply_text("✅ Order cancelled.")
        await start(update, context)

    elif query.data == "paid_proof":
        user_states[user_id] = "waiting_proof"
        await query.message.reply_text(
            "📸 Please send the payment screenshot now.\n\n"
            "Make sure the transaction details are clearly visible."
        )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user = update.message.from_user

    if user_states.get(user_id) == "waiting_proof":
        # Notify owner about payment proof
        proof_info = f"""
💰 New Payment Proof Received

👤 From: {user.first_name} {user.last_name or ''}
🔹 Username: @{user.username if user.username else 'None'}
🆔 User ID: <code>{user.id}</code>
        """
        await notify_owner(context, proof_info.strip())
        
        # Forward the screenshot to owner
        await update.message.forward(chat_id=OWNER_ID)
        
        await update.message.reply_text(
            "✅ Payment proof received!\n\n"
            "Our team will verify it shortly and grant you access within 5-30 minutes."
        )
        
        del user_states[user_id]
    else:
        await update.message.reply_text("Please use the menu buttons to proceed.")


def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    print("🤖 Bot is running... Owner notifications enabled.")
    application.run_polling()


if __name__ == '__main__':
    main()