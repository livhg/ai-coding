import os
from datetime import timedelta

class Config:
    """Application configuration."""
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    PORT = int(os.environ.get('PORT', 5001))
    HOST = os.environ.get('HOST', '0.0.0.0')
    CACHE_DIR = os.environ.get('CACHE_DIR', 'cache')
    CACHE_DURATION_MINUTES = int(os.environ.get('CACHE_DURATION_MINUTES', 30))
