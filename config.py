import os

class Config:
    # Bot Configuration
    TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
    
    # API Keys (Store in Railway Environment Variables)
    ALPHA_VANTAGE_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "")
    NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "")
    
    # Database (Optional - for persistent storage)
    DATABASE_URL = os.environ.get("DATABASE_URL", "")
    
    # Bot Settings
    SIGNAL_INTERVAL = int(os.environ.get("SIGNAL_INTERVAL", 3600))  # 1 hour
    MAX_SIGNALS_PER_DAY = int(os.environ.get("MAX_SIGNALS_PER_DAY", 10))
    
    # API Endpoints
    FOREX_API_URL = "https://api.example.com/forex"
    NEWS_API_URL = "https://newsapi.org/v2/everything"
    
    # Error Handling
    MAX_RETRIES = 3
    RETRY_DELAY = 5
