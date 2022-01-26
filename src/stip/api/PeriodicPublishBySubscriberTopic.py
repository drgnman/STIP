from stip.utils.DBUtil import DBUtil
from stip.api.PeriodicControl import PeriodicControl
from stip.api.PublishControl import PublishControl
from stip.api.SubscriberTopic import SubscriberTopic

class PeriodicPublishBySubscriberTopic:
    periodic_control = PeriodicControl()
    def __init__(self):
        pass

    def PublishBySubscriberTopic(self):
        db = DBUtil()
        db.createDBConnection()
        sql = 'SELECT * FROM SUBSCRIBER_TOPICS;'
        all_subscriber_topic_list = db.fetchAllQuery(sql)

        for record in all_subscriber_topic_list:
            subscriber_topic = SubscriberTopic()
            subscriber_topic.setParameterFromList(record)
            if not (self.periodic_control.judgeToPublishTarget(subscriber_topic.receive_frequency, subscriber_topic.create_timestamp)):
                continue
            print(subscriber_topic)

