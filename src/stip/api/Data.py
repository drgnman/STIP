class Data:
    def __init__(self):
        self.publisher = ''
        self.topic_name = ''
        self.element_values = ''

    def setDataParameters(self, post_data):
        self.publisher = post_data['Publisher']
        self.topic_name = post_data['TopicName']
        self.element_values = post_data['Elements']