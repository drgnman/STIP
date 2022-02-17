import json
import re

from stip.utils.DBUtil import DBUtil

class SubscriberManagement:
    def __init__(self):
        pass

    def registerSubscriber(self, subscriber):
        db = DBUtil()
        db.createDBConnection()
        sql = 'INSERT IGNORE INTO SUBSCRIBERS (SUBSCRIBER, LATITUDE, LONGITUDE, SPEED, DIRECTION) \
            VALUES ("{0}", {1}, {2}, "{3}", "{4}");'.format(
                    subscriber.subscriber_name,
                    subscriber.latitude,
                    subscriber.longitude,
                    subscriber.speed,
                    subscriber.direction 
                )
        result = db.executeQuery(sql)
        db.closeDBConnection()
        return result
    
    # Subscriberクラスを拡張して，そこに"登録用の"SubscriberTopicパラメータを持たせることにした
    def registerSubscriberTopic(self, subscriber):
        db = DBUtil()
        db.createDBConnection()
        # TopicNameが固定の名称である前提
        # 周期配信の場合はDetectionRangeは不要
        if (subscriber.control_mode == "Periodic"):
            sql = 'INSERT IGNORE INTO SUBSCRIBER_TOPICS \
                    (SUBSCRIBER_TOPIC, TOPIC_LIST, EXTRACTED_TOPIC_LIST, \
                        PM_FLAG, RECEIVE_FREQUENCY) VALUES \
                    ("{0}", "{1}", "{2}" , "{3}", "{4}");'.format(
                        subscriber.subscriber_name + "_" +subscriber.purpose, 
                        subscriber.topic_list, 
                        '',
                        subscriber.control_mode,
                        subscriber.receive_frequency
                    )
        elif (subscriber.control_mode == "Aggregation"):
            topic_name_list = list(subscriber.topic_list.keys())
            sql = 'INSERT IGNORE INTO SUBSCRIBER_TOPICS \
                    (SUBSCRIBER_TOPIC, TOPIC_LIST, EXTRACTED_TOPIC_LIST, PROCEDURE_LIST, \
                        PM_FLAG, RECEIVE_FREQUENCY, DATA_TTR) VALUES \
                    ("{0}", "{1}", "{2}" , \'{3}\', "{4}", "{5}", "{6}");'.format(
                        subscriber.subscriber_name + "_" +subscriber.purpose, 
                        topic_name_list, 
                        topic_name_list,
                        json.dumps(subscriber.topic_list),
                        subscriber.control_mode,
                        subscriber.receive_frequency,
                        subscriber.data_ttr
                    )
        elif(subscriber.control_mode == "Dynamic"):
            # それ以外の場合にはDetectionRangeも設定
            sql = 'INSERT IGNORE INTO SUBSCRIBER_TOPICS \
                    (SUBSCRIBER_TOPIC, TOPIC_LIST, EXTRACTED_TOPIC_LIST, \
                        PM_FLAG, DETECTION_RANGE) VALUES \
                    ("{0}", "{1}", "{2}" , "{3}", "{4}");'.format(
                        subscriber.subscriber_name + "_" + subscriber.purpose, 
                        subscriber.topic_list,
                        '',
                        subscriber.control_mode,
                        subscriber.detection_range
                    )
        elif(subscriber.control_mode == "Periodic_Dynamic"):
            # それ以外の場合にはDetectionRangeも設定
            # (Aggregation Dynamic?)
            sql = 'INSERT IGNORE INTO SUBSCRIBER_TOPICS \
                    (SUBSCRIBER_TOPIC, TOPIC_LIST, EXTRACTED_TOPIC_LIST, \
                        PM_FLAG, RECEIVE_FREQUENCY, DATA_TTR, MOVING_INFORMATION_LIST, DETECTION_RANGE) VALUES \
                    ("{0}", "{1}", "{2}" , "{3}", "{4}", "{5}", \'{6}\', "{7}");'.format(
                        subscriber.subscriber_name + "_" + subscriber.purpose, 
                        subscriber.topic_list,
                        '',
                        subscriber.control_mode,
                        subscriber.receive_frequency,
                        subscriber.data_ttr,
                        json.dumps(subscriber.moving_information_list),
                        subscriber.detection_range
                    )

        print(sql)
        result = db.executeQuery(sql)
        db.closeDBConnection()
        return result