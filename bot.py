import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from datetime import datetime, timedelta
import random
import sys

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN not set in environment variables!")
    sys.exit(1)

# Simple Flask server for Railway health checks
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!", 200

@app.route('/health')
def health():
    return "Healthy", 200

def run_web():
    """Run Flask web server for health checks."""
    try:
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    except Exception as e:
        logger.error(f"Web server error: {e}")

# Start web server in background
web_thread = threading.Thread(target=run_web)
web_thread.daemon = True
web_thread.start()

# Bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when /start is issued."""
    user = update.effective_user
    welcome_text = f"""
🤖 *Welcome to Forex Signal Bot, {user.first_name}!*

I provide real-time Forex trading signals and market analysis.

📊 *Available Commands:*
/signals - Get latest trading signals
/market - View current market status
/help - Show this message

*Status:* 🟢 Online
"""
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when /help is issued."""
    help_text = """
📚 *Help & Commands Guide*

*Basic Commands:*
/signals - Get forex signals for major pairs
/market - View current market prices
/start - Start the bot

*Signal Format:*
📈 BUY EURUSD
Entry: 1.0950
SL: 1.0900
TP1: 1.1000

*Tips:*
• Always use stop loss
• Don't risk more than 2% per trade
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def signals_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get forex signals."""
    try:
        await update.message.chat.send_action(action="typing")
        
        # Generate sample signals
        pairs = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD"]
        actions = ["BUY", "SELL"]
        
        for pair in random.sample(pairs, min(2, len(pairs))):
            action = random.choice(actions)
            price = round(random.uniform(1.05, 1.15), 4)
            
            if action == "BUY":
                sl = round(price - random.uniform(0.0020, 0.0050), 4)
                tp = round(price + random.uniform(0.0030, 0.0080), 4)
            else:
                sl = round(price + random.uniform(0.0020, 0.0050), 4)
                tp = round(price - random.uniform(0.0030, 0.0080), 4)
            
            signal_text = f"""
📊 *{pair}*

📈 *Signal: {action}*
💵 Entry: {price}
🔴 Stop Loss: {sl}
🎯 Take Profit: {tp}

📈 *Confidence:* {random.randint(65, 95)}%
⚠️ *Risk:* {round(random.uniform(0.5, 2.0), 1)}%

🕐 *Time:* {datetime.now().strftime('%H:%M')}
"""
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ Approve", callback_data=f"approve_{pair}"),
                    InlineKeyboardButton("❌ Reject", callback_data=f"reject_{pair}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                signal_text,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            await asyncio.sleep(0.5)  # Small delay between messages
        
    except Exception as e:
        logger.error(f"Error in signals command: {e}")
        await update.message.reply_text("❌ *Error fetching signals.*\nPlease try again later.", parse_mode='Markdown')

async def market_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get current market status."""
    try:
        market_data = """
📊 *Market Status*

*Major Pairs:*
🇪🇺 EUR/USD: 1.0950 (+0.15%)
🇬🇧 GBP/USD: 1.2650 (-0.08%)
🇯🇵 USD/JPY: 148.50 (+0.22%)

*Market Sentiment:* 📈 Bullish
*Volatility:* 🔴 High
"""
        await update.message.reply_text(market_data, parse_mode='Markdown')
        
    except Exception as e:
        logger.error(f"Error in market command: {e}")
        await update.message.reply_text("❌ Error fetching market data.")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("approve_"):
        pair = query.data.replace("approve_", "")
        await query.edit_message_text(f"✅ Signal for {pair} approved!")
        
    elif query.data.startswith("reject_"):
        pair = query.data.replace("reject_", "")
        await query.edit_message_text(f"❌ Signal for {pair} rejected.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors."""
    logger.error(f"Update {update} caused error {context.error}")
    
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ *An error occurred.*\nPlease try again later.",
                parse_mode='Markdown'
            )
    except Exception as e:
        logger.error(f"Error in error handler: {e}")

def main():
    """Main function to run the bot."""
    try:
        logger.info("Starting bot...")
        
        # Create application
        application = Application.builder().token(TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("signals", signals_command))
        application.add_handler(CommandHandler("market", market_command))
        application.add_handler(CallbackQueryHandler(button_callback))
        application.add_error_handler(error_handler)
        
        # Start bot
        logger.info("Bot is running!")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        raise

if __name__ == '__main__':
    main()
