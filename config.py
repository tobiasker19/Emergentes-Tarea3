import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'iot_data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'key_token'
    ADMIN_TOKEN = 'admin_token'  
