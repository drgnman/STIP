import ast

from stip.api.common.CommonStrings import CommonStrings

class SubscriberTopic:
    def __init__(self): 
        self.common_strings = CommonStrings()
        self.subscriber_topic_name = ''
        self.topic_list = ''
        self.extracted_topic_list = ''
        self.value_list = {}
        self.variable_list = {}
        self.procedure_list = {}
        self.control_mode = ''     # 旧 PM_Flag
        self.receive_frequency = ''
        self.data_ttr = 0
        self.detection_range = 0.0
        self.moving_infomation_list = {}
        self.publish_timestamp = ''
        self.create_timestamp = ''

    def setParameters(self, subscriber_topic):
        if (self.common_strings.SUBSCRIBER_TOPIC_NAME in subscriber_topic):
            self.subscriber_topic_name = subscriber_topic[self.common_strings.SUBSCRIBER_TOPIC_NAME]
        if (self.common_strings.TOPIC_LIST in subscriber_topic):
            self.topic_list = subscriber_topic[self.common_strings.TOPIC_LIST]
        if (self.common_strings.EXTRACTED_TOPIC_LIST in subscriber_topic):
            self.extracted_topic_list = subscriber_topic[self.common_strings.EXTRACTED_TOPIC_LIST]
        if (self.common_strings.VALUE_LIST in subscriber_topic):
            self.value_list = subscriber_topic[self.common_strings.VALUE_LIST]
        if (self.value_list != None):
            self.value_list = ast.literal_eval(self.value_list)
        if (self.common_strings.VARIABLE_LIST in subscriber_topic):
            self.variable_list = subscriber_topic[self.common_strings.VARIABLE_LIST]
        if (self.variable_list != None):
            self.variable_list = ast.literal_eval(self.variable_list)
        if (self.common_strings.PROCEDURE_LIST in subscriber_topic):
            self.procedure_list = subscriber_topic[self.common_strings.PROCEDURE_LIST]
        if (self.procedure_list != None):
            self.procedure_list = ast.literal_eval(self.procedure_list)
        if (self.common_strings.CONTROL_MODE in subscriber_topic):
            self.control_mode = subscriber_topic[self.common_strings.CONTROL_MODE]
        if (self.common_strings.RECEIVE_FREQUENCY in subscriber_topic):
            self.receive_frequency = subscriber_topic[self.common_strings.RECEIVE_FREQUENCY]
        if (self.common_strings.DATA_TTR in subscriber_topic):
            self.data_ttr = subscriber_topic[self.common_strings.DATA_TTR]
        if (self.common_strings.DETECTION_RANGE in subscriber_topic):
            self.detection_range = subscriber_topic[self.common_strings.DETECTION_RANGE]
        if (self.common_strings.MOVING_INFORMATION_LIST in subscriber_topic):
            self.moving_infomation_list = subscriber_topic[self.common_strings.MOVING_INFORMATION_LIST]
        if (self.common_strings.PUBLISH_TIMESTAMP in subscriber_topic):
            self.publish_timestamp = subscriber_topic[self.common_strings.PUBLISH_TIMESTAMP]
        if (self.common_strings.CREATE_TIMESTAMP in subscriber_topic):
            self.create_timestamp = subscriber_topic[self.common_strings.CREATE_TIMESTAMP]

    def setParameterFromList(self, subscriber_topic):
        self.subscriber_topic_name = subscriber_topic[0]
        self.topic_list = subscriber_topic[1]
        self.extracted_topic_list = subscriber_topic[2]
        self.value_list = subscriber_topic[3]
        if (self.value_list != None):
            self.value_list = ast.literal_eval(self.value_list)
        self.procedure_list = subscriber_topic[4]
        if (self.procedure_list != None):
            self.procedure_list = ast.literal_eval(self.procedure_list)
        self.control_mode = subscriber_topic[5]     # 旧 PM_Flag
        self.receive_frequency = subscriber_topic[6]
        self.data_ttr = subscriber_topic[7]
        self.detection_range = subscriber_topic[8]
        self.publish_timestamp = subscriber_topic[9]
        self.create_timestamp = subscriber_topic[10]
        self.moving_infomation_list = subscriber_topic[11] # 仮置き