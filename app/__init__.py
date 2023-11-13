import os
import logging
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from logging.handlers import RotatingFileHandler

load_dotenv()

db = SQLAlchemy()

# Logging configuration
log_filename = "run.log"
log_max_size = 1 * 1024 * 1024  # 1 MB

# Create a logger
logger = logging.getLogger("python")
logger.setLevel(logging.DEBUG)

# Create a file handler with log rotation
handler = RotatingFileHandler(log_filename, maxBytes=log_max_size, backupCount=5)

# Create a formatter
formatter = logging.Formatter("%(asctime)s [%(levelname)s] - %(message)s")
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("MYSQL_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .main.routes import main

    app.register_blueprint(main)

    return app
