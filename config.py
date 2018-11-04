import os

class Config(object):
  DEBUG = False
  TESTING = False
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(Config):
  DEBUG = True

class Production(Config):
  SQLALCHEMY_DATABASE_URI = 'sqlite:///base.db'

app_config = {
  'development': Development,
  'production': Production,
}