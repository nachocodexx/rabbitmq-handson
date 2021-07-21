import sys
import os
import time
from pathlib import Path
current_path = Path(os.getcwd())
sys.path.insert(1, str(current_path.parent) + '/shared')
from Publisher import Publisher
from Message import Message
from Queue import Queue
from Exchange import Exchange
from RoutingKey import RoutingKey
from RabbitMQ import RabbitMQ
from Logger import Logger
from Consumer import Consumer
"""
 parameters: ConnectionParameters :: (username,password,port,virtual_host,host)
 type      : ConnectionParameters -> RabbitMQConnection
"""


def program(*args, **kwargs):
    logger = kwargs.get('logger')
    '''
        - Description 
        connect to rabbitmq and get a connection. 
        - Type declaration
        connectToRabbitMQ: :  ConnectionParameters -> RabbitMQConnection
    '''
    connection = RabbitMQ.connectToRabbitMQ(logger=logger)
    # Create exchange, routing keys & queues
    # Routing key
    routingKey_00 = RoutingKey(name="my_routing_key")
    # Create a queue with an identifier -> my_queue
    queue_00 = Queue(name="my_queue", connection=connection)
    # Exchange
    exchange_00 = Exchange(
        name="my_exchange", type="direct", connection=connection)
    # Bind queue_00 to a exchange using a routingKey_00
    queue_00.bind(exchange=exchange_00, routing_key=routingKey_00)
    # Create a publisher that emits messages to a queue using routingKey_00 through the exchange_00
    publisher_00 = Publisher(exchange_name=exchange_00,
                             routing_key=routingKey_00)
   # Special publisher using the default exchange that emits messages direct to queue name that is equal to the routing_key
    publisher_01 = Publisher(exchange_name='', routing_key=queue_00.name)

    message_00 = Message(value='Hola', user_id="user_00")
    # Simple message
    publisher_00.publish(message='my_message',
                         connection=connection, logger=logger)
    # Advanced message
    publisher_01.publish(message=message_00.toJSON(),
                         logger=logger, connection=connection)
    connection.close()


if __name__ == '__main__':
    logger = Logger.create(name="PRODUCER-0")
    logger.info("Producer started successfully 🚀")
    program(logger=logger)
