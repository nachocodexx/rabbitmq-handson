class Consumer(object):
    def __init__(self, *args, **kwargs):
        self.connection = kwargs.get('connection')

    def defaultCallback(self, ch, method, properties, body):
        print("NEW MESSAGE -> {}".format(body))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def consume(self, *args, **kwargs):
        logger = kwargs.get('logger')
        queue = str(kwargs.get('queue'))
        callback = kwargs.get('callback', self.defaultCallback)
        channel = self.connection.channel()
        channel.basic_consume(queue=queue, on_message_callback=callback)
        channel.start_consuming()
        return channel
