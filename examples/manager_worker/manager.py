
import sys
import os
import time
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
    logger = kwargs.get('logger')
    queueNames = kwargs.get('queueNames')
    connection = RabbitMQ.connectToRabbitMQ(logger=logger)
    # Create a queue with an identifier -> name
    queues = list(map(lambda name: Queue(
        name=name, connection=connection), queueNames))
    # Exchange
    exchange_00 = Exchange(
        name="my_fanout", type="fanout", connection=connection)
    # Bind queue_00 to a exchange using a routingKey_00
    bindings = list(map(lambda q: q.bind(exchange=exchange_00), queues))
    # Create a publisher that emits messages to a queue using routingKey_00 through the exchange_00
    producer_00 = Producer(exchange_name=exchange_00, connection=connection)
   # Special publisher using the default exchange that emits messages direct to queue name that is equal to the routing_key

    # Advanced message
    message_00 = Message(
        value='[1,2,3,4,5,5,10,10,100,100,50,50]', user_id="user_00")
    # Advanced message
    producer_00.publish(message=message_00.toJSON(), logger=logger)
    connection.close()


if __name__ == '__main__':
    logger = Logger.create(name="MANAGER-0", filename="manager.log")
    logger.info("Manager started successfully 🚀")
    queueNames = sys.argv[1:]
    program(logger=logger, queueNames=queueNames)
