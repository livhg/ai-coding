import os

class Config:
    """Application configuration."""
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    DATABASE = os.environ.get('DATABASE', 'todos.db')
    PORT = int(os.environ.get('PORT', 5000))
    HOST = os.environ.get('HOST', '0.0.0.0')
