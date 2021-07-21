class Queue(object):
    def __init__(self, *args, **kwargs):
        self.connection = kwargs.get('connection', None)
        self.name = kwargs.get('name', "q0")
        self.__create()

    def __create(self, *args, **kwargs):
        channel = self.connection.channel()
        channel.queue_declare(queue=self.name)
        channel.close()

    def bind(self, *args, **kwargs):
        routing_key = kwargs.get('routing_key', "my_routing_key")
        exchange = kwargs.get('exchange')
        channel = self.connection.channel()
        channel.queue_bind(exchange=exchange.name,
                           queue=self.name, routing_key=str(routing_key))
        channel.close()

    def __str__(self):
        return self.name

    def __create(self):
        pass
