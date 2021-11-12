#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 22:28:29 2021

@author: raghu
"""

from PIL import Image
from io import BytesIO
from kafka import KafkaConsumer

import logging

logging.basicConfig(filename='../project.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

logging.info("kafkaReq_recv BEGIN")

import sys
sys.path.insert(1, '../MessageBroker')
from unifiedAPI import process_request


identifier = dict()
identifier["msg_broker"] = "kafka"
identifier["topic"] = "req_predict"

consumer = KafkaConsumer(identifier["topic"], bootstrap_servers=['localhost:9092'],
                        api_version=(0,10,1))

for message in consumer:
    stream = BytesIO(message.value)
    #image = Image.open(stream).convert("RGBA")
    image = Image.open(stream).convert('L')
    
    
    # Pass input and identifier to unifiedAPI
    logging.info("kafka:req_predict - unifiedAPI.process_request initiating")
    process_request(identifier, image)
    logging.info("kafka:req_predict - unifiedAPI.process_request successful")
    
    stream.close()
    image.show()


logging.info("kafkaReq_recv END")
