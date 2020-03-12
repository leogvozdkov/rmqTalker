import pika
import random
import string
from threading import Thread


def random_string_digits(string_length=10):
    """Generate a random string of letters and digits """
    content = string.ascii_letters + string.digits
    return ''.join(random.choice(content) for i in range(string_length))


def flood(name):
    credential = pika.PlainCredentials('leo', '28944982')
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.88.17', 5672, '/', credential))
    channel = connection.channel()
    queue_name = 'queue #%s' % name
    while True:
        channel.queue_declare(queue=queue_name)
        channel.basic_publish(exchange='',
                              routing_key=queue_name,
                              body=random_string_digits())


class MyThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        flood(self.name)


def create_threads():
    for i in range(100):
        my_thread = MyThread(i)
        my_thread.start()


if __name__ == "__main__":
    create_threads()
