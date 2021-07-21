import sys
import os
from pathlib import Path
current_path = Path(os.getcwd())
sys.path.insert(1, str(current_path.parent) + '/shared')
import pika
from Publisher import Publisher
from Message import Message
from Queue import Queue
from Exchange import Exchange
from RoutingKey import RoutingKey

"""
 parameters: ConnectionParameters :: (username,password,port,virtual_host,host)
 type      : ConnectionParameters -> RabbitMQConnection
"""


def connectToRabbitMQ(*args, **kwargs):
    # ConnectionParameters
    username = kwargs.get('username', 'guest')
    password = kwargs.get('password', 'guest')
    port = kwargs.get('port', 5672)
    virtualHost = kwargs.get('virtual_host', '/')
    host = kwargs.get('host', "localhost")
    #
    connectionCredentials = pika.PlainCredentials(username, password)
    connectionParams = pika.ConnectionParameters(
        host, port, virtualHost, connectionCredentials)
    connection = pika.BlockingConnection(connectionParams)
    return connection


def program(*args, **kwargs):
    '''
        # Description 
        connect to rabbitmq and get a connection. 
        # Type declaration
        connectToRabbitMQ: :  ConnectionParameters -> RabbitMQConnection
    '''
    connection = connectToRabbitMQ()
    # Create exchange, routing keys & queues
    routingKey_00 = RoutingKey(name="my_routing_key")
    queue_00 = Queue(name="my_queue", connection=connection)
    exchange_00 = Exchange(
        name="my_exchange", type="direct", connection=connection)
    queue_00.bind(exchange=exchange_00, routing_key=routingKey_00)
    # createQueue(connection=connection, queue_name='my_queue')
    # publish "my_message"
    publisher_00 = Publisher(exchange_name=exchange_00,
                             routing_key=routingKey_00)

    publisher_01 = Publisher(exchange_name='', routing_key=queue_00.name)

    message_00 = Message(value='Hola', user_id="user_00")
    # Simple message
    publisher_00.publish(message='my_message', connection=connection)
    # Advanced message
    publisher_01.publish(connection=connection, message=message_00.toJSON())
    # close the connection
    connection.close()


if __name__ == '__main__':
    program()
