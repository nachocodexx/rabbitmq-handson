import sys
import logging


class Logger(object):
    # def __init__(self, *args, **kwargs):

    @staticmethod
    def create(*args, **kwargs):
        name = kwargs.get('name', "LOGGER")
        filename = kwargs.get('filename', 'hello_world.log')
        root = logging.getLogger(name)
        root.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)
        logging.basicConfig(filename=filename, level=logging.INFO)
        return root
