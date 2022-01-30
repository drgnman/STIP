class BaseTopicForDTOS:
    def __init__(self):
        self.topic_name = ''
        self.latitude = 0.0
        self.longitude = 0.0
        self.data_ttl = 0.0
        self.effective_range = 0.0
    
    def setParameter(self, base_data):
        self.topic_name = base_data[0]
        self.latitude = float(base_data[1])
        self.longitude = float(base_data[2])
        self.data_ttl = float(base_data[3])
        self.effective_range = float(base_data[4])
