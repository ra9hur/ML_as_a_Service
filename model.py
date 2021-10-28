#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 27 12:38:44 2021

@author: raghu
"""


# baseline cnn model for fashion mnist
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv2D
from tensorflow.python.keras.layers import MaxPooling2D
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.layers import Flatten
import os
import yaml


# gpus = tf.config.experimental.list_physical_devices('GPU')
# if gpus:
#     try:
#         # Currently, memory growth needs to be the same across GPUs
#         for gpu in gpus:
#             tf.config.experimental.set_memory_growth(gpu, True)
#             logical_gpus = tf.config.experimental.list_logical_devices('GPU')
#             print(len(gpus), len(logical_gpus))
#     except RuntimeError as e:
#         # Memory growth must be set before GPUs have been initialized
#         print(e)


# ---------------- Load configuration parameters ------------

config_path = "./Configs"
config_name = "config.yaml"

with open(os.path.join(config_path, config_name)) as file:
    config = yaml.safe_load(file)

data_dir = config["data_dir"]
weights_dir = config["weights_dir"]
train_csv = config["train_csv"]
test_csv = config["test_csv"]
train_file = data_dir+train_csv
test_file  = data_dir+test_csv

NUM_CLASSES = config["NUM_CLASSES"]
IMG_ROWS = config["IMG_ROWS"]
IMG_COLS = config["IMG_COLS"]
TEST_SIZE = config["TEST_SIZE"]
BATCH_SIZE = config["BATCH_SIZE"]
NUM_EPOCHS = config["NO_EPOCHS"]


# ---------------- Load Data ----------------------------------------

# Function to load data
def load_dataset(raw):
    num_images = raw.shape[0]
    x_as_array = raw.values[:,1:]

    # reshape dataset to have a single channel
    out_x = x_as_array.reshape(num_images, IMG_ROWS, IMG_COLS, 1)

    # one hot encode target values
    out_y = to_categorical(raw.label, NUM_CLASSES)
    return out_x, out_y


# ---------------- Pre-process Images -------------------------------

# scale pixels
def pre_process(data):

	# convert from integers to floats
	data_norm = data.astype('float32')

	# normalize to range 0-1
	data_norm = data_norm / 255.0

	# return normalized images

	return data_norm


# ---------------- define cnn model -------------------------------

def define_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(IMG_ROWS, IMG_COLS, 1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
    model.add(Flatten())
    model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
    model.add(Dense(NUM_CLASSES, activation='softmax'))
    
    # compile model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model


# ---------------- train model ----------------------------------

def train_model():
    
    # Load data
    train_data = pd.read_csv(train_file)
    trainX, trainY = load_dataset(train_data)
    
    # Pre-process data
    trainX = pre_process(trainX)
    
    # Split training data for validation
    trainX, valX, trainY, valY = train_test_split(trainX, trainY, test_size=TEST_SIZE, random_state=2018)

	# define model
    model = define_model()
    
    trained_model = model.fit(trainX, trainY,
                  batch_size=BATCH_SIZE,
                  epochs=NUM_EPOCHS,
                  verbose=0,
                  validation_data=(valX, valY))
    
    # Save weights
    wt_file = weights_dir + '/trained_weights.h5'
    model.save_weights(wt_file)
    
    #hist = trained_model.history
    #return hist['loss'], hist['val_loss'], hist['accuracy'], hist['val_accuracy']
    
    return trained_model.history
    
    
# ---------------- evaluate model -------------------------------

def evaluate_model():

    # Load data
    test_data = pd.read_csv(test_file)
    testX, testY = load_dataset(test_data)
    
    # Pre-process data
    testX = pre_process(testX)

	# define model
    model = define_model()

    # Load trained weights
    wt_file = weights_dir + '/trained_weights.h5'
    model.load_weights(wt_file)
    
    # Evaluate the model
    _, acc = model.evaluate(testX, testY, verbose=0)
    
    return ' %.3f' % (acc * 100.0)
    



# entry point, if run from the prompt
if __name__ == "__main__":
    
    #loss, val_loss, acc, val_acc = train_model()
    #print("Loss: ", loss, "Validation_Loss: ", val_loss, "Training Accuracy: ", acc, "Validation_Accuracy: ", val_acc)
    
    print(train_model())
    
    eval_acc = evaluate_model()
    
    print("Evaluation Accuracy: ", eval_acc)
    
    
    