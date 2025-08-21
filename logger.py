import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO, ### Debug không show ra màn hình do thấp hơn INFO
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("o_transaction_analytics_api.log"),
        logging.StreamHandler()  # Also print to console
    ]
)

# Create logger for our API
logger = logging.getLogger("o_transaction_analytics_api")