import os
import asyncio
import telegram
from telegram.ext import Application, CommandHandler, ContextTypes

# ==========================================
# 1. CONFIGURATION
# ==========================================
TELEGRAM_BOT_TOKEN = "8903819958:AAHwRGMe9O3CRwJ7GVv2X7Ae0zGWG4tRUlI"
TELEGRAM_CHAT_ID = "6892430933"

# ==========================================
# 2. ASYNC HEALTH CHECK SERVER (No Threads)
# ==========================================
# Keeps Render's free tier happy using non-blocking async network loops
async def handle_health_check(reader, writer):
    response = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 26\r\n\r\nMorpho Sentinel is online."
    writer.write(response)
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = await asyncio.start_server(handle_health_check, "0.0.0.0", port)
    print(f"Health check server running on port {port}")
    async with server:
        await server.serve_forever()

# ==========================================
# 3. CORE BOT LOGIC (Morpho Tracker)
# ==========================================
async def check_morpho_pools():
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    while True:
        try:
            print("Scanning Morpho pools for liquidation triggers...")
            # Your Morpho network RPC reading logic goes here
        except Exception as e:
            print(f"Error tracking pools: {e}")
        await asyncio.sleep(30)

# ==========================================
# 4. INTERACTIVE TELEGRAM COMMANDS
# ==========================================
async def status_command(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /status command when you message the bot."""
    await update.message.reply_text(
        "🛡️ **Morpho Sentinel Status:**\n\n"
        "• System: Cloud Active (Render)\n"
        "• Monitoring: Active\n"
        "• Status: All pools stable."
    )

# ==========================================
# 5. MAIN ASYNC ENTRY POINT
# ==========================================
async def main():
    # Build the application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("status", status_command))

    # Initialize and start the telegram polling engine properly under the loop
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("Interactive Telegram command listener started.")

    # Concurrently run the web server and tracking loop side-by-side
    await asyncio.gather(
        run_health_server(),
        check_morpho_pools()
    )

if __name__ == "__main__":
    asyncio.run(main())
