import pika

import bot.config as cf


class RabbitConf:
    def __init__(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(cf.RABBIT_HOST)
        )

        self.channel = connection.channel()

    def __delete__(self, instance):
        self.connection.close()

    def declare_queues(self):
        self.channel.queue_declare(queue='unit_1')
        self.channel.queue_declare(queue='unit_2')
        self.channel.queue_declare(queue='unit_3')
        self.channel.queue_declare(queue='De1Soc_1')
        self.channel.queue_declare(queue='De10Standart_1')

    def declare_exchanges(self):
        self.channel.exchange_declare(exchange='De10Lite',
                                      exchange_type='x-random')
        self.channel.exchange_declare(exchange='De10Standart',
                                      exchange_type='x-random')
        self.channel.exchange_declare(exchange='De1Soc',
                                      exchange_type='x-random')

    def bind_q2exchange(self):
        self.channel.queue_bind(exchange='De10Lite',
                                queue='unit_1')
        self.channel.queue_bind(exchange='De10Lite',
                                queue='unit_2')
        self.channel.queue_bind(exchange='De10Lite',
                                queue='unit_3')
        self.channel.queue_bind(exchange='De1Soc',
                                queue='De1Soc_1')
        self.channel.queue_bind(exchange='De10Standart',
                                queue='De10Standart_1')


if __name__ == "__main__":
    configer = RabbitConf()
    configer.declare_queues()
    configer.bind_q2exchange()
