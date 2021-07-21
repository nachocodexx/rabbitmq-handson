import pika


class RabbitMQ(object):

    @staticmethod
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
        logger = kwargs.get('logger')
        logger.info("RabbitMQ connection established 🐇")

        return connection
