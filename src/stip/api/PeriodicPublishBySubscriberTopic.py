from datetime import datetime
from stip.api.Data import Data
from stip.api import ProcedureProcessing
from stip.utils.DBUtil import DBUtil
from stip.api.PeriodicControl import PeriodicControl
from stip.api.PublishControl import PublishControl
from stip.api.SubscriberTopic import SubscriberTopic
from stip.api.ProcedureProcessing import ProcedureProcessing

class PeriodicPublishBySubscriberTopic:
    def __init__(self):
        self.procedureProcessing = ProcedureProcessing()
        self.periodic_control = PeriodicControl()
        self.publish_control = PublishControl()

    def PublishBySubscriberTopic(self):
        db = DBUtil()
        db.createDBConnection()
        sql = 'SELECT * FROM SUBSCRIBER_TOPICS;'
        all_subscriber_topic_list = db.fetchAllQuery(sql)

        for record in all_subscriber_topic_list:
            subscriber_topic = SubscriberTopic()
            subscriber_topic.setParameterFromList(record)
            if not (self.periodic_control.judgeToPublishTarget(subscriber_topic.receive_frequency, subscriber_topic.create_timestamp)):
                continue
            if (subscriber_topic.control_mode == "Aggregation"):
                result = self.publishForModePeriodicAggregation(subscriber_topic)
                print(result)
            # パブリッシュの処理を書いていく
            # ここに最後パブリッシュ内容をまとめて，最後にパブリッシュ

            # Procedureに記載された処理の実行


    def publishForModePeriodicAggregation(self, subscriber_topic):
        publish_contents = {}
        for topic_name in subscriber_topic.procedure_list:
            procedure = subscriber_topic.procedure_list[topic_name]['Procedure']
            if ("VariableList" in subscriber_topic.procedure_list[topic_name]):
                variable_list = subscriber_topic.procedure_list[topic_name]['VariableList']
            operators = self.procedureProcessing.procedureSplit(procedure)
            for operator in operators:
                # operatorを参考に計算する箇所の切り出し
                target_formula = self.procedureProcessing.extractTargetFormulaPart(
                    operator, procedure
                    )
                # 切り出した要素から計算及び，元テキスト書き換えのための要素取り出し
                if (operator != "Hot"):
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
        
        # 完成したデータとトピック名をDataオブジェクトに格納してIoTプラットフォームにPublish
        publish_data = Data()
        publish_data.topic_name = subscriber_topic.subscriber_topic_name
        publish_data.element_values = publish_contents
        print(publish_data.element_values)

        result = self.publish_control.publishDirectly(publish_data)
        return result

    def rewriteProcedureByCulculatedResult(self, operator, procedure, target_formula, result):
        replace_target = "{0}({1})".format(operator, target_formula)
        # 文章と値をそれぞれ逆転文字列化して, 置き換えをした後にもう一度反転して元に戻す
        return procedure[::-1].replace(replace_target[::-1], str(result)[::-1], 1)[::-1]