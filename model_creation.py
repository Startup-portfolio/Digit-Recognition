import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow import keras
from keras.datasets import mnist
from PIL import Image

(x_train, y_train), (x_test, y_test) = mnist.load_data() #loading data

x_train = x_train / 255.0
x_test = x_test / 255.0

model = keras.Sequential([ #creating model
        keras.layers.Flatten(input_shape=(28,28)),
        keras.layers.Dense(128, activation="relu"), #128 layers
        keras.layers.Dense(10, activation="softmax") #10 output layers
        ])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=15)

model.save("model.h5")
