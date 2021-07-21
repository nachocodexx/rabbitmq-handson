class RoutingKey(object):
    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name', 'my_routing_key_test')

    def __str__(self):
        return self.name
