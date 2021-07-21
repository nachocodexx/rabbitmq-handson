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
    '''
        - Description 
        connect to rabbitmq and get a connection. 
        - Type declaration
        connectToRabbitMQ: :  ConnectionParameters -> RabbitMQConnection
    '''
    connection = RabbitMQ.connectToRabbitMQ(logger=logger)
    routingKeys = list(map(lambda name: RoutingKey(name=name), queueNames))
    queues = list(map(lambda name: Queue(
        name=name, connection=connection), queueNames))

    # Create exchange, routing keys & queues
    # Exchange
    exchange_00 = Exchange(name="ex0", type="direct", connection=connection)
    queuesAndRks = list(zip(queues, routingKeys))
    bindings = list(map(lambda args: args[0].bind(
        exchange=exchange_00, routing_key=args[1]), queuesAndRks))
    print(bindings)
    # Create a publisher that emits messages to a queue using routingKey_00 through the exchange_00
    producers = list(map(lambda rk: Producer(
        exchange_name=exchange_00, routing_key=rk, connection=connection), routingKeys))
   # Special publisher using the default exchange that emits messages direct to queue name that is equal to the routing_key

    # Advanced message
    numQueues = len(queueNames)
    numbersPerWorker = 10
    numbers = list(range(numQueues * numbersPerWorker))

    workerData = list(map(lambda i: numbers[(
        i - 1) * numbersPerWorker:(numbersPerWorker * i)], range(1, numQueues + 1)))
    print(workerData)

    def toString(x): return str(x)
    messages = list(map(lambda value: Message(value=','.join(
        list(map(toString, value))), user_id="user_00"), workerData))

    def sendMessage(x):
        x[0].publish(message=x[1].toJSON(), logger=logger)
    workersAndMessages = list(zip(producers, messages))
    list(map(sendMessage, workersAndMessages))
    # publisher_00.publish(message=message_00.toJSON(), logger=logger)
    connection.close()


if __name__ == '__main__':
    logger = Logger.create(name="MANAGER-0", filename="manager.log")
    logger.info("Manager started successfully 🚀")
    queueNames = sys.argv[1:]
    program(logger=logger, queueNames=queueNames)
