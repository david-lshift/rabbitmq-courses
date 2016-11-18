
# Copyright (C) LShift, all rights reserved
# WARNING: this code is an example in a course. Don't use it as a production example.

import pika
from pika.spec import BasicProperties
from uuid import uuid4

connection = pika.BlockingConnection()
channel = connection.channel()

def service(channel):
    # This is obviously going to leak memory... It's just an arbitrary way to
    # illustrate idempotent behaviour
    requests = {}
    channel.queue_declare(queue='service', durable=True)
    channel.confirm_delivery()
    for method, properties, body in channel.consume('service'):
        id = properties.correlation_id
        if not requests.has_key(id):
            requests[id] = body
            print body
        if channel.basic_publish(
            exchange='', 
            routing_key=properties.reply_to,
            body='Response',
            properties=BasicProperties(
                reply_to=responses,
                delivery_mode=2,
                correlation_id=id)):
            channel.basic_ack(method.delivery_tag)


def send_request(channel, timeout=1.0, id=None):
    id = id or str(uuid4())
    channel.confirm_delivery()
    # We use a durable queue named after the request. It's only allowable to call this
    # function again with the same id.
    responses = channel.queue_declare(queue='service-response-{}'.format(id), durable=True).method.queue
    consume = channel.consume(responses, inactivity_timeout=timeout, exclusive=True)
    try:
        if channel.basic_publish(
            exchange='',
            routing_key='service',
            body='Request {}'.format(id),
            properties=BasicProperties(
                reply_to=responses,
                delivery_mode=2)):
            for response in consume:
                method, properties, body = response
                print body
                channel.basic_ack(method.delivery_tag)
                channel.queue_delete(responses)
                return True
            return False
        else:
            return False
    finally:
        channel.cancel()
