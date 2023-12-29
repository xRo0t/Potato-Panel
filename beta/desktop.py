import os
from PyQt5.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QVBoxLayout, 
    QFileSystemModel, 
    QListView, 
    QMessageBox,
    QInputDialog,
    QMenu
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from menus import FileMenu
from desktop_list_view import DesktopListView, FixedSizeDelegate

class Desktop(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowState(Qt.WindowFullScreen)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint | Qt.Tool)

        self.init_ui()
        self.setStyleSheet("background-color:#212121;")

        #self.setStyleSheet("background-color: #191919;color:white;border-style:hidden:")

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create a context menu for the list view
        self.context_menu = FileMenu(self)

        # Create a context menu for the desktop
        self.desktop_menu = QMenu(self)

        # Add actions to the desktop menu
        self.desktop_menu.addAction("Create Folder", self.context_menu.create_folder)
        self.desktop_menu.addAction("Create File", self.context_menu.create_file)

        background_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "girl.jpg")
        background_image = QPixmap(background_image_path)
        central_widget.setStyleSheet(f"background-image: url({background_image_path}); background-repeat: no-repeat; background-position:center;")

        self.model = QFileSystemModel()
        self.model.setRootPath(os.path.expanduser("~"))
        self.list_view = DesktopListView(self.context_menu, self, self)
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(os.path.expanduser("~/Desktop")))
        self.list_view.setIconSize(QSize(80, 80))
        self.list_view.setViewMode(QListView.IconMode)

        delegate = FixedSizeDelegate(self.list_view)
        self.list_view.setItemDelegate(delegate)

        # Connect the itemClicked signal to a custom slot
        self.list_view.doubleClicked.connect(self.handle_item_click)

        layout.addWidget(self.list_view)

        # Set the context menu for the list view
        self.list_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.list_view.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        # Get the currently selected item
        selected_indexes = self.list_view.selectedIndexes()

        if not selected_indexes:
            return

        # Check if all selected items are either files or directories
        all_files = all(self.model.fileInfo(index).isFile() for index in selected_indexes)
        all_directories = all(self.model.fileInfo(index).isDir() for index in selected_indexes)

        # Enable or disable the "Open" and "Delete" actions based on the selection
        self.context_menu.open_action.setEnabled(len(selected_indexes) == 1 and (all_files or all_directories))
        self.context_menu.delete_action.setEnabled(all_files or all_directories)

        # Show the context menu at the specified position
        self.context_menu.exec_(self.list_view.mapToGlobal(position))

    def handle_item_click(self, index):
        # Get the file path of the clicked item
        file_path = self.model.filePath(index)

        # Use xdg-open to open the file or folder with the default application
        os.system(f'xdg-open "{file_path}"')