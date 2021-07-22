import sys
import os
import time
import json
from pathlib import Path
current_path = Path(os.getcwd())
sys.path.insert(1, str(current_path.parent) + '/shared')
from Producer import Producer
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
    # Create exchange & queues
    exchange_00 = Exchange(name="ex0", type="direct", connection=connection)
    queue_00 = Queue(name=queueName, connection=connection)
    queue_01 = Queue(name="qcoquer", connection=connection)
    queue_00.bind(exchange=exchange_00, routing_key=queue_00.name)
    queue_01.bind(exchange=exchange_00, routing_key=queue_01.name)

    # Create consumer
    def onMessage(ch, method, properties, body):
        # global logger
        logger.info(body)
        data = json.loads(body)
        numbers = map(lambda x: int(x), data['value'].split(","))
        result = Message(value=sum(numbers))
        p = Producer(exchange_name=exchange_00,
                     routing_key=queue_01.name, connection=connection, logger=logger)
        p.publish(message=result.toJSON(), logger=logger)
        # print(numbers)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    consumer_00 = Consumer(connection=connection)
    consumer_00.consume(queue=queue_00, callback=onMessage)
    connection.close()


if __name__ == '__main__':
    logger = Logger.create(name="WORKER", filename="./logs/worker.log")
    logger.info("Worker started successfully 🚀")
    program(logger=logger)
