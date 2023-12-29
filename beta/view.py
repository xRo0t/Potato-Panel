import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class PotatoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout
        layout = QVBoxLayout(central_widget)

        # Create buttons
        button1 = QPushButton("Button 1", self)
        button2 = QPushButton("Button 2", self)

        # Create a QLabel for displaying the image
        label = QLabel(self)
        pixmap = self.get_scaled_pixmap("girl.jpg")
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)

        # Add buttons and label to the layout
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(label)

        # Set the z-order to make the label appear below the buttons
        label.stackUnder(button1)
        label.stackUnder(button2)

        self.setWindowTitle("Potato Window")
        self.setGeometry(100, 100, 800, 600)  # Set initial window size
        self.show()

    def get_scaled_pixmap(self, image_path):
        # Load the image from the file
        pixmap = QPixmap(image_path)

        # Scale the image to match the window size
        scaled_pixmap = pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatio)

        return scaled_pixmap


if __name__ == '__main__':
    app = QApplication(sys.argv)
    potato_window = PotatoWindow()
    sys.exit(app.exec_())
