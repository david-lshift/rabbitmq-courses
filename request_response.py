
# Copyright (C) LShift, all rights reserved
# WARNING: this code is an example in a course. Don't use it as a production example.

import pika
from pika.spec import BasicProperties

connection = pika.BlockingConnection()
channel = connection.channel()

def service(channel):
    channel.queue_declare(queue='service', auto_delete=True)
    for method, properties, body in channel.consume('service'):
        print body
        channel.basic_publish(exchange='', 
                              routing_key=properties.reply_to,
                              body='Response')
        channel.basic_ack(method.delivery_tag)


def send_request(channel):
    responses = channel.queue_declare(exclusive=True).method.queue
    try:
        channel.basic_publish(exchange='',
                              routing_key='service',
                              body='Request', 
                              properties=BasicProperties(reply_to=responses))
        consume = channel.consume(responses)
        try:
            method, properties, body = next(consume)
            print body
            channel.basic_ack(method.delivery_tag)
        finally:
            channel.cancel()
    finally:
        channel.queue_delete(responses)
