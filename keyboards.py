from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🖼 Image → Base64", callback_data="nav_to_b64")],
        [InlineKeyboardButton("🔄 Base64 → Image", callback_data="nav_to_img")],
        [InlineKeyboardButton("📚 Conversion Logs", callback_data="nav_logs"),
         InlineKeyboardButton("❓ Help Manual", callback_data="nav_help")]
    ]
    return InlineKeyboardMarkup(keyboard)

