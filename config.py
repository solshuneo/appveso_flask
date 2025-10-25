import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    # For Vercel, use PostgreSQL if DATABASE_URL is provided, otherwise SQLite for local dev
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # Convert PostgreSQL URL to SQLAlchemy format if needed
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
