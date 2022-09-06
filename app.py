from flask import Flask
from flask_pymongo import PyMongo
import sys

app = Flask(__name__)
app.config.from_pyfile('config.py')
sys.dont_write_bytecode = True

mongo = PyMongo(app)