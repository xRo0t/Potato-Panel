from PyQt5.QtWidgets import QMenu, QAction, QMessageBox, QInputDialog
import os
import shutil

class FileMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Add a "Open" action to the context menu
        self.open_action = QAction("Open", parent)
        self.open_action.triggered.connect(self.open_selected_item)
        self.addAction(self.open_action)

        # Add a "Delete" action to the context menu
        self.delete_action = QAction("Delete", parent)
        self.delete_action.triggered.connect(self.delete_selected_items)
        self.addAction(self.delete_action)

    def open_selected_item(self):
        # Get the currently selected item
        selected_indexes = self.parent().list_view.selectedIndexes()

        if not selected_indexes:
            return

        # Get the file path of the selected item
        file_path = self.parent().model.filePath(selected_indexes[0])

        # Use xdg-open to open the file or folder with the default application
        os.system(f'xdg-open "{file_path}"')

    def delete_selected_items(self):
        # Get the currently selected items
        selected_indexes = self.parent().list_view.selectedIndexes()

        if not selected_indexes:
            return

        # Confirm deletion with a QMessageBox
        msg_box = QMessageBox(QMessageBox.Warning, "Confirm Deletion", "Are you sure you want to delete the selected item(s)?", QMessageBox.Yes | QMessageBox.No, self.parent())
        result = msg_box.exec_()

        if result == QMessageBox.Yes:
            for index in selected_indexes:
                file_path = self.parent().model.filePath(index)

                # Use shutil to remove both files and directories
                try:
                    if os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                    else:
                        os.remove(file_path)

                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")

    def create_folder(self):
        # Get the name for the new folder from the user
        folder_name, ok = QInputDialog.getText(self.parent(), "Create Folder", "Enter folder name:")
        

        if ok and folder_name:
            # Create the new folder
            folder_path = os.path.join(os.path.expanduser("~/Desktop"), folder_name)
            try:
                os.makedirs(folder_path)
                QMessageBox.information(self.parent(), "Success", "Folder created successfully!")
            except OSError as e:
                QMessageBox.warning(self.parent(), "Error", f"Failed to create folder: {e}")

    def create_file(self):
        # Get the name for the new file from the user
        file_name, ok = QInputDialog.getText(self.parent(), "Create File", "Enter file name:")

        if ok and file_name:
            # Create the new file
            file_path = os.path.join(os.path.expanduser("~/Desktop"), file_name)
            with open(file_path, "w") as file:
                file.write("")
            QMessageBox.information(self.parent(), "Success", "File created successfully!")
