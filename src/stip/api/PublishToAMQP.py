import pika
import json

class PublishToAMQP:
    def __init__(self):
        pass

    def createConnection(self, ip='localhost', p='5672'):
        connection = pika.BlockkingConnection(
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