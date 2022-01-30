from os import openpty
from stip.api import ProcedureProcessing
from stip.utils.DBUtil import DBUtil
from stip.api.PeriodicControl import PeriodicControl
from stip.api.PublishControl import PublishControl
from stip.api.SubscriberTopic import SubscriberTopic
from stip.api.ProcedureProcessing import ProcedureProcessing

class PeriodicPublishBySubscriberTopic:
    periodic_control = PeriodicControl()
    def __init__(self):
        self.procedureProcessing = ProcedureProcessing()

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
            # 集計処理及び
            # パブリッシュの処理を書いていく
            for topic_name in subscriber_topic.procedure_list:
                procedure = subscriber_topic.procedure_list[topic_name]['Procedure']
                if ("VariableList" in subscriber_topic.procedure_list[topic_name]):
                    variable_list = subscriber_topic.procedure_list[topic_name]['VariableList']
                operators = self.procedureProcessing.procedureSplit(procedure)
                for operator in operators:
                    print("operator: ", operator)
                    # operatorを参考に計算する箇所の切り出し
                    print("procedure:", procedure)
                    target_formula = self.procedureProcessing.extractTargetFormulaPart(
                        operator, procedure
                        )
                    # 切り出した要素から計算及び，元テキスト書き換えのための要素取り出し
                    if (operator != "Hot"):
                        rewrite_elements = self.procedureProcessing.splitEachElementFromTargetFormula(
                            target_formula, subscriber_topic.value_list)  # 要素数0~2の配列が返ってくる
                    else:
                        rewrite_elements = target_formula

                    print("rewrite_elements: ", rewrite_elements)
                    # 計算処理
                    processingResult = self.procedureProcessing.calcurateFromProcedure(
                        operator, rewrite_elements
                        )
                    print("processing result: ", processingResult)
                    # 結果を用いてprocedure本体を書き換える
                    procedure = self.rewriteProcedureByCulculatedResult(
                        operator, procedure, target_formula, processingResult 
                        )

    def rewriteProcedureByCulculatedResult(self, operator, procedure, target_formula, result):
        replace_target = "{0}({1})".format(operator, target_formula)
        # 文章と値をそれぞれ逆転文字列化して, 置き換えをした後にもう一度反転して元に戻す
        return procedure[::-1].replace(replace_target[::-1], str(result)[::-1], 1)[::-1]