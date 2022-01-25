class Subscriber:
    def __init__(self): 
        self.subscriber_name = ''
        self.purpose = ''
        self.latitude = 0.0
        self.longitude = 0.0
        self.speed = 0.0
        self.direction = 0.0

    def setSubscriberParameters(self, subscriber):
        self.subscriber_name = subscriber['SubscriberName']
        if ("Location" in subscriber):
            self.latitude = subscriber['Location']['Latitude']
            self.longitude = subscriber['Location']['Longitude']
        
        if ("Speed" in subscriber):
            self.speed = subscriber['Speed']

        if ("Direction" in subscriber):
            self.speed = subscriber['Direction']