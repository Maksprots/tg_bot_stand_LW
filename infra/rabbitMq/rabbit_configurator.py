
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('127.0.0.1', '15672')
)

channel = connection.channel()
channel.queue_declare(queue='alala')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
connection.close()

