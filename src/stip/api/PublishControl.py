from stip.api.PublishToPlatforms import PublishToAMQP, PublishToMQTT

class PublishControl:
    def __init__(self):
        pass

    def publishDirectly(self, data, iot_type="amqp"):
        if (iot_type == "amqp"):
            self.publishToAQMP(data)
        elif (iot_type == "mqtt"):
            self.publishToMQTT(data)

    def publishToAQMP(self, data):
        publish_to_amqp = PublishToAMQP()
        connection, channel = publish_to_amqp.createConnection()
        publish_to_amqp.dataPublishToAMQP(channel, data)
        return True

    def publishToMQTT(self, data):
        publish_to_mqtt = PublishToMQTT()
        publish_to_mqtt.setConnection()
        publish_to_mqtt.dataPublishToMQTT(data)
        return True
