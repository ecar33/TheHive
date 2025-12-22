import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Rate Limiting
    RATELIMIT_STORAGE_URL = "memory://"
    RATELIMIT_HEADERS_ENABLED = True
    RATELIMIT_DEFAULT = "200 per hour"

class DevelopmentConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    uri = os.getenv("DATABASE_URL")

    # Heroku gives postgres:// but SQLAlchemy expects postgresql://
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    uri = os.getenv("DATABASE_URL")

    # Heroku gives postgres:// but SQLAlchemy expects postgresql://
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = uri