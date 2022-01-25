from stip.utils.DBUtil import DBUtil
import datetime
import json

class DataManagement:
    def __init__(self):
        pass

    def insertToDataValue(self, data):
        db = DBUtil()
        db.createDBConnection()

        # DataValueテーブルへのデータ追加
        sql = "INSERT IGNORE INTO DATA_VALUE_TEMP (TOPIC_NAME, ELEMENT_VALUE) VALUES ('{0}', '{1}');".format(
            data.topic_name, json.dumps(data.element_values)
        )
        print(sql)
        result = db.executeQuery(sql)
        db.closeDBConnection()
        return result
    
    def insertToSubscriberTopic(self, data):
        pass