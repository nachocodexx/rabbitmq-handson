class Publisher(object):
    def __init__(self, *args, **kwargs):
        self.routingKey = kwargs.get('routing_key', 'test')
        self.exchangeName = kwargs.get('exchange_name', 'testEx')

    def publish(self, *args, **kwargs):
        connection = kwargs.get('connection', None)
        channel = connection.channel()
        message = kwargs.get('message', 'HOLA')
        channel.basic_publish(exchange=str(self.exchangeName),
                              routing_key=str(self.routingKey), body=message)
        channel.close()
