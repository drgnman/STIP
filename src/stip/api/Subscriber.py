class Subscriber:
    def __init__(self): 
        self.subscriber_name = ''
        self.purpose = ''
        self.latitude = 0.0
        self.longitude = 0.0
        self.speed = 0.0
        self.direction = 0.0

        # "登録用の"SubscriberTopic要素
        self.topic_list = {}
        self.receive_frequency = ''
        self.control_mode = ''     # Database嬢はPM_FLAG ("Contronlの手段を管理する")
        self.detection_range = 0.0
        self.data_ttr = 0       # 秒単位

    def setParameters(self, subscriber):
        self.subscriber_name = subscriber['SubscriberName']
        self.purpose = subscriber['Purpose']
        if ("Location" in subscriber):
            self.latitude = subscriber['Location']['Latitude']
            self.longitude = subscriber['Location']['Longitude']
        if ("Speed" in subscriber):
            self.speed = subscriber['Speed']
        if ("Direction" in subscriber):
            self.direction = subscriber['Direction']
        
    def setSubscriberTopicParameters(self, subscriber):
        # "登録用の"SubscriberTopic要素
        self.topic_list = subscriber['TopicList']
        self.receive_frequency = subscriber['ReceiveFrequency']
        self.control_mode = subscriber['ControlMode']
        self.detection_range = subscriber['DetectionRange']
        self.data_ttr = subscriber['DataTTR']