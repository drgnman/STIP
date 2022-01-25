# AMQP
import pika
import json

#MQTT
import paho.mqtt.client as mqtt
# from time import sleep # loop制御に使うかもしれない
import json

class PublishToAMQP:
    def __init__(self):
        pass

    def createConnection(self, ip='localhost', p='5672'):
        connection = pika.BlockingConnection(
            # credentials = pika.PlainCredentials('username', 'password')
            pika.ConnectionParameters(host=ip, port=p)
        )
        channel = connection.channel()
        return connection, channel

    def closeConnection(self, connection):
        connection.close()

    def dataPublishToAMQP(self, channel, data): # dataオブジェクトにはトピック名とelement_values(送信するデータ本体)が入っていること
        channel.exchange_declare(exchange=data.topic_name, exchange_type='fanout')
        channel.basic_publish(exchange=data.topic_name, routing_key='', body=json.dumps(data.element_values))

class PublishToMQTT:
    def __init__(self):
        self.client = mqtt.Client()

    def setConnection(self, ip="localhost", p=1883):
        self.client.connect(ip, p, 60)

    def dataPublishToMQTT(self, data):
        self.client.loop_start()
        self.client.publish(data.topic_name, json.dumps(data.element_values))
        self.client.loop_stop()
