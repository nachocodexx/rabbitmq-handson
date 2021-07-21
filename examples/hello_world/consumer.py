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


def program(*args, **kwargs):
    logger = kwargs.get('logger')
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
    # Create consumer
    consumer_00 = Consumer(connection=connection)
    consumer_00.consume(queue=queue_00)
    connection.close()


if __name__ == '__main__':
    logger = Logger.create(name="CONSUMER")
    logger.info("Consumer started successfully 🚀")
    program(logger=logger)
