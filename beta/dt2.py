from dtm import *

class DesktopListView(QListView):
    def __init__(self, context_menu, desktop_menu, parent=None):
        super().__init__(parent)
        self.context_menu = context_menu
        self.desktop_menu = desktop_menu

    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        if event.button() == Qt.RightButton:
            if not index.isValid():
                self.clearSelection()
                self.context_menu.hide()
                self.desktop_menu.exec_(self.mapToGlobal(event.pos()))
            else:
                super().mousePressEvent(event)
        elif event.button() == Qt.LeftButton:
            if not index.isValid():
                self.clearSelection()
                self.context_menu.hide()
            else:
                super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        drop_position = event.pos()
        print(f"Item dropped at position: {drop_position}")

        super().dropEvent(event)

class FixedSizeDelegate(QStyledItemDelegate):
    def sizeHint(self, option, index):
        return QSize(100, 100)  # Set a custom size for each item (adjust as needed)
    
class MdiAreaWithBackground(QMdiArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.background_image = QPixmap("artwork-digital-art-room-window-sunset-2246552-wallhere.com.jpg")  # Replace with the actual path to your image

    def paintEvent(self, event):
        painter = QPainter(self.viewport())
        painter.drawPixmap(self.viewport().rect(), self.background_image)

class Desktop(QMainWindow):
    def __init__(self): 
        super().__init__()

        #self.setWindowState(Qt.WindowFullScreen)
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint | Qt.Tool)

        self.init_ui()
        self.setStyleSheet("background-color: #191919;color:white;border-style:hidden;background-color: transparent;")
        #self.setAttribute(Qt.WA_TranslucentBackground)

    def init_ui(self):

        central_widget = MdiAreaWithBackground(self)


        #central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setSpacing(0)  # Set spacing to zero
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a context menu for the list view
        self.context_menu = QMenu(self)

        # Add a "Open" action to the context menu
        self.open_action = QAction("Open", self)
        self.open_action.triggered.connect(self.open_selected_item)
        self.context_menu.addAction(self.open_action)

        # Add a "Delete" action to the context menu
        self.delete_action = QAction("Delete", self)
        self.delete_action.triggered.connect(self.delete_selected_items)
        self.context_menu.addAction(self.delete_action)

        # Create a context menu for the desktop
        self.desktop_menu = QMenu(self)

        # Add actions to the desktop menu
        self.desktop_menu.addAction("Create Folder", self.create_folder)
        self.desktop_menu.addAction("Create File", self.create_file)
        self.setGeometry(0,0,0,0)
        """self.bk_img = "girl.jpg"
        background_image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.bk_img)
        background_image = QPixmap(background_image_path)
        central_widget.setStyleSheet(f"background-image: url({background_image_path}); background-repeat: no-repeat; background-position:center;")
"""
        self.model = QFileSystemModel()
        self.model.setRootPath(os.path.expanduser("~"))
        self.list_view = DesktopListView(self.context_menu, self.desktop_menu, self)
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
        self.open_action.setEnabled(len(selected_indexes) == 1 and (all_files or all_directories))
        self.delete_action.setEnabled(all_files or all_directories)

        # Show the context menu at the specified position
        self.context_menu.exec_(self.list_view.mapToGlobal(position))

    def open_selected_item(self):
        # Get the currently selected item
        selected_indexes = self.list_view.selectedIndexes()

        if not selected_indexes:
            return

        # Get the file path of the selected item
        file_path = self.model.filePath(selected_indexes[0])

        # Use xdg-open to open the file or folder with the default application
        os.system(f'xdg-open "{file_path}"')

    def delete_selected_items(self):
        # Get the currently selected items
        selected_indexes = self.list_view.selectedIndexes()

        if not selected_indexes:
            return

        # Confirm deletion with a QMessageBox
        msg_box = QMessageBox(QMessageBox.Warning, "Confirm Deletion", "Are you sure you want to delete the selected item(s)?", QMessageBox.Yes | QMessageBox.No, self)
        result = msg_box.exec_()

        if result == QMessageBox.Yes:
            for index in selected_indexes:
                file_path = self.model.filePath(index)

                # Use shutil to remove both files and directories
                try:
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    else:
                        os.remove(file_path)

                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

    def handle_item_click(self, index):
        # Get the file path of the clicked item
        file_path = self.model.filePath(index)

        # Use xdg-open to open the file or folder with the default application
        os.system(f'xdg-open "{file_path}"')

    def create_folder(self):
        
        # Get the name for the new folder from the user
        folder_name, ok = QInputDialog.getText(self, "Create Folder", "Enter folder name:")

        if ok and folder_name:
            # Create the new folder
            folder_path = os.path.join(os.path.expanduser("~/Desktop"), folder_name)
            try:
                os.makedirs(folder_path)
                QMessageBox.information(self, "Success", "Folder created successfully!")
            except OSError as e:
                QMessageBox.warning(self, "Error", f"Failed to create folder: {e}")

    def create_file(self):
        # Get the name for the new file from the user
        file_name, ok = QInputDialog.getText(self, "Create File", "Enter file name:")

        if ok and file_name:
            # Create the new file
            file_path = os.path.join(os.path.expanduser("~/Desktop"), file_name)
            with open(file_path, "w") as file:
                file.write("")
            QMessageBox.information(self, "Success", "File created successfully!")

if __name__ == '__main__':
    app = QApplication([])
    file_manager = Desktop()
    file_manager.show()
    app.exec_()



#last done