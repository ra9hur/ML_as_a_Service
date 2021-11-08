#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 21:32:48 2021

@author: raghu
"""

import logging

logging.basicConfig(filename='../project.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

import time 
import json 
import random
from kafka import KafkaProducer

logging.info("kafkaRes_send BEGIN")

# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode('utf-8')


def send_response(result):
    # Kafka Producer
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=serializer
    )

    logging.info("kafkaRes_send.send_response - sending response")
    producer.send('res_predict', result)
    logging.info("kafkaRes_send.send_response - response sent successfully")

    # Sleep for a random number of seconds
    time_to_sleep = random.randint(1, 11)
    time.sleep(time_to_sleep)


logging.info("kafkaRes_send END")
