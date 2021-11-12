import os
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

import logging

logging.basicConfig(filename='../project.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

logging.info("psRes_recv BEGIN")

credentials_path = '../key.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

# timeout in seconds
timeout = 5.0

subscriber = pubsub_v1.SubscriberClient()
subscription_path = 'projects/lively-arc-330715/subscriptions/res_predict-sub'


def callback(message):
    print(f'Received message: {message}')
    print(f'data: {message.data}')

    if message.attributes:
        print("Attributes:")
        for key in message.attributes:
            value = message.attributes.get(key)
            print(f"{key}: {value}")

    message.ack()           


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f'Listening for messages on {subscription_path}')


# wrap subscriber in a 'with' block to automatically call close() when done
with subscriber:                                                
    try:
        # streaming_pull_future.result(timeout=timeout)
        # going without a timeout will wait & block indefinitely
        streaming_pull_future.result()
    except TimeoutError:
    	# trigger the shutdown
        streaming_pull_future.cancel()
        # block until the shutdown is complete
        streaming_pull_future.result()

logging.info("psRes_recv END")

