class Queue(object):
    def __init__(self, *args, **kwargs):
        self.connection = kwargs.get('connection', None)
        self.name = kwargs.get('name', "q0")
        self.durable = kwargs.get('durable', True)
        self.create()

    def create(self, *args, **kwargs):
        channel = self.connection.channel()
        channel.queue_declare(queue=self.name, durable=self.durable)
        channel.close()

    def bind(self, *args, **kwargs):
        routing_key = kwargs.get('routing_key', "my_routing_key")
        exchange = kwargs.get('exchange')
        channel = self.connection.channel()
        channel.queue_bind(exchange=str(exchange),
                           queue=self.name, routing_key=str(routing_key))
        channel.close()

    def __str__(self):
        return self.name

    def __create(self):
        pass
