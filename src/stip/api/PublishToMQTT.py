import paho.mqtt.client as mqtt
# from time import sleep # loop制御に使うかもしれない
import json

class PublishToMQTT:
    def __init__(self):
        self.client = mqtt.Client()

    def setConnection(self, ip='localchost', p=1883):
        self.client.connect(ip, p, 60)

    def dataPublishToMQTT(self, data):
        self.client.loop_start()
        self.client.publish(data.topic_name, json.dumps(data.element_values))
        self.client.loop_stop()