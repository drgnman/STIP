from stip.api.common.CommonStrings import CommonStrings

class Subscriber:
    def __init__(self): 
        self.common_strings = CommonStrings()
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
        self.moving_information_list = {}
        self.data_ttr = 0       # 秒単位

    def setParameters(self, subscriber):
        self.subscriber_name = subscriber[self.common_strings.SUBSCRIBER_NAME]
        self.purpose = subscriber[self.common_strings.PURPOSE]
        if (self.common_strings.LOCATION in subscriber):
            self.latitude = subscriber[self.common_strings.LOCATION][self.common_strings.LATITUDE]
            self.longitude = subscriber[self.common_strings.LOCATION][self.common_stringsLONGITUDE]
        if (self.common_strings.SPEED in subscriber):
            self.speed = subscriber[self.common_strings.SPEED]
        if (self.common_strings.DIRECTION in subscriber):
            self.direction = subscriber[self.common_strings.DIRECTION]
        
    def setSubscriberTopicParameters(self, subscriber):
        # "登録用の"SubscriberTopic要素
        self.topic_list = subscriber[self.common_strings.TOPIC_LIST]
        if (self.common_strings.RECEIVE_FREQUENCY in subscriber):
            self.receive_frequency = subscriber[self.common_strings.RECEIVE_FREQUENCY]
        self.control_mode = subscriber[self.common_strings.CONTROL_MODE]
        if ( in subscriber):
            self.detection_range = subscriber[self.common_strings.DETECTION_RANGE]
        if (self.common_strings.MOVING_INFORMATION_LIST in subscriber):
            self.moving_information_list = subscriber[self.common_strings.MOVING_INFORMATION_LIST]
        if (self.common_strings.DATA_TTR in subscriber):
            self.data_ttr = subscriber[self.common_strings.DATA_TTR]