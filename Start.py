#!/usr/bin/python3.6
import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen

from EnergyUse import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.processEvents()
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())