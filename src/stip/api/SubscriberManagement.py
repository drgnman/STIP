from stip.utils.DBUtil import DBUtil

class SubscriberManagement:
    def __init__(self):
        pass

    def registerSubscriber(self, subscriber):
        db = DBUtil()
        db.createDBConnection()
        sql = 'INSERT IGNORE INTO SUBSCRIBERS (SUBSCRIBER, LATITUDE, LONGITUDE, SPEED, DIRECTION) \
            VALUES ("{0}", {1}, {2}, "{3}", "{4}");'.format(
                    subscriber.subscriber_name,
                    subscriber.latitude,
                    subscriber.longitude,
                    subscriber.speed,
                    subscriber.direction 
                )
        result = db.executeQuery(sql)
        return result