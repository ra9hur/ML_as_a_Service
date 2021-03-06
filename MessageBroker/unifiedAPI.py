#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 10:34:57 2021

@author: raghu
"""

#import asyncio
from concurrent.futures import ProcessPoolExecutor
import sys
import os
import multiprocessing
import json
import logging

logging.basicConfig(filename='../project.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


# In later versions
# To have a function to processes input data and place them in the required folders. 
# For instance, if the request is to refine the model with further training using additional input images, 
# the request_handler moves these images to the specified folder so that ML service can pick them up for training.



# # Receives requests with ID details from Kafka and Sub / Pub. 
def request_handler(identifier, data):

    logging.info("unifiedAPI.request_handler - BEGIN")
    print("unifiedAPI.request_handler PID {}".format(os.getpid()))
    logging.info("unifiedAPI.request_handler PID {}".format(os.getpid()))

    # Passes input details along with the ID to the model. 
    # ID serves as an identifier and carries requester details.

    sys.path.insert(1, '../Model')
    from model import model_request

    logging.info("unifiedAPI.request_handler - model.model_request initiating")
    
    model_request(identifier, data)
    logging.info("unifiedAPI.request_handler - model.model_request successful")
    logging.info("unifiedAPI.request_handler - END")




#REF: Python Multiprocessing Tutorial: Run Code in Parallel Using the Multiprocessing Module - Corey Schafer
#REF: https://www.youtube.com/watch?v=fKl2JW_qrso
#REF: https://tutorialedge.net/python/concurrency/python-processpoolexecutor-tutorial/
# The process_request initiates an asynchronous (fire and forget) call to ML service.
# def process_request(identifier, data):

#     logging.info("unifiedAPI.process_request - BEGIN")
#     logging.info("Executing our Task on Process {}".format(os.getpid()))
 	
#     p = multiprocessing.Process(target = request_handler, args = (identifier, data))
#     p.start()
 	
#     logging.info("unifiedAPI.process_request - END")




#REF: Python Multiprocessing Tutorial: Run Code in Parallel Using the Multiprocessing Module - Corey Schafer
#REF: https://www.youtube.com/watch?v=fKl2JW_qrso
# The process_request initiates an asynchronous (fire and forget) call to ML service.
def process_request(identifier, data):

    logging.info("unifiedAPI.process_request - BEGIN")
    print("unifiedAPI.process_request PID {}".format(os.getpid()))
    logging.info("unifiedAPI.process_request {}".format(os.getpid()))
 	
    #request_handler(identifier, data)
    with ProcessPoolExecutor() as executor:
        executor.submit(request_handler, identifier, data)
 	
    logging.info("unifiedAPI.process_request - END")






# Response collects results from the ML service along with the ID. 
# Based on the ID, this function either publishes to Kafka or Pub / Sub.
def response_handler(identifier, result):
    
    logging.info("unifiedAPI.response_handler - BEGIN")
    # print("unifiedAPI.response_handler PID {}".format(os.getpid()))
    # logging.info("unifiedAPI.response_handler {}".format(os.getpid()))
    
    if (identifier["msg_broker"] == "kafka"):
        from kafkaRes_send import send_response
        
        logging.info("unifiedAPI.response_handler - kafkaRes_send.send_response initiating")        
        send_response(result)
        logging.info("unifiedAPI.response_handler - kafkaRes_send.send_response successful")
    
    elif (identifier["msg_broker"] == "PubSub"):
        from psRes_send import send_response
        
        logging.info("unifiedAPI.response_handler - psRes_send.send_response initiating")
        
        with open('result_file.json', 'w') as rfile:
            json.dump(result, rfile)
        
        #send_response(result)
        #exec(open('psRes_send.py').send_response(result))
        os.system("python psRes_send.py")

        logging.info("unifiedAPI.response_handler - psRes_send.send_response successful")

    logging.info("unifiedAPI.response_handler - END")



# def process_response(identifier, result):

#     logging.info("unifiedAPI.process_response - BEGIN")
#     print("unifiedAPI.process_response PID {}".format(os.getpid()))
#     logging.info("unifiedAPI.process_response {}".format(os.getpid()))
 	
#     #request_handler(identifier, data)
#     with ProcessPoolExecutor() as executor:
#         executor.submit(response_handler, identifier, result)
 	
#     logging.info("unifiedAPI.process_response - END")




if __name__ == "__main__":

    identifier = {"msg_broker": "PubSub"}

    result = {'7': '???Sneaker???'}

    from psRes_send import send_response
    response_handler(identifier, result)