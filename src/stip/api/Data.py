class Data:
    def __init__(self):
        self.publisher = ''
        self.topic_name = ''
        self.elements = ''

    def setDataParameters(self, post_data):
        self.publisher = post_data['Publisher']
        self.topic_name = post_data['TopicName']
        self.elements = post_data['Elements']