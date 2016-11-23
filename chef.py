
import sys, signal
from multiprocessing import Pool
import kitchen
from random import randint

def chef(location):
    connection = kitchen.connect('chef')
    try:
        channel = connection.channel()
        for method, properties, body in channel.consume('chef@{}'.format(location)):
            if randint(0,5) == 0:
                print "Dropped it on the floor!"
                channel.basic_nack(method.delivery_tag, False, not method.redelivered)
            else:
                print body
                channel.basic_ack(method.delivery_tag)
    finally:
        connection.close()

if __name__ == "__main__":
    locations = sys.argv[1:]
    pool = Pool(3*len(locations))

    try:
        pool.map(chef, [x for x in locations for _ in range(3)])
        pool.close()
    finally:
        print "Joining pool"
        pool.join()



