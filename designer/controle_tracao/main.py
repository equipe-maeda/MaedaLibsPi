from PyQt5 import QtCore, QtGui, QtWidgets
from main_frame import Ui_MainWindow

class Main(Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.actionSair.triggered.connect(MainWindow.close)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Main()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())