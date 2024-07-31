from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QPoint

class TitleBar(QWidget):
    def __init__(self, parent, title):
        super().__init__(parent)
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.title = QLabel(title)

        btn_size = 35

        self.btn_close = QPushButton("×")
        self.btn_close.clicked.connect(self.parent.close)
        self.btn_close.setFixedSize(btn_size,btn_size)
        self.btn_close.setStyleSheet("""
            QPushButton {
                background-color: #202225;
                color: #dcddde;
                border: none;
                font-size: 16px;
                border-top-right-radius: 10px;
            }
            QPushButton:hover {
                background-color: #f04747;
            }
        """)

        self.title.setFixedHeight(35)
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_close)

        self.setStyleSheet("""
            background-color: #202225;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)
        self.title.setStyleSheet("""
            color: #dcddde;
            font-weight: bold;
            padding-left: 10px;
        """)

        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(TitleBar, self).resizeEvent(QResizeEvent)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                    self.mapToGlobal(self.movement).y(),
                                    self.parent.width(),
                                    self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False