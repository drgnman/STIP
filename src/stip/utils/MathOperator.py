import numpy as np
import statistics
import math

from stip.utils.DBUtil import DBUtil

class MathOperator:
    def __init__(self):
        pass
    
    def callCalculate(self, operator, num1, num2):
        if(operator == "Add"):
            return self.operateAdd(num1, num2)
        elif(operator == "Min"):
            return self.operateMin(num1, num2)
        elif(operator == "Mul"):
            return self.operateMul(num1, num2)
        elif(operator == "Div"):
            return self.operateDiv(num1, num2)

    def callAggregation(self, operator, value_list):
        if(operator == "SUM"):
            return self.operateSUM(value_list)
        elif(operator == "AVE"):
            return self.operateAVE(value_list)
        elif(operator == "MAX"):
            return self.operateMAX(value_list)
        elif(operator == "MIN"):
            return self.operateMIN(value_list)
        elif(operator == "MID"):
            return self.operateMID(value_list)
        elif(operator == "MOD"):
            return self.operateMOD(value_list)
        elif(operator == "NEW"):
            return self.operateNEW(value_list)

    # ちょっと仮で置いておく，どんな要素が流れてくるか考えること
    def callQuery(self, operator, topic_name):
        if(operator == "Hot"):
            return self.operateHot(topic_name)

    # 引数が二つのグループ
    def operateAdd(self, num1, num2):
        return num1 + num2 

    def operateMin(self, num1, num2):
        return num1 -  num2 

    def operateMul(self, num1, num2):
        return num1 * num2 

    def operateDiv(self, num1, num2):
        return num1 / num2

    # 引数がリスト一つのグループ
    def operateSUM(self, value_list):
        return statistics.mean(value_list) 

    def operateAVE(self, value_list):
        return statistics.harmonic_mean(value_list) 

    def operateMAX(self, value_list):
        return max(value_list)

    def operateMIN(self, value_list):
        return min(value_list) 

    def operateMID(self, value_list):
        return statistics.median(value_list)

    def operateMOD(self, value_list):
        return statistics.mode(value_list)
    
    def operateNEW(self, value_list):
        return value_list[0][0]

    # 引数がtopic名と要素名
    def operateHot(self, topic_name):
    # SQLの発行 
        sql = 'SELECT ELEMENT_VALUE, PUBLISH_TIMESTAMP FROM DATA_VALUE_TEMP WHERE TOPIC_NAME = "{0}" \
                ORDER BY PUBLISH_TIMESTAMP DESC LIMIT 1;'.format(
            topic_name
        )
        db = DBUtil()
        db.createDBConnection()
        result = db.fetchAllQuery(sql)
        db.closeDBConnection
        return result

    def isInt(self, input_value):
        try:
            int(input_value)
            return True
        except ValueError:
            return False

    def isFloat(self, input_value):
        try:
            float(input_value)
            return True
        except ValueError:
            return False

    def calculateDistance(self, base_latitude, base_longitude, latitude, longitude):
        distance = 6371 * math.acos(
            math.cos(math.radians(base_latitude))
            * math.cos(math.radians(latitude))
            * math.cos(math.radians(longitude) - math.radians(base_longitude))
            + math.sin(math.radians(base_latitude))
            * math.sin(math.radians(latitude))
        )
        return distance