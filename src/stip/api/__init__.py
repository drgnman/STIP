# api/__init__.py

import json
import time
from collections import OrderedDict

from flask import jsonify, render_template, request
from flask_cors import CORS, cross_origin

# import original moduels
from stip import app
from stip.api.Topic import Topic
from stip.api.TopicManagement import TopicManagement


# Class変数として利用するモジュールのインスタンスを作っておく
# ここにでインスタンス化するものはモジュール内にself変数を持たない
topic_management = TopicManagement()

@app.route('/')
def helloWorld():
  return "Hello World"

@app.route('/publish/create', methods=["POST"])
def topicCeate():
  create_topic_request = request.get_json()
  if not (create_topic_request.keys() >= {'publisher', 'name', 'elements'}):
    return 'Not Found Publisher or Name or Elements'

  # Topic Createメソッドの呼び出し
  topic = Topic()
  topic.setTopicParameters(create_topic_request)
  # Topicテーブルに対象のトピックレコードを追加
  result = topic_management.topicCreate(topic)
  if not result: return "Create Topic Error!"
  result = topic_management.elementsSet(topic)
  if result: 
    return "topic: {0} created!!".format(topic.name)
  else:
    return "Set Elements Error!!"
