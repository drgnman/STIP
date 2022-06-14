from datetime import datetime
from inspect import CO_ASYNC_GENERATOR
import json
import ast

from pyrsistent import CheckedValueTypeError

from stip.api.common.CommonStrings import CommonStrings

from stip.utils.DBUtil import DBUtil
from stip.api.objects.SubscriberTopic import SubscriberTopic

class DataManagement:
    def __init__(self):
        self.common_strings = CommonStrings()

    def insertToDataValue(self, data):
        db = DBUtil()
        db.createDBConnection()

        # DataValueテーブルへのデータ追加
        sql = "INSERT IGNORE INTO DATA_VALUE_TEMP (TOPIC_NAME, ELEMENT_VALUE) VALUES ('{0}', '{1}');".format(
            data.topic_name, json.dumps(data.element_values)
        )
        result = db.executeQuery(sql)
        db.closeDBConnection()
        return result
    
    def insertToSubscriberTopic(self, data):
        db = DBUtil()
        db.createDBConnection()

        sql = 'SELECT SUBSCRIBER_TOPIC, PROCEDURE_LIST, VALUE_LIST FROM SUBSCRIBER_TOPICS;'
        result_set = db.fetchAllQuery(sql)
        for result in result_set:
            subscriber_topic = SubscriberTopic()
            subscriber_topic.subscriber_topic_name = result[0]
            if (result[1] != None) : subscriber_topic.procedure_list = ast.literal_eval(result[1])
            if (result[2] != None) : subscriber_topic.value_list = ast.literal_eval(result[2])

            # print (subscriber_topic.procedure_list.values())
            for element in subscriber_topic.procedure_list.values():
                variable_list = element.get(self.common_strings.VARIABLE_LIST)
                if (variable_list == None): continue
                for variable_element in variable_list:
                    if (not self.checkTargetTopicInVariableList(data.topic_name, variable_list[variable_element][self.common_strings.TOPIC_NAME])): continue
                    if (variable_element in subscriber_topic.value_list): 
                    # value_listの該当キーに中身がない場合は新しくリストを用意する必要がある
                        if (subscriber_topic.value_list[variable_element] != None):
                          subscriber_topic.value_list[variable_element].insert(-1, data.element_values.get(variable_list[variable_element][self.common_strings.ELEMENTS]))
                          subscriber_topic.value_list[variable_element][-1] = str(datetime.now())
                    # 一致しない場合，該当のvalue_listはNoneだけど，対象にはなっている
                    else:
                        print(variable_element) 
                        subscriber_topic.value_list[variable_element] = [data.element_values.get(variable_list[variable_element][self.common_strings.ELEMENTS])]
                        print(subscriber_topic.value_list[variable_element])
                        subscriber_topic.value_list[variable_element].add(str(datetime.now()))
                    
            if (subscriber_topic.value_list == {}): continue
            sql = 'UPDATE SUBSCRIBER_TOPICS SET VALUE_LIST = \'{0}\' WHERE (SUBSCRIBER_TOPIC = "{1}")'.format(
                json.dumps(subscriber_topic.value_list),
                subscriber_topic.subscriber_topic_name
            )
            # subscriber_topic単位で最後にVALUE_LIST要素を更新する 
            if (db.executeQuery(sql) == False): return False
        return True


    def checkTargetTopicInVariableList(self, topic_name, variable_element):
        print(topic_name, variable_element)
        if topic_name != variable_element:
            return False
        return True

