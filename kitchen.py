
import sys

import pika
from pika.spec import BasicProperties
from pika.credentials import PlainCredentials

def create(locations):
    connection = connect('guest', 'guest')
    channel = connection.channel()
    channel.exchange_declare(exchange='orders', type='direct', durable=True)
    channel.exchange_declare(exchange='failed_orders', type='fanout', durable=True)
    channel.queue_declare(queue='failed_orders', durable=True)
    channel.queue_bind('failed_orders', 'failed_orders')
    
    for location in locations:
        channel.queue_declare(queue='chef@{}'.format(location), 
                              durable=True,
                              arguments = { 'x-dead-letter-exchange': 'failed_orders' })
        channel.queue_bind(queue='chef@{}'.format(location), exchange='orders', routing_key=location)

def connect(username, password='foobar'):
    return pika.BlockingConnection(parameters=pika.ConnectionParameters(credentials=PlainCredentials(username=username, password=password)))

if __name__ == "__main__":
    create(sys.argv[1:])

