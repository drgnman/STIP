from stip.utils.DBUtil import DBUtil
from stip.utils.ProccessingSupports import ProcessingSupports
from stip.utils.MathOperator import MathOperator
from stip.utils.ProccessingSupports import ProcessingSupports
from stip.api.BaseTopicForDTOS import  BaseTopicForDTOS
from stip.api.PublishToPlatforms import PublishToAMQP, PublishToMQTT
from stip.api.SubscriberTopic import SubscriberTopic
from stip.api.Subscriber import Subscriber
from datetime import datetime

class PublishControl:
    def __init__(self):
        self.math_operator = MathOperator()
        self.processing_supports = ProcessingSupports()

    def publishToAQMP(self, data):
        try:
            publish_to_amqp = PublishToAMQP()
            connection, channel = publish_to_amqp.createConnection()
            publish_to_amqp.dataPublishToAMQP(channel, data)
            return True
        except Exception as e:
            print(e)
            return False

    def publishToMQTT(self, data):
        try: 
            publish_to_mqtt = PublishToMQTT()
            publish_to_mqtt.setConnection()
            publish_to_mqtt.dataPublishToMQTT(data)
            return True
        except Exception as e:
            print(e)
            return False

    def publishDirectly(self, data, iot_type="amqp"):
        if (iot_type == "amqp"):
            return self.publishToAQMP(data)
        elif (iot_type == "mqtt"):
            return self.publishToMQTT(data)
    
    def publishByDynamicTopicOptimization(self, data):
        db = DBUtil()
        db.createDBConnection()
        sql = 'SELECT TOPIC_NAME, LATITUDE, LONGITUDE, DATA_TTL, EFFECTIVE_RANGE \
                FROM TOPIC WHERE TOPIC_NAME = "{0}"'.format(data.topic_name)
        result = db.fetchAllQuery(sql)[0]

        base_topic = BaseTopicForDTOS()
        base_topic.setParameter(result)
        base_topic.data_ttl = base_topic.data_ttl + datetime.now().timestamp()

        sql = 'SELECT SUBSCRIBER, LATITUDE, LONGITUDE FROM SUBSCRIBERS;'
        all_subscribers = db.fetchAllQuery(sql)

        subscribers_distance_information_list = {} 
        for subscriber in all_subscribers:
            distance = self.math_operator.calculateDistance(
                base_topic.latitude, base_topic.longitude, subscriber[1], subscriber[2])
            # effective_rangeよりもdetection_rengeに収まっているかどうかが大事
            subscribers_distance_information_list[subscriber[0]] = distance
        
        target_subscribers = []
        publish_topic_category = data.topic_name.split("_")[-1]
        for subscriber, distance in subscribers_distance_information_list.items():
            # subscriber名の部分一致とPM_FLAG == "Dynamic" 
            # distance < detection_rangeを条件にSELECTクエリを発行すればいいのでは？
            sql = 'SELECT SUBSCRIBER_TOPIC, TOPIC_LIST FROM SUBSCRIBER_TOPICS WHERE \
                    PM_FLAG = "Dynamic" AND DETECTION_RANGE > {0} AND SUBSCRIBER_TOPIC LIKE "{1}\_%";'.format(
                        distance,
                        subscriber
                    )
            result_set = db.fetchAllQuery(sql)
            if result_set != []:
                if (len(result_set) > 0):
                    for result in result_set:
                        result = list(result)
                        # DBからの戻り値がtupleで中身は全てstr扱いのため，リストに変換する
                        topic_list = result[1][1:-1]
                        topic_list = self.processing_supports.convertFromStrToList(topic_list) 
                        # 完全一致検索
                        if (data.topic_name in topic_list):
                            # 送信先としてここで必要なのはSubscriber-topic名だけ
                            target_subscribers.append(result[0])
                        # 部分一致検索 topic名の末尾が種類を示すルールであることから，末尾から種類だけを切り取った 
                        elif (publish_topic_category in topic_list):
                            target_subscribers.append(result[0])

        
        # print(target_subscribers)
        for target in target_subscribers:
            # 送信する先のtopic_name = Subscriber_topicを意味する
            data.topic_name = target
            self.publishDirectly(data)
        
        return True 