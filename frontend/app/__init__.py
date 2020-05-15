from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'applesauce'

login = LoginManager(__name__)

from app import routes
