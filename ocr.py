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
from keras.datasets import mnist

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "Paint Application"
        top = 400
        left = 400
        width = 800
        height = 600

        self.setWindowTitle(title)
        self.setGeometry(top, left, width, height)
        self.widget = QWidget(self)
        self.widget.move(100, 100)
        self.image = QImage(QSize(280, 280), QImage.Format_RGB32)
        self.pix = QPixmap().fromImage(self.image)
        self.pix = self.pix.copy(100, 0, 280, 280)
        self.image.fill(Qt.white)
        #self.image.resize(280, 280)
        self.drawing = False
        self.brushSize = 4
        self.brushColor = Qt.black
        self.lastPoint = QPoint()
        self.submit = QPushButton('Submit', self)
        self.submit.move(300, 300)
        self.submit.clicked.connect(self.save)
        self.clear = QPushButton('Clear', self)
        self.clear.move(400, 300)
        self.clear.clicked.connect(self.erase)
        self.prediction = QLabel("Prediction: ", self)
        self.prediction.move(350, 400)

    def save(self):
        self.image.save("image.png")
        self.image2 = Image.open("image.png")
        self.image2 = self.image2.resize((28,28),Image.ANTIALIAS)
        self.image2.save("image.png")
        self.prediction.setText('Prediction: ' + str(self.predict()))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            #print(self.lastPoint)

    def mouseMoveEvent(self, event):
        if(event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False


    def paintEvent(self, event):
        canvasPainter  = QPainter(self)
        canvasPainter.drawImage(self.image.rect(), self.image, self.image.rect() )


    def erase(self):
        self.image.fill(Qt.white)
        self.update()

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.createModel()
    window.show()
    app.exec()
