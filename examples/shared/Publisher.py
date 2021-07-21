class Publisher(object):
    def __init__(self, *args, **kwargs):
        self.routingKey = kwargs.get('routing_key', 'test')
        self.exchangeName = kwargs.get('exchange_name', 'testEx')

    def publish(self, *args, **kwargs):
        logger = kwargs.get('logger')
        connection = kwargs.get('connection', None)
        message = kwargs.get('message', 'HOLA')
        channel = connection.channel()
        channel.basic_publish(exchange=str(self.exchangeName),
                              routing_key=str(self.routingKey), body=message)
        logger.info("Message sent to {} using {} as routing key".format(
            self.exchangeName, self.routingKey))
        channel.close()
