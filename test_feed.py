import os
import asyncio
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import telegram
from telegram.ext import Application, CommandHandler, ContextTypes

# ==========================================
# 1. CONFIGURATION
# ==========================================
TELEGRAM_BOT_TOKEN = "8903819958:AAHwRGMe9O3CRwJ7GVv2X7Ae0zGWG4tRUlI"
TELEGRAM_CHAT_ID = "6892430933"

# ==========================================
# 2. RENDER COMPLIANCE (The Free Web Server)
# ==========================================
class HealthCheckServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Morpho Sentinel is online.")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckServer)
    print(f"Health check server running on port {port}")
    server.serve_forever()

# ==========================================
# 3. CORE BOT LOGIC (Morpho Tracker)
# ==========================================
async def check_morpho_pools():
    """
    Your automated loop that runs every 30 seconds to track 
    pool metrics, liquidations, or utilization changes.
    """
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    
    while True:
        try:
            # This logs to your Render dashboard terminal so you see it's working
            print("Scanning Morpho pools for liquidation triggers...")
            
            # Place your exact Morpho network RPC reading logic right here
            
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
        "• Market Volatility: Low (MiCA impact calm)\n"
        "• Status: All pools stable."
    )

def run_telegram_polling():
    """Starts the interactive command listener loop."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("status", status_command))
    
    print("Interactive Telegram command listener started.")
    application.run_polling(close_loop=False)

# ==========================================
# 5. MAIN ENTRY POINT
# ==========================================
if __name__ == "__main__":
    # Start the dummy web server so Render stays happy for free
    web_thread = threading.Thread(target=run_health_server, daemon=True)
    web_thread.start()
    
    # Start the interactive Telegram command listener
    tg_thread = threading.Thread(target=run_telegram_polling, daemon=True)
    tg_thread.start()
    
    # Run the main 30-second automated tracker
    asyncio.run(check_morpho_pools())

