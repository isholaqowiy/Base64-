import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
import database
import converter
import utils
import keyboards
from config import TEMP_DIR

ENCODE_STAGE, DECODE_STAGE = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    utils.ensure_temp_directory()
    uid = update.effective_user.id
    await database.register_user(uid)
    
    welcome = (
        "👋 Welcome to *Base64Image Bot*!\n"
        "Easily convert images to Base64 arrays and decode string blocks back into images.\n\n"
        "🖼 *Image → Base64 Compilation*\n"
        "🔄 *Base64 → Image Structural Extraction*\n"
        "📄 *Automatic Text File Exporter*\n\n"
        "Choose an option below or send an image to get started."
    )
    if update.message:
        await update.message.reply_text(welcome, reply_markup=keyboards.get_main_menu(), parse_mode="Markdown")
    return ConversationHandler.END

async def start_encode_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📥 Please send the *Photo/Image* asset you want to convert into Base64 format:", parse_mode="Markdown")
    return ENCODE_STAGE

async def handle_encode_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    photo = update.message.photo[-1]
    
    tg_file = await context.bot.get_file(photo.file_id)
    input_path = os.path.join(TEMP_DIR, f"img_{uid}.png")
    await tg_file.download_to_drive(input_path)
    
    await update.message.reply_text("⚡ Processing and computing image string vectors...")
    
    b64_str, txt_file, dims, fmt = converter.encode_image_to_base64(input_path, uid)
    
    if b64_str and os.path.exists(txt_file):
        preview = b64_str[:250] + "..."
        caption = (
            f"✅ *Base64 Encoding Complete!*\n\n"
            f"📐 *Dimensions:* `{dims}`\n"
            f"📄 *Format:* `{fmt}`\n"
            f"🔢 *String Length:* `{len(b64_str)}` characters\n\n"
            f"📝 *Preview:* \n`data:image/png;base64,{preview}`"
        )
        with open(txt_file, "rb") as f:
            await update.message.reply_document(document=f, filename="base64_string.txt", caption=caption, parse_mode="Markdown")
        await database.save_history_log(uid, "Encode", f"Image ({dims}) → Base64")
        utils.clean_user_files(uid)
    else:
        await update.message.reply_text("❌ System encoding transformation error execution trace failure.")
        
    return ConversationHandler.END

async def start_decode_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("📥 Please paste your raw *Base64 String block* context directly here to re-compile it back into an image:", parse_mode="Markdown")
    return DECODE_STAGE

async def handle_decode_string(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    raw_b64 = update.message.text
    
    await update.message.reply_text("⚡ Validating and processing data array sequences...")
    
    output_image = converter.decode_base64_to_image(raw_b64, uid)
    
    if output_image and os.path.exists(output_image):
        with open(output_image, "rb") as f:
            await update.message.reply_photo(photo=f, caption="✨ Reconstruction complete! Vector structures converted cleanly via Base64Image Engine.")
        await database.save_history_log(uid, "Decode", f"Base64 String → Extracted Image")
        utils.clean_user_files(uid)
    else:
        await update.message.reply_text("❌ Invalid or corrupt Base64 string data blocks tracking mapping boundary layout parameters error.")
        
    return ConversationHandler.END

async def menu_navigation_routing(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id
    
    if query.data == "nav_logs":
        history = await database.get_user_history(uid)
        if not history:
            await query.message.reply_text("📂 You have not initialized any conversion tasks across your workspace records history index yet.", reply_markup=keyboards.get_main_menu())
        else:
            msg = "📂 *Your Recent Data Conversions Logs History Index:*\n\n" + "\n".join([f"- [{item['type']}] {item['summary']}" for item in history])
            await query.message.reply_text(msg, reply_markup=keyboards.get_main_menu(), parse_mode="Markdown")
    elif query.data == "nav_help":
        help_text = (
            "❓ *Base64 Technical Documentation Manual*\n\n"
            "Base64 converts raw binary image frames into clear text layout streams "
            "allowing assets to be loaded inline without remote calls within HTML/CSS script configurations.\n\n"
            "💡 *Usage:* Tap 'Image → Base64', send any photo, and parse text vectors instantly."
        )
        await query.message.reply_text(help_text, reply_markup=keyboards.get_main_menu(), parse_mode="Markdown")

