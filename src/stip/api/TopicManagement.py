from stip.utils.DBUtil import DBUtil

class TopicManagement:
  def __init__(self):
    pass

  def create(self, topic):
    db = DBUtil()
    db.createDBConnection()
    sql = 'INSERT INTO TOPIC \
            (TOPIC_NAME, TOPIC_TYPE, LATITUDE, LONGITUDE, EFFECTIVE_RANGE, DATA_TTL, PUBLISH_FREQUENCY, TOPIC_DESCRIPTION, PUBLISHER) \
            VALUES ("{0}", "{1}", {2}, {3}, {4},{5}, {6}, "{7}", "{8}");'.format(
              topic.name, topic.type, topic.latitude, topic.longitude, topic.effective_range,
              topic.data_ttl, topic.publish_frequency, topic.description, topic.publisher
            ) 
    print(sql)
    result  = db.executeQuery(sql)
    return result