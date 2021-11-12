# Machine Learning as a Service

----------
**1. Problem Definition - About Project**
-------------
Intent is to design and build a robust system to classify MNISTFashion images. Fashion classifier model will be utilised as a machine learning service. 

![high_level_arch](https://user-images.githubusercontent.com/17127066/140688601-ed31bdfb-fafd-47be-b03d-e416a8fe2a9a.jpg )

The system will have a single client consuming a single machine learning service. The client sends and receives messages to/from the ML service through a message broker (Kafka / Google PubSub).


----------
 **2. Required packages**
-------------

1. cudatoolkit              10.1.243
2. cudnn                    7.6.5
3. h5py                     2.10.0
4. kafka                    2.12-3.0.0
5. kafka-python             2.0.2
6. google-cloud-sdk         362.0.0
7. google-cloud-pubsub
8. keras-preprocessing      1.1.2
9. matplotlib               3.4.3
10. numpy                    1.21.2
11. opencv                  4.5.0 
12. pandas                  1.3.4
13. pillow                  8.4.0
14. python                  3.9.7
15. scikit-learn            1.0.1
16. scipy                   1.7.1
17. tensorflow-gpu          2.4.1


----------
 **3. How to run**
-------------

The reference dataset being considered is MNISTFashion Dataset and can be downloaded from [here](https://www.kaggle.com/zalando-research/fashionmnist). 


***Kafka: steps to execute:***

Open 3 terminals to execute scripts as mentioned below.
1. Start zookeeper and kafka services.
2. Create topics: req_predict and res_predict
3. Terminal 1: Change directory to Client and run,
    
    ‘python kafkaReq_send.py sandal5.png’ 
    
    to send a predict_model request via Kafka message broker. One of the images from Client/Images folder can be selected as parameter. Default is sneaker7.png.
4. Terminal 2: Change directory to MessageBroker and run,
    
    'python kafkaReq_recv.py'
    
    to receive request for prediction.
    
    Note: If the model runs in a virtual environment, it should be activated.
5. Terminal 3: Change directory to Client and run,

    'python kafkaRes_recv.py'

    to receive predicted results.


***Google PubSub: steps to execute:***

Open 3 terminals to execute scripts as mentioned below.
1. Create a project and set-up a service account in the google cloud platform.
2. Create topics/subscritions: req_predict / req_predict-sub and res_predict / res_predict-sub
3. Terminal 1: Change directory to Client and run,
    
    ‘python psReq_send.py sandal5.png’ 
    
    to send a predict_model request via Kafka message broker. One of the images from Client/Images folder can be selected as parameter. Default is sneaker7.png.
4. Terminal 2: Change directory to MessageBroker and run,
    
    'python psReq_recv.py'
    
    to receive request for prediction.
    
    Note: If the model runs in a virtual environment, it should be activated.

5. Terminal 3: Change directory to Client and run,

    'python psRes_recv.py'

    to receive predicted results.


----------
 **4. Implementation**
-------------

![data-flow_diagram](https://user-images.githubusercontent.com/17127066/140695718-dca40779-5ad4-4e4c-815e-37044fffcb91.jpg)

Here is the list of files used.

Client
 - kafkaReq_send.py / psReq_send.py: Client uses this script to send a predict_model request via message broker (Kafka / PubSub). An image is sent as an input to the trained model.
 - Images/: One of the images in this folder can be used as an input for prediction.
 - kafkaRes_recv.py / psRes_recv.py: Client uses this script to receive the predicted result. 

MessageBroker
 - kafkaReq_recv.py / psReq_recv.py: This script is used to receive request for prediction. An image is received as an input along with the request.
 - kafkaRes_send.py / psRes_send.py: This script is used to send the predicted result to the client via message broker (Kafka / PubSub).
 - unifiedAPI.py: This scripts the requests received from message brokers. The requests are forwarded to the model for further processing. A new process is created to initiate an asynchronous request to the model. 

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

To test end-to-end, a simple scenario - predict the model given an image as input, is considered. This works for both Kafka & PubSub message brokers.

----------
 **6. Further Improvements**
-------------

1. There is further scope to improve the model accuracy
2. Support end-to-end for all functionality of the model.


----------
 **7. References**
-------------

1. [Dataset Download](https://www.kaggle.com/zalando-research/fashionmnist)
2. [Python Multiprocessing - Corey Schafer](https://www.youtube.com/watch?v=fKl2JW_qrso)
3. [Python Multiprocessing - TutorialEdge](https://tutorialedge.net/python/concurrency/python-processpoolexecutor-tutorial/)
4. [Producer sending an image issue](https://github.com/dpkp/kafka-python/issues/1045)
