import sys
from main_window import *

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()

if __name__ == "__main__":
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
