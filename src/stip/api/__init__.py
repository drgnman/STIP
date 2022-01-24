# api/__init__.py

import json
import time
from collections import OrderedDict

from flask import jsonify, render_template, request
from flask_cors import CORS, cross_origin

# import original moduels
from stip import app


# Class変数として利用するモジュールのインスタンスを作っておく
# Topic = TopciCreate()

@app.route('/')
def helloWorld():
  return "Hello World"

@app.route('/publish/create', methods=["POST"])
def topicCeate():
  topic = request.get_json()
  try:
    if not (topic.keys() >= {'publisher', 'name', 'elements'}):
      return 'Not Found Publisher or Name or Elements'

    # Topic Createメソッドの呼び出し
