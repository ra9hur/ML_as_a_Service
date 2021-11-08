# Machine Learning as a Service

----------
**1. Problem Definition - About Project**
-------------
Intent is to design and build a robust system to classify MNISTFashion images. Fashion classifier model will be utilised as a machine learning service. 

![high_level_arch](https://user-images.githubusercontent.com/17127066/140688601-ed31bdfb-fafd-47be-b03d-e416a8fe2a9a.jpg )

The system will have a single client consuming a single machine learning service. The client sends and receives messages to/from the ML service through a message broker.


----------
 **2. Required packages**
-------------



----------
 **3. How to run**
-------------

***Steps to execute:***

Open 3 terminals to execute scripts as mentioned below.
1. Start zookeeper and kafka services.
2. Terminal 1: Change directory to Client and run,
    
    ‘python kafkaReq_send.py sandal5.png’ 
    
    to send a predict_model request via Kafka message broker.
3. Terminal 2: Change directory to MessageBroker and run,
    
    'python kafkaReq_recv.py'
    
    to receive request for prediction.
    
    Note: If the model runs in a virtual environment, it should be activated.
4. Terminal 3: Change directory to Client and run,

    'python kafkaRes_recv.py'

    to receive predicted results.


----------
 **4. Implementation**
-------------

![data-flow_diagram](https://user-images.githubusercontent.com/17127066/140695718-dca40779-5ad4-4e4c-815e-37044fffcb91.jpg)

Here is the list of files used.

Client
 - kafkaReq_send.py: Client uses this script to send a predict_model request via Kafka message broker. An image is sent as an input to the trained model.
 - Images/: One of the images in this folder can be used as an input for prediction.
 - kafkaRes_recv.py: Client uses this script to receive the predicted result.

MessageBroker
 - kafkaReq_recv.py: This script is used to receive request for prediction. An image is received as an input along with the request.
 - kafkaRes_send.py: This script is used to send the predicted result to the client via Kafka.
 - unifiedAPI.py: This scripts the requests received from message brokers. The requests are forwarded to the model for further processing. Since A process is created to initiate an asynchronous request to the model. 

Configs
 - config.yaml: path to trainig data, weights. Also has parameters for the training.

Model
 - model.py: Includes functionality for training the model, testing the trained model and predict given an image.

Data
 - Training / Test data saved in this location

Weights
 - Trained weights are saved in this location

----------
 **5. Results**
-------------

***Model***:

For epoch=10, get the below results.

Training

    Loss = 0.136
    Training Accuracy = 0.9495 or 94.95%
    Validation Loss = 0.263
    Validation Accuracy = 0.9135 or 91.35%

Test

    Evaluation Accuracy = 91.57%


***End-to-end Integration***

To test end-to-end, a simple scenario - predict the model given an image as input, is considered. This works for Kafka message broker.

----------
 **6. Further Improvements**
-------------

1. There is further scope to improve the model accuracy
2. Google Pub/Sub is to be integrated.

----------
 **7. References**
-------------

