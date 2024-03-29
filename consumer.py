import pika
from threading import Thread


def callback(ch, method, properties, body):
    print(" [x] Received %r" % (body,))


def read(name):
    credential = pika.PlainCredentials('admin', 'xxxxxxx')
    connection = pika.BlockingConnection(pika.ConnectionParameters('1.1.1.1', 5672, '/', credential))
    channel = connection.channel()
    queue_name = 'queue #%s' % name
    channel.basic_consume(on_message_callback=callback,
                          queue=queue_name,
                          auto_ack=True)
    channel.start_consuming()


class MyThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name

    def run(self):
        read(self.name)


def create_threads():
    for i in range(100):
        my_thread = MyThread(i)
        my_thread.start()
        
def func():
    pass


def empty_func():
    pass


if __name__ == "__main__":
    create_threads()
