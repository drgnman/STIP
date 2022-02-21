class Topic:       # Topicテーブルに関わる要素を初期化するためのインスタンス変数
  def __init__(self):
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
    self.publisher = create_topic_request['Publisher']
    self.topic_name = create_topic_request['TopicName']
    self.type = create_topic_request['Type']
    if ('Location' in create_topic_request):          # 位置情報の確認
      self.latitude = create_topic_request['Location']['Latitude']
      self.longitude = create_topic_request['Location']['Longitude']
    if ('Elements' in create_topic_request):          # 要素本体の確認
      self.elements = create_topic_request['Elements']
    if ('EffectiveRange' in create_topic_request):           # effectiveRangeの確認
      self.effective_range = create_topic_request['EffectiveRange']
    if ('DataTTL' in create_topic_request):           # dataTTLの確認
      self.data_ttl = create_topic_request['DataTTL']
    if ('PublishFrequency' in create_topic_request):  # publishFrequency(発信頻度)の確認
      self.publish_frequency = create_topic_request['PublishFrequency']
    if ('Description' in create_topic_request):       # 備考の確認
      self.description = create_topic_request['Description']

