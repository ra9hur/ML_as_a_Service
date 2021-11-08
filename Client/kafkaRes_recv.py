#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 21:34:14 2021

@author: raghu
"""

import json 
from kafka import KafkaConsumer


if __name__ == '__main__':
    
    # Kafka Consumer 
    consumer = KafkaConsumer(
        'res_predict',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest'
    )
   
    for message in consumer:
        print(json.loads(message.value))
        
