from stip.utils.DBUtil import DBUtil
from stip.utils.ProccessingSupports import ProcessingSupports
from stip.utils.MathOperator import MathOperator
from stip.utils.ProccessingSupports import ProcessingSupports
from stip.api.common.CommonStrings import CommonStrings
from stip.api.objects.BaseTopicForDTOS import  BaseTopicForDTOS
from stip.api.PublishToPlatforms import PublishToAMQP, PublishToMQTT
from stip.api.objects.SubscriberTopic import SubscriberTopic
from stip.api.objects.Subscriber import Subscriber
from stip.api.objects.Data import Data
from datetime import datetime

class PublishControl:
    def __init__(self):
        self.common_strings = CommonStrings()
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
        if (iot_type == self.common_strings.AMQP):
            return self.publishToAQMP(data)
        elif (iot_type == self.common_strings.MQTT):
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
            distance = self.math_operator.calculateGeoInformation(
                base_topic.latitude, base_topic.longitude, subscriber[1], subscriber[2], self.common_strings.GIS_DISTANCE)
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
        db.closeDBConnection() 
        # print(target_subscribers)
        for target in target_subscribers:
            # 送信する先のtopic_name = Subscriber_topicを意味する
            data.topic_name = target
            self.publishDirectly(data)
        
        return True 

    def publishWhenUpdateSubscriber(self, subscriber):
        db = DBUtil()
        db.createDBConnection()
        sql = 'SELECT SUBSCRIBER_TOPIC, TOPIC_LIST, DETECTION_RANGE FROM SUBSCRIBER_TOPICS WHERE SUBSCRIBER_TOPIC LIKE "{0}\_%"'.format(subscriber.subscriber_name)
        subscriber_topic_list = db.fetchAllQuery(sql)
        publish_dataset = []
        for result in subscriber_topic_list:
            subscriber_topic = SubscriberTopic()
            subscriber_topic.subscriber_topic_name = result[0]
            subscriber_topic.topic_list = self.processing_supports.convertFromStrToList(result[1][1:-1])
            subscriber_topic.detection_range = result[2]
            target_topic_list = []
            contents_list = []
            for topic in subscriber_topic.topic_list:
                sql =  'SELECT TOPIC_NAME, LATITUDE, LONGITUDE, EFFECTIVE_RANGE, DATA_TTL FROM TOPIC WHERE TOPIC_NAME LIKE "%\_{0}" \
                   HAVING (6371 * acos(cos(radians({1})) * cos(radians(LATITUDE)) * cos(radians(LONGITUDE) - radians({2})) + sin(radians({1})) * sin(radians(LATITUDE)))) <= {3}'.format(
                       topic, subscriber.latitude, subscriber.longitude, subscriber_topic.detection_range)
                result_topic_list = db.fetchAllQuery(sql)
                if (result_topic_list == []):
                    continue
                for result_topic in result_topic_list:
                    target_topic_list.append(result_topic)
        
            # ここのfor文が間違っているのを直す
            for topic in target_topic_list:
                sql = 'SELECT TOPIC_NAME, ELEMENT_NAME, VALUE, PUBLISH_TIMESTAMP FROM DATA_VALUE WHERE TOPIC_NAME="{0}"'.format(topic[0])
                topic_index_result = db.fetchAllQuery(sql)
                if (topic_index_result == []):
                    continue
                topic_index_result = topic_index_result[0]
                data_ttl = float(topic[4]) + topic_index_result[3].timestamp()
                data_part = {}
                data_list = {}
                if (',' in topic_index_result[1]):
                    elements_list = topic_index_result[1].split(',')
                    rawValue_list = topic_index_result[2].split(',')
                    for i in range(0, len(elements_list)):
                        data_list[elements_list[i]] = rawValue_list[i]
                else:
                    data_list[topic_index_result[1]] = topic_index_result[2]

                data_part = {self.common_strings.TOPIC: topic_index_result[0], self.common_strings.ELEMENTS:data_list, 
                    self.common_strings.PUBLISH_TIMESTAMP:str(topic_index_result[3]),
                    self.common_strings.DATA_TTL: str(data_ttl), self.common_strings.EFFECTIVE_RANGE: str(topic[4]),
                    self.common_strings.LONGITUDE: topic[1], self.common_strings.LATITUDE: topic[2]}
                contents_list.append(data_part)

            data = Data()
            data.topic_name = subscriber_topic.subscriber_topic_name
            data.element_values = contents_list
            publish_dataset.append(data)

        for content in publish_dataset:
            print("content: ", content.topic_name, content.element_values)
            # resultがFalse帰ってきた場合，どうするか考えたほうがいい?
            result = self.publishDirectly(content)

        return True