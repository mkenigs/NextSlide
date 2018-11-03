import sys
import transcription
from PyQt5 import QtCore, QtGui, QtWidgets

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("NextSlide")
        self.show()


if __name__ == '__main__':
   transcription.main()
	# app = QtWidgets.QApplication(sys.argv)
	# GUI = Window()
	# sys.exit(app.exec_())
