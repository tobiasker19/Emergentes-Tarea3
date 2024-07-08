from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    company_api_key = db.Column(db.String(100), nullable=False)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    location_name = db.Column(db.String(100), nullable=False)
    location_country = db.Column(db.String(100), nullable=False)
    location_city = db.Column(db.String(100), nullable=False)
    location_meta = db.Column(db.String(100))

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    sensor_name = db.Column(db.String(100), nullable=False)
    sensor_category = db.Column(db.String(100), nullable=False)
    sensor_meta = db.Column(db.String(100))
    sensor_api_key = db.Column(db.String(100), nullable=False)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)
    json_data = db.Column(db.JSON, nullable=False)
    timestamp = db.Column(db.Integer, nullable=False)
