import sys
import os
import time
from pathlib import Path
current_path = Path(os.getcwd())
sys.path.insert(1, str(current_path.parent) + '/shared')
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
    queueName = sys.argv[1]
    logger = kwargs.get('logger')
    '''
        - Description 
        connect to rabbitmq and get a connection. 
        - Type declaration
        connectToRabbitMQ: :  ConnectionParameters -> RabbitMQConnection
    '''
    connection = RabbitMQ.connectToRabbitMQ(logger=logger)
    # Create exchange, routing keys & queues
    # Create a queue with an identifier -> my_queue
    queue_00 = Queue(name=queueName, connection=connection)
    # Create consumer
    consumer_00 = Consumer(connection=connection)
    consumer_00.consume(queue=queue_00)
    connection.close()


if __name__ == '__main__':
    logger = Logger.create(name="WORKER", filename="worker.log")
    logger.info("Worker started successfully 🚀")
    program(logger=logger)
