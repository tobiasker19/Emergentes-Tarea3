from flask import Flask
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

import routes  # Asegúrate de que esto esté al final para que las rutas se importen después de inicializar la app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
