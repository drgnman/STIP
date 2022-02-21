from stip.api.common.CommonStrings import CommonStrings

class Data:
    def __init__(self):
        self.common_strings = CommonStrings()
        self.publisher = ''
        self.topic_name = ''
        self.element_values = ''

    def setParameters(self, post_data):
        self.publisher = post_data[self.common_strings.PUBLISHER]
        self.topic_name = post_data[self.common_strings.TOPIC_NAME]
        self.element_values = post_data[self.common_strings.ELEMENTS]