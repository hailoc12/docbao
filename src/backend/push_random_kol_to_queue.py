#################################################################################
# Program: Push random kol_id to SMCC_IN_QUEUE to get kol posts in mail crawling
# Author: hailoc12
# Created: 2019-09-02
#################################################################################

from lib.rabbitmq_client import *
from time import sleep

TIME = 10

# push random kols to kols in queue to get them in the next time
while True:
    try:
        rb = RabbitMQ_Client()
        rb.connect()
        base_path = '..'
        while True:
            rb.push_random_kols_to_queue(base_path, number=1)
            sleep(TIME)
        rb.disconnect()
    except:
        print("Some error has happended. Restart")
        sleep(TIME)


