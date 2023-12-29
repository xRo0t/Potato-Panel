from PyQt5.QtWidgets import QListView, QStyledItemDelegate
from PyQt5.QtCore import Qt, QSize

class DesktopListView(QListView):
    def __init__(self, context_menu, desktop, parent=None):
        super().__init__(parent)
        self.context_menu = context_menu
        self.desktop = desktop

    def mousePressEvent(self, event):
        index = self.indexAt(event.pos())
        if event.button() == Qt.RightButton:
            if not index.isValid():
                self.clearSelection()
                self.context_menu.hide()
                self.desktop.desktop_menu.exec_(self.mapToGlobal(event.pos()))
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
