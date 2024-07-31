from PySide6.QtWidgets import QLineEdit, QPushButton, QComboBox

class StylizedLineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4f545c;
                border-radius: 5px;
                padding: 5px;
                background-color: #40444b;
                color: #dcddde;
            }
            QLineEdit:focus {
                border-color: #7289da;
            }
        """)

class StylizedButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #7289da;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #677bc4;
            }
            QPushButton:pressed {
                background-color: #5b6eae;
            }
        """)

class StylizedComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QComboBox {
                border: 2px solid #4f545c;
                border-radius: 5px;
                padding: 5px;
                background-color: #40444b;
                color: #dcddde;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 25px;
                border-left-width: 1px;
                border-left-color: #4f545c;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow.png);
            }
            QComboBox QAbstractItemView {
                border: 2px solid #4f545c;
                selection-background-color: #7289da;
            }
        """)