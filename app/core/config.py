import os

# Application settings
APP_NAME = "Smart Summarizer API"
API_PREFIX = "/api"
DEBUG = False

# Model settings
MODEL_NAME = os.getenv("MODEL_NAME", "t5-small")

# Rate limiting
RATE_LIMIT_ENABLED = True
RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW = 60

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"