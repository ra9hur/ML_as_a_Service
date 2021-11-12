import os
import sys
import json
from google.cloud import pubsub_v1

import logging

logging.basicConfig(filename='../project.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')
# filemode='w'  create a new log file for every new run. Old loggings are discarded.

logging.info("psRes_send BEGIN")

credentials_path = '../key.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


publisher = pubsub_v1.PublisherClient()
topic_path = 'projects/lively-arc-330715/topics/res_predict'

def send_response(res):

    logging.info("psRes_send.send_response - BEGIN")

    #print(res)

    data = 'prediction for the given input!'
    data = data.encode('utf-8')
    attributes = res
  
    try:
        logging.debug('in try block')
        logging.info("psRes_send.send_response - sending response")
        #publisher.publish(topic_path, data).result()
        future = publisher.publish(topic_path, data, **attributes).result()

        logging.debug("check check check")
        #logging.info(f'published message id {future}')
        logging.info(f"Published {data} to {topic_path}: {future}")

        logging.debug('try block done')
    except Exception as e:
        logging.error(e)

    logging.info("psRes_send.send_response - response sent successfully")
    
    logging.info("psRes_send.send_response - END")


logging.info("psRes_send END")


# entry point, if run from the prompt
if __name__ == "__main__":

    # n = len(sys.argv)
    # if (n > 1):
    #     result = sys.argv[1]
    # else:
    #     raise Exception("psRes_send: result not available")
    
    #result = {'7': '‘Sneaker’'}

    with open('result_file.json', 'r') as rfile:
        result = json.load(rfile)

    print(result)

    send_response(result)

