import random
import aiohttp
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

async def get_forex_signals() -> List[Dict]:
    """Fetch forex signals from API or generate sample data."""
    try:
        # In production, fetch from real API
        # For now, generate sample signals
        
        pairs = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]
        actions = ["BUY", "SELL"]
        
        signals = []
        for pair in random.sample(pairs, min(3, len(pairs))):
            action = random.choice(actions)
            price = round(random.uniform(1.05, 1.15), 4)
            
            if action == "BUY":
                sl = round(price - random.uniform(0.0020, 0.0050), 4)
                tp1 = round(price + random.uniform(0.0030, 0.0080), 4)
                tp2 = round(price + random.uniform(0.0080, 0.0150), 4)
            else:
                sl = round(price + random.uniform(0.0020, 0.0050), 4)
                tp1 = round(price - random.uniform(0.0030, 0.0080), 4)
                tp2 = round(price - random.uniform(0.0080, 0.0150), 4)
            
            signal = {
                "pair": pair,
                "action": action,
                "entry": str(price),
                "stop_loss": str(sl),
                "take_profit_1": str(tp1),
                "take_profit_2": str(tp2),
                "confidence": random.randint(65, 95),
                "risk": f"{round(random.uniform(0.5, 2.0), 1)}%",
                "analysis": "Based on technical analysis and market sentiment",
                "support": str(round(price - random.uniform(0.01, 0.02), 4)),
                "resistance": str(round(price + random.uniform(0.01, 0.02), 4)),
                "time": datetime.now().strftime("%H:%M")
            }
            signals.append(signal)
        
        return signals
        
    except Exception as e:
        logger.error(f"Error fetching signals: {e}")
        return []

async def get_market_news() -> List[Dict]:
    """Fetch market news."""
    try:
        # Sample news data
        news = [
            {
                "title": "Fed Signals Rate Cut Possibility",
                "summary": "Federal Reserve officials hint at potential rate cuts amid economic uncertainty...",
                "time": datetime.now().strftime("%H:%M")
            },
            {
                "title": "EUR/USD Rises on Weak Dollar",
                "summary": "Euro strengthens against dollar following US economic data...",
                "time": (datetime.now() - timedelta(hours=1)).strftime("%H:%M")
            },
            {
                "title": "Oil Prices Surge on Supply Concerns",
                "summary": "Crude oil prices jump as supply disruptions continue...",
                "time": (datetime.now() - timedelta(hours=2)).strftime("%H:%M")
            }
        ]
        return news
        
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return []

async def get_economic_calendar() -> List[Dict]:
    """Fetch economic calendar events."""
    try:
        events = [
            {
                "time": "08:30",
                "currency": "USD",
                "event": "Initial Jobless Claims",
                "forecast": "220K",
                "previous": "215K",
                "impact": "HIGH"
            },
            {
                "time": "09:00",
                "currency": "EUR",
                "event": "ECB President Speech",
                "forecast": "-",
                "previous": "-",
                "impact": "MEDIUM"
            },
            {
                "time": "10:00",
                "currency": "GBP",
                "event": "BOE Interest Rate Decision",
                "forecast": "5.25%",
                "previous": "5.25%",
                "impact": "HIGH"
            }
        ]
        return events
        
    except Exception as e:
        logger.error(f"Error fetching calendar: {e}")
        return []

async def send_notification(bot, user_id, message):
    """Send notification to user."""
    try:
        await bot.send_message(
            chat_id=user_id,
            text=message,
            parse_mode='Markdown'
        )
        return True
    except Exception as e:
        logger.error(f"Error sending notification to {user_id}: {e}")
        return False
