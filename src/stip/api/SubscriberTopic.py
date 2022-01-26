import ast

class SubscriberTopic:
    def __init__(self): 
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
        self.publish_timestamp = ''
        self.create_timestamp = ''

    def setParameters(self, subscriber_topic):
        if ("SubscriberTopicName" in subscriber_topic):
            self.subscriber_topic_name = subscriber_topic['SubscriberTopicName']
        if ("TopicList" in subscriber_topic):
            self.topic_list = subscriber_topic['TopicList']
        if ("ExtractedTopicList" in subscriber_topic):
            self.extracted_topic_list = subscriber_topic['ExtractedTopicList']
        if ("ValueList" in subscriber_topic):
            self.value_list = ast.literal_eval(subscriber_topic['ValueList'])
        if ("VariableList" in subscriber_topic):
            self.variable_list = ast.literal_eval(subscriber_topic['VariablaList'])
        if ("ProcedureList" in subscriber_topic):
            self.procedure_list = ast.literal_eval(subscriber_topic['ProcedureList'])
        if ("ControlMode" in subscriber_topic):
            self.control_mode = subscriber_topic['ControlMode']
        if ("ReceiveFrequency" in subscriber_topic):
            self.receive_frequency = subscriber_topic['ReceiveFrequency']
        if ("DataTTR" in subscriber_topic):
            self.data_ttr = subscriber_topic['DataTTR']
        if ("DetectionRange" in subscriber_topic):
            self.detection_range = subscriber_topic['DetectionRange']
        if ("PublishTimestamp" in subscriber_topic):
            self.publish_timestamp = subscriber_topic['PublishTimestamp']
        if ("CreateTimestamp" in subscriber_topic):
            self.create_timestamp = subscriber_topic['CreateTimestamp']

    def setParameterFromList(self, subscriber_topic):
        self.subscriber_topic_name = subscriber_topic[0]
        self.topic_list = subscriber_topic[1]
        self.extracted_topic_list = subscriber_topic[2]
        self.value_list = ast.literal_eval(subscriber_topic[3])
        self.procedure_list = ast.literal_eval(subscriber_topic[4])
        self.control_mode = subscriber_topic[5]     # 旧 PM_Flag
        self.receive_frequency = subscriber_topic[6]
        self.data_ttr = subscriber_topic[7]
        self.detection_range = subscriber_topic[8]
        self.publish_timestamp = subscriber_topic[9]
        self.create_timestamp = subscriber_topic[10]
