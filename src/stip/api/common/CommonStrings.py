
class CommonStrings:
    def __init__(self):
        # 共通符号
        self.STR_SPACE = " "
        self.STR_UNDER_BAR = "_"

        # モード制御
        self.CONTROL_MODE= "ControlMode"
        self.PERIODIC = "Periodic"
        self.AGGREGATION = "Aggregation"
        self.DYNAMIC = "Dynamic"
        self.PERIODIC_AND_DYNAMIC = "Periodic_Dynamic"
        self.AGGREGATION_AND_DYNAMIC = "Aggregation_Dynamic"

        # 共通用語
        self.LOCATION = "Location"
        self.LATITUDE = "Latitude"
        self.LONGITUDE = "Longitude"

        # Publisher及びTopic登録時の情報
        self.PUBLISHER = "Publisher"
        self.TYPE = "Type"
        self.TOPIC = "Topic"
        self.TOPIC_NAME = "TopicName"
        self.EFFECTIVE_RANGE = "EffectiveRange"
        self.DATA_TTL = "DataTTL"
        self.PUBLISH_FREQUENCY = 'PublishFrequency'
        self.DESCRIPTION = "Description"
        self.UNIT = "Unit"
        self.MAX_VALUE = "MaxValue"
        self.MIN_VALUE = "MinValue"

        # Subscriber及びSubscriber Topic登録時の情報
        self.SUBSCRIBER = "Subscriber"
        self.SUBSCRIBER_NAME = "SubscriberName"
        self.PURPOSE = "Purpose"

        self.TOPIC_LIST = "TopicList"
        self.EXTRACTED_TOPIC_LIST = "ExtractedTopicList"
        self.ELEMENTS = "Elements"
        self.VALUE_LIST = "ValueList"
        self.SUBSCRIBER_TOPIC = "SubscriberTopic"
        self.SUBSCRIBER_TOPIC_NAME = "SubscriberTopicName"
        self.RECEIVE_FREQUENCY = "ReceiveFrequency"

        self.PROCEDURE = "Procedure"
        self.PROCEDURE_LIST = "ProcedureList"
        self.VARIABLE_LIST = "VariableList"
        self.DATA_TTR = "DataTTR"

        self.DETECTION_RANGE = "DetectionRange"
        self.SPEED = "Speed"
        self.DIRECTION = "Direction"
        self.MOVING_INFORMATION_LIST = "MovingInformationList"

        self.PUBLISH_TIMESTAMP = "PublishTimestamp"
        self.CREATE_TIMESTAMP = "CreateTimestamp"

        # 処理に関わる用語
        self.GEOMETORY = "Geometory"
        self.DURATION = "Duration"
        self.LATLNG = "Latlng"
        self.DISTANCE = "Distance"
        self.DURATION = "Duration"
        self.GIS_DISTANCE = "distance"
        self.GIS_AZIMUTH = "azimuth"

        self.HOT = "Hot"

        # IoTPlatformプロトコル名
        self.AMQP = "amqp"
        self.MQTT = "mqtt"