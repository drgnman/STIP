from stip.utils.DBUtil import DBUtil

class SubscriberManagement:
    def __init__(self):
        pass

    def registerSubscriber(self, subscriber):
        db = DBUtil()
        db.createDBConnection()
        sql = 'INSERT IGNORE INTO SUBSCRIBERS (SUBSCRIBER, LATITUDE, LONGITUDE) VALUES \
                ("{0}", {1}, {2});'.format(
                    subscriber.subscriber_name,
                    subscriber.latitude,
                    subscriber.longitude                    
                )
        result = db.executeQuery(sql)
        return result