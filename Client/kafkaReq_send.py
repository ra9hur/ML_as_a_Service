#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 22:28:27 2021

@author: raghu
"""

# https://stackoverflow.com/questions/55526491/how-can-i-send-an-image-from-kafka-producer-in-python#

# https://github.com/dpkp/kafka-python/issues/1045


import logging

logging.basicConfig(filename='../project.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

from kafka import KafkaProducer
import cv2
import sys


logging.info("kafkaReq_send BEGIN")

producer=KafkaProducer(bootstrap_servers=['localhost:9092'],api_version=(0,10,1))

# CHANGE this to take image as an  input
n = len(sys.argv)
if (n > 1):
    image_path = "./Images/" + sys.argv[1]
    image = cv2.imread(image_path)
else:
    image = cv2.imread("./Images/sneaker7.png")

#cv2.imshow(image)
size = sys.getsizeof(image) / (1024 * 1024)
logging.info("Image byte size before:", size, "mb")

ret, buffer = cv2.imencode('.png', image)

size = sys.getsizeof(buffer) / (1024 * 1024)
logging.info("Buffer shape:", buffer.shape)
logging.info("Image byte size after:", size, "mb")

img = cv2.imdecode(buffer, cv2.IMREAD_GRAYSCALE)
logging.info("Buffer shape:", img.shape)

topic = "req_predict"

logging.info("Client - sending message")
producer.send(topic, buffer.tobytes())
logging.info("Client - message successfully sent")

producer.flush()

logging.info("kafkaReq_send END")

