from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen, QBrush, QPixmap
from PyQt5.QtCore import Qt, QPoint, QSize, QRect
import sys

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
        self.brushSize = 2
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
        self.image.save("image.jpeg")
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

    def predict(self):
        return "Hello"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
