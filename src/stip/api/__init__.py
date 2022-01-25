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
  if not (create_topic_request.keys() >= {'Publisher', 'TopicName', 'Elements'}):
    return 'Not Found Publisher or Topic or Elements'

  # Topic Createメソッドの呼び出し
  topic = Topic()
  topic.setTopicParameters(create_topic_request)
  # Topicテーブルに対象のトピックレコードを追加
  result = topic_management.topicCreate(topic)
  if not result: return "Create Topic Error!"
  result = topic_management.elementsSet(topic)
  if result: 
    return "topic: {0} created!!".format(topic.topic_name)
  else:
    return "Set Elements Error!!"

@app.route('/publish/post', methods=['POST'])
def dataPost():
  request_data = request.get_json()
  if not (request_data.keys() >= {'Publisher', 'TopicName', 'Elements'}):
    return 'Not Found Publisher or Topic or Elements'

  # 送信先の対象トピックがstip上に存在するか確認する (TopicManagement.py)
  # 位置情報を用いる場合，ここで空間情報検索したものの送信を行う処理を書く (PublishControl.py)
  # postされた情報を時間及び時空間情報処理によって送信制御するためにデータをストアしておく処理を書く (DataManagement.py)