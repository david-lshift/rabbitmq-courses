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
    channel.queue_declare(queue='service', auto_delete=True)
    channel.basic_qos(prefetch_count=10)
    for method, properties, body in channel.consume('service', no_ack=True):
        id = properties.correlation_id
        # Notice our idempotent test may not rely on the reply_to address, since this will
        # change if the requesters connection drops 
        if not requests.has_key(id):
            requests[id] = body
            print body
        channel.basic_publish(
            exchange='', 
            routing_key=properties.reply_to,
            body='Response {}'.format(id),
            properties=BasicProperties(correlation_id=id))

def send_request(channel, id=None, retries = 3, timeout=1.0):
    id = id or str(uuid4())
    # Our queue belongs to this process - we don't need it after the connection closes
    responses = channel.queue_declare(exclusive=True).method.queue
    try:
        consume = channel.consume(responses, inactivity_timeout=timeout, no_ack=True)
        try:
            # FIXME: this loop does not deal with a dropped connection
            for attempt in range(retries):
                channel.basic_publish(
                    exchange='',
                    routing_key='service',
                    body='Request {}'.format(id),
                    properties=BasicProperties(
                        reply_to=responses,
                        correlation_id=id))
                response = next(consume)
                if not response:
                    print "WARN: timeout"
                else:
                    method, properties, body = response
                    if id == properties.correlation_id:
                        print "{}: {}".format(id, body)
                        return True
                    else:
                        print "ERROR {}: unrecognised correlation_id {}".format(id, properties.correlation_id)
            print "ERROR: failed after {} retries".format(retries)
            return False
        finally:
            channel.cancel()
    finally:
        channel.queue_delete(responses)
