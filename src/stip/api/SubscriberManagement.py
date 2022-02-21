import json
import re

from stip.api.common.CommonStrings import CommonStrings
from stip.utils.DBUtil import DBUtil
from stip.utils.MathOperator import MathOperator
from stip.utils.ProccessingSupports import ProcessingSupports

class SubscriberManagement:
    def __init__(self):
        self.common_strings = CommonStrings()

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
        if (subscriber.control_mode == self.common_strings.PERIODIC):
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
        elif (subscriber.control_mode == self.common_strings.AGGREGATION):
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

        elif (subscriber.control_mode == self.common_strings.DYNAMIC):
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

        elif (subscriber.control_mode == self.common_strings.PERIODIC_AND_DYNAMIC):
            # extracted_topic_listに抽出したトピック群を追加する処理を追加する
            extracted_topic_list = []
            latitude_list = []
            longitude_list = []
            math_operator = MathOperator()
            processing_supports = ProcessingSupports()
            for i in range(len(subscriber.moving_information_list)):
                if (i+1 >= len(subscriber.moving_information_list)):
                    break
                point = subscriber.moving_information_list[i]
                latitude, longitude = point[self.common_strings.GEOMETORY][self.common_strings.LATLNG].split(',')
                latitude = float(latitude)
                longitude = float(longitude) 
                next_point = subscriber.moving_information_list[i+1]
                next_latitude, next_longitude = next_point[self.common_strings.GEOMETORY][self.common_strings.LATLNG].split(',')
                next_latitude = float(next_latitude)
                next_longitude = float(next_longitude) 
                distance = math_operator.calculateGeoInformation(
                    latitude, longitude, next_latitude, next_longitude, self.common_strings.GIS_DISTANCE)
                if (distance < subscriber.detection_range):
                    pass
                    # sqlを発行する
                else:
                    azimuth = math_operator.calculateGeoInformation(
                        latitude, longitude, next_latitude, next_longitude, self.common_strings.GIS_AZIMUTH 
                    )
                    tmp_latitude, tmp_longitude = math_operator.estimateDestination(
                        latitude, longitude, azimuth, subscriber.detection_range
                    )

                if (latitude < next_latitude):
                    # (current_x < tmp_x < destination_x)
                    # (destinaion_x < tmp_x)の時だけ，tmp_x = destination_xとする
                    tmp_latitude = processing_supports.nextLatitudeLargerThanCurrentLatitude(tmp_latitude, next_latitude)
                else:
                    # (destination_x < tmp_x < current_x)
                    # (tmp_x < destinaion_x)の時だけ，tmp_x = destination_xとする
                    tmp_latitude = processing_supports.nextLatitudeSmallerThanCurrentLatitude(tmp_latitude, next_latitude)
                    # (current_y < destination_y)

                if (longitude < next_longitude):
                    # (destination_y < tmp_y)の時だけ，tmp_y = destination_yとする
                    tmp_longitude = processing_supports.nextLongitudeLagerThanCurrentLongitude(tmp_longitude, next_longitude)
                # (destination_y < current_y)
                else:
                    # (tmp_y < destination_y)の時だけ，tmp_y = destination_yとする
                    tmp_longitude = processing_supports.nextLongitudeSmallerThanCurrentLongitude(tmp_longitude, next_longitude)

                # detection処理を呼び出す

                sql = 'INSERT IGNORE INTO SUBSCRIBER_TOPICS \
                        (SUBSCRIBER_TOPIC, TOPIC_LIST, EXTRACTED_TOPIC_LIST, \
                            PM_FLAG, RECEIVE_FREQUENCY, DATA_TTR, MOVING_INFORMATION_LIST, DETECTION_RANGE) VALUES \
                        ("{0}", "{1}", "{2}" , "{3}", "{4}", "{5}", \'{6}\', "{7}");'.format(
                            subscriber.subscriber_name + "_" + subscriber.purpose, 
                            subscriber.topic_list,
                            subscriber.extracted_topic_list,
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