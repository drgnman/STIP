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

    def setParameters(self, subscriber_topic):
        if ("SubscriberTopicName" in subscriber_topic):
            self.subscriber_topic_name = subscriber_topic['SubscriberTopicName']
        if ("TopicList" in subscriber_topic):
            self.topic_list = subscriber_topic['TopicList']
        if ("ExtractedTopicList" in subscriber_topic):
            self.extracted_topic_list = subscriber_topic['ExtractedTopicList']
        if ("ValueList" in subscriber_topic):
            self.value_list = subscriber_topic['ValueList']
        if ("VariableList" in subscriber_topic):
            self.variable_list = subscriber_topic['VariablaList']
        if ("ProcedureList" in subscriber_topic):
            self.procedure_list = subscriber_topic['ProcedureList']
        if ("ControlMode" in subscriber_topic):
            self.control_mode = subscriber_topic['ControlMode']
        if ("ReceiveFrequency" in subscriber_topic):
            self.receive_frequency = subscriber_topic['ReceiveFrequency']
        if ("DataTTR" in subscriber_topic):
            self.data_ttr = subscriber_topic['DataTTR']
        if ("DetectionRange" in subscriber_topic):
            self.detection_range = subscriber_topic['DetectionRange']