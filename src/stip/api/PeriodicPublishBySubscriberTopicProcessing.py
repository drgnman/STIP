import re
from datetime import datetime
import json
from stip.api.objects.Data import Data
from stip.api import ProcedureProcessing
from stip.utils.DBUtil import DBUtil
from stip.api.PeriodicControl import PeriodicControl
from stip.api.PublishControl import PublishControl
from stip.api.common.CommonStrings import CommonStrings
from stip.api.objects.SubscriberTopic import SubscriberTopic
from stip.api.ProcedureProcessing import ProcedureProcessing
from stip.utils.ProccessingSupports import ProcessingSupports

class PeriodicPublishBySubscriberTopicProcessing:
    def __init__(self):
        self.db = DBUtil()
        self.procedureProcessing = ProcedureProcessing()
        self.periodic_control = PeriodicControl()
        self.publish_control = PublishControl()
        self.processing_supports = ProcessingSupports()
        self.common_strings = CommonStrings()

    def PublishBySubscriberTopic(self):
        self.db.createDBConnection()
        sql = 'SELECT * FROM SUBSCRIBER_TOPICS;'
        all_subscriber_topic_list = self.db.fetchAllQuery(sql)
        self.db.closeDBConnection()
        result = None
        for record in all_subscriber_topic_list:
            subscriber_topic = SubscriberTopic()
            subscriber_topic.setParameterFromList(record)
            publish_contents = {}
            if subscriber_topic.control_mode == self.common_strings.DYNAMIC:
                continue
            if not (self.periodic_control.judgeToPublishTarget(subscriber_topic.receive_frequency, subscriber_topic.create_timestamp)):
                continue
            if (subscriber_topic.control_mode == self.common_strings.PERIODIC):
                publish_contents = self.publishForModePeriodic(subscriber_topic)
                print(publish_contents)
            elif (subscriber_topic.control_mode == self.common_strings.AGGREGATION):
                publish_contents = self.publishForModePeriodicAggregation(subscriber_topic)
                print(publish_contents)
            elif (subscriber_topic.control_mode == self.common_strings.PERIODIC_AND_DYNAMIC):
                publish_contents = self.publishForModePeriodicAndDynamic(subscriber_topic)
                print(publish_contents)

            if (publish_contents == {}): continue
            # 完成したデータとトピック名をDataオブジェクトに格納してIoTプラットフォームにPublish
            publish_data = Data()
            publish_data.topic_name = subscriber_topic.subscriber_topic_name
            publish_data.element_values = publish_contents
            # 今今は各レコード単位で送信処理してるけど，まとめて最後にpublishした方がいいか？
            result = self.publish_control.publishDirectly(publish_data)
        return result

    # aggegationを含まないシンプルな送信制御モード
    def publishForModePeriodic(self, subscriber_topic):
        topic_list = subscriber_topic.topic_list[1:-1]
        topic_list = self.processing_supports.convertFromStrToList(topic_list)
        publish_contents = self.getDataValueFromDatabaseByTopicList(topic_list)
        return publish_contents
        

    # 位置情報を用いた送信制御モード
    def publishForModePeriodicAndDynamic(self, subscriber_topic):
        # 送信周期が一致しているものに対しての処理
        now_unixtime = datetime.now().timestamp()
        start_unixtime = subscriber_topic.create_timestamp.timestamp()
        elapsed_time = now_unixtime - start_unixtime
        elapsed_duration, sum_duration, skip_counter = 0.0, 0.0, 0 # (単位は秒の前提)
        # durationと経過時間を見てどこまでスキップするかを決める
        # subscriber_topic.moving_information_list = 
        subscriber_topic.moving_information_list = json.loads(subscriber_topic.moving_information_list)
        for i in range(skip_counter, len(subscriber_topic.moving_information_list)):
            elapsed_duration += float(subscriber_topic.moving_information_list[i][self.common_strings.WAYPOINT][self.common_strings.DURATION])
            if (elapsed_duration > elapsed_time):
                break
            skip_counter += 1
        
        receive_frequency = subscriber_topic.receive_frequency.split()
        receive_period = int(receive_frequency[0]) * 60
        publish_topic_list = []
        organized_extracted_topic_list = subscriber_topic.extracted_topic_list.split("],")
        for i in range(len(organized_extracted_topic_list)):
            organized_extracted_topic_list[i] = organized_extracted_topic_list[i].replace("[", "").replace("]", "")
            organized_extracted_topic_list[i] =organized_extracted_topic_list[i].split(",")

        # subscriber_topic.extracted_topic_list 
        for i in range(len(subscriber_topic.moving_information_list)):
            for topic_name in organized_extracted_topic_list[i]:
                publish_topic_list.append(topic_name)
            sum_duration += subscriber_topic.moving_information_list[i][self.common_strings.WAYPOINT][self.common_strings.DURATION]
            if (sum_duration > receive_period):
                break

        # 送信対象の範囲を整理する(extracted_topic_list)から今回の送信で送る分を判断する
        publish_topic_list = list(dict.fromkeys(publish_topic_list))
        publish_contents = self.getDataValueFromDatabaseByTopicList(publish_topic_list)
        return publish_contents

    # aggregationを用いた送信制御モード
    def publishForModePeriodicAggregation(self, subscriber_topic):
        publish_contents = {}
        for topic_name in subscriber_topic.procedure_list:
            procedure = subscriber_topic.procedure_list[topic_name][self.common_strings.PROCEDURE]
            if (self.common_strings.VARIABLE_LIST in subscriber_topic.procedure_list[topic_name]):
                variable_list = subscriber_topic.procedure_list[topic_name][self.common_strings.VARIABLE_LIST]
            operators = self.procedureProcessing.procedureSplit(procedure)
            for operator in operators:
                # operatorを参考に計算する箇所の切り出し
                target_formula = self.procedureProcessing.extractTargetFormulaPart(
                    operator, procedure
                    )
                # 切り出した要素から計算及び，元テキスト書き換えのための要素取り出し
                if (operator != self.common_strings.HOT):
                    rewrite_elements = self.procedureProcessing.splitEachElementFromTargetFormula(
                        target_formula, subscriber_topic.value_list)  # 要素数0~2の配列が返ってくる
                else:
                    rewrite_elements = target_formula

                # 計算処理
                processingResult = self.procedureProcessing.calcurateFromProcedure(
                    operator, rewrite_elements
                    )
                # 結果を用いてprocedure本体を書き換える
                procedure = self.rewriteProcedureByCulculatedResult(
                    operator, procedure, target_formula, processingResult 
                    )
            publish_contents[topic_name] = [procedure, str(datetime.now())]
        return publish_contents
        
    def rewriteProcedureByCulculatedResult(self, operator, procedure, target_formula, result):
        replace_target = "{0}({1})".format(operator, target_formula)
        # 文章と値をそれぞれ逆転文字列化して, 置き換えをした後にもう一度反転して元に戻す
        return procedure[::-1].replace(replace_target[::-1], str(result)[::-1], 1)[::-1]

    def getDataValueFromDatabaseByTopicList(self, topic_list):
        publish_contents = {}
        self.db.createDBConnection()
        for topic_name in topic_list:
            print(topic_name)
            sql = 'SELECT TOPIC_NAME, ELEMENT_VALUE, PUBLISH_TIMESTAMP \
                    FROM DATA_VALUE_TEMP WHERE TOPIC_NAME = "{0}" ORDER BY PUBLISH_TIMESTAMP DESC LIMIT 1;'.format(
                        topic_name
                    )
            print(sql)
            result_set = self.db.fetchAllQuery(sql)
            print(result_set)
            if (result_set != []):
                publish_contents[topic_name] = result_set[0]
        self.db.closeDBConnection()
        return publish_contents
