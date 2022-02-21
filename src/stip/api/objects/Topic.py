from stip.api.common.CommonStrings import CommonStrings

class Topic:       # Topicテーブルに関わる要素を初期化するためのインスタンス変数
  def __init__(self):
    self.common_strings = CommonStrings()
    self.publisher = ''
    self.topic_name = ''
    self.type = ''
    self.latitude = 0.0
    self.longitude = 0.0
    self.elements = ''
    self.effective_range = 0.0
    self.data_ttl = 0            # 秒で指定
    self.publish_frequency = 0   # 秒で指定
    self.description = ''

  def setParameters(self, create_topic_request):
    self.publisher = create_topic_request[self.common_strings.PUBLISHER]
    self.topic_name = create_topic_request[self.common_strings.TOPIC_NAME]
    self.type = create_topic_request[self.common_strings.TYPE]
    if (self.common_strings.LOCATION in create_topic_request):          # 位置情報の確認
      self.latitude = create_topic_request[self.common_strings.LOCATION][self.common_strings.LATITUDE]
      self.longitude = create_topic_request[self.common_strings.LOCATION][self.common_strings.LONGITUDE]
    if (self.common_strings.ELEMENTS in create_topic_request):          # 要素本体の確認
      self.elements = create_topic_request[self.common_strings.ELEMENTS]
    if (self.common_strings.EFFECTIVE_RANGE in create_topic_request):           # effectiveRangeの確認
      self.effective_range = create_topic_request[self.common_strings.EFFECTIVE_RANGE]
    if (self.common_strings.DATA_TTL in create_topic_request):           # dataTTLの確認
      self.data_ttl = create_topic_request[self.common_strings.DATA_TTL]
    if (self.common_strings.PUBLISH_FREQUENCY in create_topic_request):  # publishFrequency(発信頻度)の確認
      self.publish_frequency = create_topic_request[self.common_strings.PUBLISH_FREQUENCY]
    if (self.common_strings.DESCRIPTION in create_topic_request):       # 備考の確認
      self.description = create_topic_request[self.common_strings.DESCRIPTION]

