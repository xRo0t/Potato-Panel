#import os
from PyQt5.QtWidgets import QApplication
from desktop import Desktop

if __name__ == '__main__':
    app = QApplication([])
    DesktopMG = Desktop()
    DesktopMG.show()
    app.exec_()
