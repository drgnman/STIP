# api/__init__.py

import json
import time
from collections import OrderedDict

from flask import jsonify, render_template, request
from flask_cors import CORS, cross_origin

# import original moduels
from stip import app
# Class Object 
from stip.api.objects.Topic import Topic
from stip.api.objects.Data import Data
from stip.api.objects.Subscriber import Subscriber
from stip.api.objects.SubscriberTopic import SubscriberTopic
from stip.api.common.CommonStrings import CommonStrings
# Processing Module
from stip.api.TopicManagement import TopicManagement
from stip.api.DataManagement import DataManagement
from stip.api.PublishControl import PublishControl
from stip.api.SubscriberManagement import SubscriberManagement


# Class変数として利用するモジュールのインスタンスを作っておく
# ここにでインスタンス化するものはモジュール内にself変数を持たない
topic_management = TopicManagement()
data_management = DataManagement()
publish_control = PublishControl()
subscriber_management = SubscriberManagement()
common_strings = CommonStrings()


@app.route('/')
def helloWorld():
  return "Hello World"

@app.route('/publish/create', methods=["POST"])
def topicCeate():
  create_topic_request = request.get_json()
  if not (create_topic_request.keys() >= {common_strings.PUBLISHER, common_strings.TOPIC_NAME, common_strings.ELEMENTS}):
    return 'Not Found Publisher or Topic or Elements'

  topic = Topic()
  topic.setParameters(create_topic_request)

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
  if not (post_data.keys() >= {common_strings.PUBLISHER, common_strings.TOPIC_NAME, common_strings.ELEMENTS}):
    return 'Not Found Publisher or Topic or Elements'

  # 送信先の対象トピックがstip上に存在するか確認する (TopicManagement.py)
  if not (topic_management.topicExistCheck(post_data[common_strings.TOPIC_NAME], post_data[common_strings.PUBLISHER])):
    return "Does Not Exist Publisher or Target Topic!"
  
  data = Data()
  data.setParameters(post_data)
  # 最終的に送信する中身はelements_valueだけ(topicは宛先指定に使われる),
  # サブスクライバがなんのデータかわかるようにelements_valueにTopicNameデータを追加する
  data.element_values[common_strings.TOPIC_NAME] = data.topic_name
  result = publish_control.publishDirectly(data)
  # 位置情報を用いる場合，ここで空間情報検索したものの送信を行う処理を書く (PublishControl.py)
  result = publish_control.publishByDynamicTopicOptimization(data)
  if not result: return "Exeception Error! Publish Failed"

  # DATA_VALUESテーブルへの追加
  result = data_management.insertToDataValue(data)
  # SUBSCRIBER_TOPICSテーブルへの追加
  # postされた情報を時間及び時空間情報処理によって送信制御するためにデータをストアしておく処理を書く (DataManagement.py)
  result = data_management.insertToSubscriberTopic(data)
  if result: 
    return "topic: {0} Published!!".format(data.topic_name)
  else:
    return "Published! But Insert Record to the Database Error!!"

@app.route('/subscribe/register', methods=['POST'])
def registerSubscriber():
  request_subscriber = request.get_json()
  # Subscriberとして最低限必要な要素のキーチェック
  if not (request_subscriber.keys() >= {common_strings.SUBSCRIBER_NAME, common_strings.PURPOSE, common_strings.CONTROL_MODE}):
    return 'Not Found SubscriberName or Purpose'
  subscriber = Subscriber()
  # Subscriber情報の設定
  subscriber.setParameters(request_subscriber) 
  # Subscriberの重複チェック -> 存在してた場合は登録しない 
  # 他のユーザが同じ名前で登録しようとしてるかはわからない -> Skip
  result = subscriber_management.registerSubscriber(subscriber)
  if not result: return "Failed! Subscrbier Cann't Register"

  # SubscribeTopic情報の設定
  subscriber.setSubscriberTopicParameters(request_subscriber)
  result = subscriber_management.registerSubscriberTopic(subscriber)

  return "Success"


  # Subscriberの登録

  # Subscriber-topicの登録