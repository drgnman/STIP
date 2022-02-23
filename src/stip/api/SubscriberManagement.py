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
            math_operator = MathOperator()
            processing_supports = ProcessingSupports()

            # 名前から対象となるtopic群を取り出しておく
            pre_topic_list = []
            for topic in subscriber.topic_list:
                sql = 'SELECT TOPIC_NAME, LATITUDE, LONGITUDE FROM TOPIC WHERE TOPIC_NAME LIKE "%\_{0}";'.format(topic)
                result_set = db.fetchAllQuery(sql)
                for result in result_set:
                    pre_topic_list.append(result)

            for i in range(len(subscriber.moving_information_list)):
                if (i==0):
                    latitude, longitude = subscriber.latitude, subscriber.longitude
                    next_point = subscriber.moving_information_list[i]

                elif (i+1 >= len(subscriber.moving_information_list)):
                    next_latitude, next_longitude = 0.0, 0.0 

                else:
                    point = subscriber.moving_information_list[i]
                    latitude, longitude = point[self.common_strings.GEOMETORY][self.common_strings.LATLNG].split(',')
                    next_point = subscriber.moving_information_list[i+1]

                next_latitude, next_longitude = next_point[self.common_strings.GEOMETORY][self.common_strings.LATLNG].split(',')
                latitude, longitude, next_latitude, next_longitude = float(latitude), float(longitude), float(next_latitude), float(next_longitude) 


                if (not(i+1 >= len(subscriber.moving_information_list))):
                    distance = math_operator.calculateGeoInformation(
                        latitude, longitude, next_latitude, next_longitude, self.common_strings.GIS_DISTANCE)
                    if (subscriber.detection_range < distance):
                        extracted_topic_list_parts = []
                        tmp_latitude, tmp_longitude = 0.0, 0.0
                        latitude_over_flag, longitude_over_flag = False, False
                        while (not latitude_over_flag or not longitude_over_flag):
                            if (tmp_latitude > 0.0 and tmp_longitude > 0.0):
                                azimuth = math_operator.calculateGeoInformation(
                                    tmp_latitude, tmp_longitude, next_latitude, next_longitude, self.common_strings.GIS_AZIMUTH 
                                )
                                tmp_latitude, tmp_longitude = math_operator.estimateDestination(
                                    tmp_latitude, tmp_longitude, azimuth, (subscriber.detection_range)
                                )

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
                                latitude_over_flag = True
                            else:
                                # (destination_x < tmp_x < current_x)
                                # (tmp_x < destinaion_x)の時だけ，tmp_x = destination_xとする
                                tmp_latitude = processing_supports.nextLatitudeSmallerThanCurrentLatitude(tmp_latitude, next_latitude)
                                latitude_over_flag = True
                            # (current_y < destination_y)
                            if (longitude < next_longitude):
                                # (destination_y < tmp_y)の時だけ，tmp_y = destination_yとする
                                tmp_longitude = processing_supports.nextLongitudeLagerThanCurrentLongitude(tmp_longitude, next_longitude)
                                longitude_over_flag = True
                            # (destination_y < current_y)
                            else:
                                # (tmp_y < destination_y)の時だけ，tmp_y = destination_yとする
                                tmp_longitude = processing_supports.nextLongitudeSmallerThanCurrentLongitude(tmp_longitude, next_longitude)
                                longitude_over_flag = True
                            # detection処理
                            # extracted_topic_listへの要素追加
                            for target_topic_name in subscriber.topic_list:
                                for topic in pre_topic_list:
                                    result = processing_supports.compareDistanceDuaringSubscriberAndTopic(
                                        target_topic_name, topic[0], tmp_latitude, tmp_longitude, float(topic[1]), float(topic[2]), subscriber.detection_range
                                    )
                                    if result:
                                        extracted_topic_list_parts.append(topic[0])
                        extracted_topic_list_parts = list(dict.fromkeys(extracted_topic_list_parts))
                        extracted_topic_list_parts = "["+",".join(map(str, extracted_topic_list_parts))+"]"
                        subscriber.extracted_topic_list += extracted_topic_list_parts + ","

                    else:
                        extracted_topic_list_parts = []
                        for target_topic_name in subscriber.topic_list:
                            for topic in pre_topic_list:
                                result = processing_supports.compareDistanceDuaringSubscriberAndTopic(
                                    target_topic_name, topic[0], latitude, longitude, float(topic[1]), float(topic[2]), subscriber.detection_range)
                                if result:
                                    extracted_topic_list_parts.append(topic[0])
                        extracted_topic_list_parts = list(dict.fromkeys(extracted_topic_list_parts))
                        extracted_topic_list_parts = "["+",".join(map(str, extracted_topic_list_parts))+"]"
                        subscriber.extracted_topic_list += extracted_topic_list_parts + ","
                else:
                    extracted_topic_list_parts = []
                    for target_topic_name in subscriber.topic_list:
                        for topic in pre_topic_list:
                                result = processing_supports.compareDistanceDuaringSubscriberAndTopic(
                                    target_topic_name, topic[0], latitude, longitude, float(topic[1]), float(topic[2]), subscriber.detection_range)
                                if result:
                                    extracted_topic_list_parts.append(topic[0])
                    extracted_topic_list_parts = list(dict.fromkeys(extracted_topic_list_parts))
                    extracted_topic_list_parts = "["+",".join(map(str, extracted_topic_list_parts))+"]"
                    subscriber.extracted_topic_list += extracted_topic_list_parts

            print(subscriber.extracted_topic_list)

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

        result = db.executeQuery(sql)
        db.closeDBConnection()
        return result