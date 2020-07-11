""" Entry and Exit point of application - Application layer"""

from flask import Flask
from bikeshare.views.index import bp as index_bp

app = Flask(__name__)

app.register_blueprint(index_bp)
