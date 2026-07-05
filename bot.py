import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
import database
import handlers
from config import BOT_TOKEN

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(database.init_db())

    if not BOT_TOKEN:
        print("Fatal error: Missing BOT_TOKEN structural runtime variable environment setting mapping parameters data.")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    encoder_wizard = ConversationHandler(
        entry_points=[CallbackQueryHandler(handlers.start_encode_flow, pattern="^nav_to_b64$")],
        states={handlers.ENCODE_STAGE: [MessageHandler(filters.PHOTO, handlers.handle_encode_photo)]},
        fallbacks=[CommandHandler("start", handlers.start)]
    )

    decoder_wizard = ConversationHandler(
        entry_points=[CallbackQueryHandler(handlers.start_decode_flow, pattern="^nav_to_img$")],
        states={handlers.DECODE_STAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_decode_string)]},
        fallbacks=[CommandHandler("start", handlers.start)]
    )

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CallbackQueryHandler(handlers.menu_navigation_routing, pattern="^nav_"))
    app.add_handler(encoder_wizard)
    app.add_handler(decoder_wizard)

    print("Base64Image Core Engine Running & Polling Live instances...")
    app.run_polling()

if __name__ == '__main__':
    main()

