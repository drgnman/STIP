from stip.utils.MathOperator import MathOperator
from stip.api.common.CommonStrings import CommonStrings

class ProcessingSupports:
    def __init__(self):
        self.common_strings = CommonStrings()

    # 現状のは作ってるだけだけど，複数箇所でDataBaseコンテンツの加工が必要になったらこれに切り替える
    def convertFromStrToList(self, str_list_contents):
        # remove_quoute = str_list_contents.replace('"')
        if("'" in str_list_contents):
            str_list_contents = str_list_contents.replace("'", "")
        if(" " in str_list_contents):
            str_list_contents = str_list_contents.replace(" ", "")
        convert_to_list = str_list_contents.split(',')
        return convert_to_list

    def nextLatitudeLargerThanCurrentLatitude(self, base_latitude, latitude):
        if (latitude < base_latitude):
            return latitude, True
        return base_latitude, False

    def nextLatitudeSmallerThanCurrentLatitude(self, base_latitude, latitude):
        if (base_latitude < latitude):
            return latitude, True
        return base_latitude, False

    def nextLongitudeLagerThanCurrentLongitude(self, base_longitude, longitude):
        if (longitude < base_longitude):
            return longitude, True
        return base_longitude, False

    def nextLongitudeSmallerThanCurrentLongitude(self, base_longitude, longitude):
        if (base_longitude < longitude):
            return longitude, True
        return base_longitude, False

    def compareDistanceDuaringSubscriberAndTopic(self, target_topic_name, topic_name, base_latitude, base_longitude, latitude, longitude, detection_range):
        math_operator = MathOperator()
        if(target_topic_name != topic_name[topic_name.rfind("_")+1:]):
            return False
        distance = math_operator.calculateGeoInformation(
            base_latitude, base_longitude, latitude, longitude, self.common_strings.GIS_DISTANCE)
        if (distance < detection_range):
            return True
        return False
                
    
