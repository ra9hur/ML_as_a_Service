import logging

logging.basicConfig(filename='../project.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

import os
import sys
import cv2
from google.cloud import pubsub_v1

logging.info("psReq_send BEGIN")

credentials_path = '../key.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path


publisher = pubsub_v1.PublisherClient()
topic_path = 'projects/lively-arc-330715/topics/req_predict'


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

#future = publisher.publish(topic_path, data, **attributes)
logging.info("Client - sending message")
future = publisher.publish(topic_path, buffer.tobytes())
print(f'published message id {future.result()}')
logging.info(f'Client - published message id {future.result()}')

logging.info("psReq_send END")

