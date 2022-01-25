# api/__init__.py

import json
import time
from collections import OrderedDict

from flask import jsonify, render_template, request
from flask_cors import CORS, cross_origin

# import original moduels
from stip import app
from stip.api.Topic import Topic
from stip.api.Data import Data
from stip.api.TopicManagement import TopicManagement
from stip.api.DataManagement import DataManagement
from stip.api.PublishControl import PublishControl


# Class変数として利用するモジュールのインスタンスを作っておく
# ここにでインスタンス化するものはモジュール内にself変数を持たない
topic_management = TopicManagement()
data_management = DataManagement()
publish_control = PublishControl()

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
    return "topic: {0} Created!!".format(topic.topic_name)
  else:
    return "topic Created! But Set Elements Error!!"

@app.route('/publish/post', methods=['POST'])
def dataPost():
  post_data = request.get_json()
  if not (post_data.keys() >= {'Publisher', 'TopicName', 'Elements'}):
    return 'Not Found Publisher or Topic or Elements'

  # 送信先の対象トピックがstip上に存在するか確認する (TopicManagement.py)
  if not (topic_management.topicExistCheck(post_data['TopicName'], post_data['Publisher'])):
    return "Does Not Exist Publisher or Target Topic!"
  
  data = Data()
  data.setDataParameters(post_data)
  result = publish_control.publishDirectly(data)
  if not result: return "Exeception Error! Publish Failed"
  result = data_management.insertToDataValue(data)
  if result:
    return "topic:"

  # 位置情報を用いる場合，ここで空間情報検索したものの送信を行う処理を書く (PublishControl.py)
  if result: 
    return "topic: {0} Published!!".format(data.topic_name)
  else:
    return "Published! But Insert Record to the Database Error!!"

  # postされた情報を時間及び時空間情報処理によって送信制御するためにデータをストアしておく処理を書く (DataManagement.py)