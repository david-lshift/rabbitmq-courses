
from random import choice
from time import sleep
from order import *
from multiprocessing import Pool

def customers(locations):
    while True:
        order(choice(locations))
        sleep(0.001)

if __name__ == "__main__":
    locations=sys.argv[1:]
    pool = Pool(3)
    pool.map(customers, [locations for x in range(3)])
    pool.close()
    print "Joining pool"
    pool.join()

