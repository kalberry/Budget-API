from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'applesauce'

from app import routes
