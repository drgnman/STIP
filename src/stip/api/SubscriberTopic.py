class SubscriberTopic:
    def __init__(self): 
        self.subscriber_topic_name = ''
        self.topic_list = ''
        self.extracted_topic_list = ''
        self.value_list = {}
        self.procedure_list = {}
        self.pmflag = ''
        self.receive_frequency = ''
        self.data_ttr = 0
        self.detection_range = 0.0
        self.publish_timestamp = ''

    def setParameters(self, subscriber_topic):
        self.subscriber_topic_name = subscriber_topic['SubscriberTopicName']
        self.topic_list = subscriber_topic['TopicList']
        self.extracted_topic_list = subscriber_topic['ExtractedTopicList']
        self.value_list = subscriber_topic['ValueList']
        self.procedure_list = subscriber_topic['ProcedureList']
        self.pmflag = subscriber_topic['PMFlag']
        self.receive_frequency = subscriber_topic['ReceiveFrequency']
        self.data_ttr = subscriber_topic['DataTTR']
        self.detection_range = subscriber_topic['DetectionRange']