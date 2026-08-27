import threading
import logging
from flask import Flask

logger = logging.getLogger(__name__)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/health')
def health():
    return "Healthy", 200

def run_web():
    """Run web server to keep bot alive."""
    try:
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        logger.error(f"Web server error: {e}")

def start_web_server():
    """Start web server in a separate thread."""
    thread = threading.Thread(target=run_web)
    thread.daemon = True
    thread.start()
    logger.info("Web server started on port 8080")
