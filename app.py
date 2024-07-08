from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
