import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from datetime import datetime, timedelta
import aiohttp
import json
from config import Config
from utils import get_forex_signals, get_market_news, get_economic_calendar

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class ForexSignalBot:
    def __init__(self):
        self.token = Config.TELEGRAM_BOT_TOKEN
        self.application = None
        self.user_states = {}
        self.last_signal_time = {}

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when /start is issued."""
        user = update.effective_user
        welcome_text = f"""
🤖 *Welcome to Forex Signal Bot, {user.first_name}!*

I provide real-time Forex trading signals and market analysis.

📊 *Available Commands:*
/signals - Get latest trading signals
/market - View current market status
/news - Latest forex news
/economic - Economic calendar
/settings - Configure your preferences
/help - Show this message

🔔 *Features:*
• Real-time buy/sell signals
• Risk management suggestions
• Market analysis
• Economic event notifications

*Status:* 🟢 Online
"""
        await update.message.reply_text(welcome_text, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message when /help is issued."""
        help_text = """
📚 *Help & Commands Guide*

*Basic Commands:*
/signals - Get forex signals for major pairs
/market - View current market prices
/news - Latest forex news
/economic - Upcoming economic events
/settings - Configure your preferences
/subscribe - Subscribe to premium signals
/unsubscribe - Unsubscribe from signals

*Signal Format:*
📈 BUY EURUSD
Entry: 1.0950
SL: 1.0900
TP1: 1.1000
TP2: 1.1050
Risk: 1%

*Tips:*
• Always use stop loss
• Don't risk more than 2% per trade
• Follow your trading plan

*Support:* @forexsignal_support
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def signals_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get forex signals."""
        try:
            # Send typing indicator
            await update.message.chat.send_action(action="typing")
            
            signals = await get_forex_signals()
            
            if not signals:
                await update.message.reply_text(
                    "⚠️ *No signals available at the moment.*\nPlease try again later.",
                    parse_mode='Markdown'
                )
                return

            for signal in signals[:5]:  # Limit to 5 signals
                signal_text = f"""
📊 *{signal['pair']}*

📈 *Signal: {signal['action']}*
💵 Entry: {signal['entry']}
🔴 Stop Loss: {signal['stop_loss']}
🎯 Take Profit 1: {signal['take_profit_1']}
🎯 Take Profit 2: {signal['take_profit_2']}

📈 *Confidence:* {signal['confidence']}%
⚠️ *Risk:* {signal['risk']}%

*Analysis:*
{signal['analysis']}

*Key Levels:*
Support: {signal.get('support', 'N/A')}
Resistance: {signal.get('resistance', 'N/A')}

🕐 *Time:* {signal['time']}
"""
                
                keyboard = [
                    [
                        InlineKeyboardButton("✅ Approve", callback_data=f"approve_{signal['pair']}"),
                        InlineKeyboardButton("❌ Reject", callback_data=f"reject_{signal['pair']}")
                    ],
                    [
                        InlineKeyboardButton("📊 More Details", callback_data=f"details_{signal['pair']}")
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    signal_text,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
                
        except Exception as e:
            logger.error(f"Error in signals command: {e}")
            await update.message.reply_text(
                "❌ *Error fetching signals.*\nPlease try again later.",
                parse_mode='Markdown'
            )

    async def market_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get current market status."""
        try:
            await update.message.chat.send_action(action="typing")
            
            # Sample market data - In production, fetch from API
            market_data = """
📊 *Market Status*

*Major Pairs:*
🇪🇺 EUR/USD: 1.0950 (+0.15%)
🇬🇧 GBP/USD: 1.2650 (-0.08%)
🇯🇵 USD/JPY: 148.50 (+0.22%)
🇨🇭 USD/CHF: 0.8750 (-0.12%)

*Commodities:*
🥇 Gold: $2,050 (+0.45%)
🥈 Silver: $24.50 (+0.30%)

*Indices:*
📈 S&P 500: 4,800 (+0.25%)
📈 NASDAQ: 16,900 (+0.35%)

*Market Sentiment:* 📈 Bullish

*Volatility:* 🔴 High
*Risk Appetite:* Moderate
"""
            await update.message.reply_text(market_data, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in market command: {e}")
            await update.message.reply_text("❌ Error fetching market data.")

    async def news_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get latest forex news."""
        try:
            await update.message.chat.send_action(action="typing")
            
            news = await get_market_news()
            
            if not news:
                await update.message.reply_text("📰 No recent news available.")
                return
            
            news_text = "📰 *Latest Forex News*\n\n"
            for item in news[:3]:
                news_text += f"🔹 *{item['title']}*\n"
                news_text += f"📝 {item['summary'][:100]}...\n"
                news_text += f"🕐 {item['time']}\n\n"
            
            await update.message.reply_text(news_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in news command: {e}")
            await update.message.reply_text("❌ Error fetching news.")

    async def economic_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Get economic calendar."""
        try:
            await update.message.chat.send_action(action="typing")
            
            events = await get_economic_calendar()
            
            if not events:
                await update.message.reply_text("📅 No economic events scheduled.")
                return
            
            events_text = "📅 *Economic Calendar*\n\n"
            for event in events[:5]:
                events_text += f"🕐 {event['time']} - {event['currency']}\n"
                events_text += f"📊 *{event['event']}*\n"
                events_text += f"📈 Forecast: {event['forecast']} | Previous: {event['previous']}\n"
                events_text += f"⭐ Impact: {event['impact']}\n\n"
            
            await update.message.reply_text(events_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in economic command: {e}")
            await update.message.reply_text("❌ Error fetching economic calendar.")

    async def settings_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Configure user settings."""
        keyboard = [
            [
                InlineKeyboardButton("📊 Signal Frequency", callback_data="set_frequency"),
                InlineKeyboardButton("📈 Pairs", callback_data="set_pairs")
            ],
            [
                InlineKeyboardButton("🔔 Notifications", callback_data="set_notifications"),
                InlineKeyboardButton("📊 Risk Level", callback_data="set_risk")
            ],
            [
                InlineKeyboardButton("💾 Save Settings", callback_data="save_settings")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⚙️ *Settings*\n\nConfigure your preferences:",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks."""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data.startswith("approve_"):
            pair = data.replace("approve_", "")
            await query.edit_message_text(
                f"✅ Signal for {pair} approved!",
                parse_mode='Markdown'
            )
            
        elif data.startswith("reject_"):
            pair = data.replace("reject_", "")
            await query.edit_message_text(
                f"❌ Signal for {pair} rejected.",
                parse_mode='Markdown'
            )
            
        elif data.startswith("details_"):
            pair = data.replace("details_", "")
            details = f"""
📊 *Detailed Analysis for {pair}*

*Technical Indicators:*
📈 RSI: 65 (Overbought)
📊 MACD: Bullish crossover
📉 Moving Averages: 50 > 200 (Golden Cross)

*Support/Resistance:*
🟢 Support: 1.0900
🔴 Resistance: 1.1000

*Risk Assessment:*
📊 Risk/Reward: 1:2
⚡ Volatility: Medium
🎯 Profit Potential: High

*Recommendation:* Consider entering at current level
"""
            await query.edit_message_text(
                details,
                parse_mode='Markdown'
            )

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    def setup_handlers(self):
        """Setup all command handlers."""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("signals", self.signals_command))
        self.application.add_handler(CommandHandler("market", self.market_command))
        self.application.add_handler(CommandHandler("news", self.news_command))
        self.application.add_handler(CommandHandler("economic", self.economic_command))
        self.application.add_handler(CommandHandler("settings", self.settings_command))
        
        # Callback query handler
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)

    async def run(self):
        """Run the bot."""
        try:
            # Create application
            self.application = Application.builder().token(self.token).build()
            
            # Setup handlers
            self.setup_handlers()
            
            # Start bot
            logger.info("Starting bot...")
            await self.application.initialize()
            await self.application.start()
            
            # Start polling
            await self.application.updater.start_polling()
            
            logger.info("Bot is running!")
            
            # Keep the bot running
            while True:
                await asyncio.sleep(3600)
                
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            raise

def main():
    """Main function to run the bot."""
    try:
        bot = ForexSignalBot()
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        # In production, you might want to implement automatic restart
        raise

if __name__ == '__main__':
    main()
