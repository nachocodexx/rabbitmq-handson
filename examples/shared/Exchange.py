class Exchange(object):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.connection = kwargs.get('connection')
        self.create()

    def create(self, *args, **kwargs):
        channel = self.connection.channel()
        channel.exchange_declare(exchange=self.name, exchange_type=self.type)
        channel.close()

    def __str__(self):
        return self.name
