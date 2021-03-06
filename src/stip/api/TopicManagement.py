from stip.api.common.CommonStrings import CommonStrings

from stip.utils.DBUtil import DBUtil

class TopicManagement:
  def __init__(self):
    self.common_strings = CommonStrings()

  def topicCreate(self, topic):
    db = DBUtil()
    db.createDBConnection()
    sql = 'INSERT INTO TOPIC \
            (TOPIC_NAME, TOPIC_TYPE, LATITUDE, LONGITUDE, EFFECTIVE_RANGE, DATA_TTL, PUBLISH_FREQUENCY, TOPIC_DESCRIPTION, PUBLISHER) \
            VALUES ("{0}", "{1}", {2}, {3}, {4},{5}, {6}, "{7}", "{8}");'.format(
              topic.topic_name, topic.type, topic.latitude, topic.longitude, topic.effective_range,
              topic.data_ttl, topic.publish_frequency, topic.description, topic.publisher
            ) 
    result  = db.executeQuery(sql)
    db.closeDBConnection()
    return result
  
  def elementsSet(self, topic):
    db = DBUtil()
    db.createDBConnection()
    for request_element in topic.elements:
      element = topic.elements[request_element]
      unit = ''
      min_value = 0.0
      max_value = 0.0

      if(type(element) != str):
       if (self.common_strings.UNIT in element.keys()): 
         unit = element[self.common_strings.UNIT]
       if (self.common_strings.MIN_VALUE in element.keys()): 
         unit = element[self.common_strings.MIN_VALUE]
       if (self.common_strings.MAX_VALUE in element.keys()): 
         unit = element[self.common_strings.MAX_VALUE]

      sql = 'INSERT INTO ELEMENTS (TOPIC_NAME, ELEMENT_NAME, UNIT, MIN_VALUE, MAX_VALUE) \
              VALUES ("{0}", "{1}", "{2}", {3}, {4});'.format(
                topic.topic_name, request_element, unit, min_value, max_value
              )
      result = db.executeQuery(sql)

    db.closeDBConnection()
    return result

  def topicExistCheck(self, topic_name, publisher):
    db = DBUtil()
    db.createDBConnection()
    sql = 'SELECT COUNT(*) FROM TOPIC WHERE TOPIC_NAME = "{0}" AND PUBLISHER = "{1}";'.format(
      topic_name, publisher
    )
    result = db.fetchSingleQuery(sql)
    db.closeDBConnection()
    if (result > 0): return True
    return False