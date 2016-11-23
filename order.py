
# Copyright (C) LShift, all rights reserved
# WARNING: this code is an example in a course. Don't use it as a production example.

import sys
import pika
from pika.spec import BasicProperties
from pika.credentials import PlainCredentials
from random import choice
import kitchen

CURRIES=[
    'Achari',
    'Balti',
    'Bhindi Ghosht',
    'Bhuna',
    'Biryani',
    'Bombay',
    'Ceylon',
    'Dahi Wala',
    'Dhaba Curry',
    'Dhansak',
    'Dhansak',
    'Do Piyaz',
    'Haleem',
    'Jaipur',
    'Jalfrezi',
    'Jungli Mas',
    'Karahi',
    'Kashmir'
    ]

def order(locations):
    connection = kitchen.connect('customer')
    try:
        channel = connection.channel()
        channel.confirm_delivery()
    
        # responses = channel.queue_declare(exclusive=True).method.queue
        responses=''
        try:
            if channel.basic_publish(exchange='orders',
                                     routing_key=choice(locations),
                                     body=choice(CURRIES),
                                     properties=BasicProperties(reply_to=responses)):
                print "Order sent"
            else:
                print "Order not sent"
        finally:
            pass
            # channel.queue_delete(responses)
    finally:
        connection.close()
        
if __name__ == "__main__":
    order(sys.argv[1:])
