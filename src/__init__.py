from flask import Flask
from flask_cors import CORS

def createApp():
  app = Flask(__name__)
  app.config['JSON_SORT_KEYS'] = False
  return app

app = createApp()
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

from . import api
