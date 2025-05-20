class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///feedback.db'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:kayodeso@localhost/feedback'
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:kayodeso@localhost/feedback'
