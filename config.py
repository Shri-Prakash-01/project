import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# Get the base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database - use /tmp for SQLite on Render (ephemeral filesystem)
    # Better to use PostgreSQL in production, but SQLite works with /tmp
    instance_path = os.path.join(BASE_DIR, 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    # For Render, use /tmp for SQLite (writable)
    if os.environ.get('RENDER'):
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/secure_vault.db'
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(instance_path, 'secure_vault.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload folder - use /tmp on Render
    if os.environ.get('RENDER'):
        UPLOAD_FOLDER = '/tmp/uploads'
    else:
        UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    
    # Security
    BCRYPT_LOG_ROUNDS = 12
    RATE_LIMIT_DEFAULT = "100 per hour"
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = True  # True in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
