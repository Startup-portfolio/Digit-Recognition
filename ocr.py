import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt, QPoint, QSize, QRect
import sys
from PIL import Image
import tensorflow as tf
import matplotlib.pyplot as plt
from PIL import Image
from tensorflow import keras
from tensorflow.keras.datasets import mnist

class Widget1(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        self.lbl = QLabel(self)
        self.lbl.setGeometry(0, 0, 280, 280)
        self.lbl.setPixmap(QPixmap(QSize(280, 280)))
        self.lbl.pixmap().fill(Qt.white)
        lay.addWidget(self.lbl)
        self.drawing = False
        self.brushSize = 4
        self.brushColor = Qt.black
        self.lastPoint = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            #print(self.lastPoint)

    def mouseMoveEvent(self, event):
        if(event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.lbl.pixmap())
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter  = QPainter(self.lbl.pixmap())
        canvasPainter.drawPixmap(0, 0, self.lbl.pixmap())

class stackedExample(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        title = "Didgit Recognition"
        top = 400
        left = 400
        width = 500
        height = 400

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)

        self.Stack = Widget1(self)
        self.Stack.move((width/2-140), 20)

        btnClear = QPushButton("Clear", self)
        btnClear.clicked.connect(self.clear)
        btnClear.move((width/2-140), 360)
        btnSubmit = QPushButton("Submit", self)
        btnSubmit.clicked.connect(self.submit)
        btnSubmit.move((width/2-30), 360)

        self.prediction = QLabel(self)
        self.prediction.setText("Prediction: ")
        self.prediction.setGeometry((width/2-140), 320, 100, 30)

    def clear(self):
        self.Stack.lbl.pixmap().fill(Qt.white)
        self.update()

    def submit(self, other):
        self.Stack.lbl.pixmap().save("image.png")
        self.image2 = Image.open("image.png")
        self.image2 = self.image2.resize((28,28), Image.ANTIALIAS)
        self.image2.save("image.png")
        self.prediction.setText('Prediction: ' + str(self.predict()))

    def createModel(self):
        (x_train, y_train), (x_test, y_test) = mnist.load_data() #loading data

        x_train = x_train / 255.0
        x_test = x_test / 255.0

        self.model = keras.Sequential([ #creating model
            keras.layers.Flatten(input_shape=(28,28)),
            keras.layers.Dense(128, activation="relu"), #128 layers
            keras.layers.Dense(10, activation="softmax") #10 output layers
            ])

        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        self.model.fit(x_train, y_train, epochs=2) #train model

    def predict(self):
        self.im = Image.open("image.png").convert('L')  #convert image to 8-bit grayscal
        self.data = list(self.im.getdata())

        for i in range(len(self.data)):
            self.data[i] = 255 - self.data[i]

        self.data = [self.data[offset:offset+28] for offset in range(0, 784, 28)]
        self.assume = self.model.predict([self.data])

        return(str(self.assume[0].argmax()))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = stackedExample()
    w.createModel()
    w.show()
    sys.exit(app.exec_())

#Put it all to train data
#Save model
#Character dataset 
