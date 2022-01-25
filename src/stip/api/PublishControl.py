from stip.api.PublishToPlatforms import PublishToAMQP, PublishToMQTT

class PublishControl:
    def __init__(self):
        pass

    def publishDirectly(self, data, iot_type="amqp"):
        if (iot_type == "amqp"):
            return self.publishToAQMP(data)
        elif (iot_type == "mqtt"):
            return self.publishToMQTT(data)

    def publishToAQMP(self, data):
        try:
            publish_to_amqp = PublishToAMQP()
            connection, channel = publish_to_amqp.createConnection()
            publish_to_amqp.dataPublishToAMQP(channel, data)
            return True
        except Exception as e:
            print(e)
            return False

    def publishToMQTT(self, data):
        try: 
            publish_to_mqtt = PublishToMQTT()
            publish_to_mqtt.setConnection()
            publish_to_mqtt.dataPublishToMQTT(data)
            return True
        except Exception as e:
            print(e)
            return False
