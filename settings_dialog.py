# settings_dialog.py

import psutil
import pygetwindow as gw
from PySide6.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLabel, QCheckBox, QPushButton, QHBoxLayout, QWidget
from PySide6.QtCore import Qt
from title_bar import TitleBar

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Window)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(300, 200)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Custom title bar
        self.title_bar = TitleBar(self, "Settings")
        main_layout.addWidget(self.title_bar)

        # Content widget with the rest of the settings UI
        content = QWidget()
        content.setObjectName("contentWidget")
        content.setStyleSheet("""
            QWidget#contentWidget {
                background-color: #36393f;
                color: #dcddde;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }
            QLabel, QCheckBox, QComboBox {
                color: #dcddde;
            }
            QComboBox {
                border: 2px solid #4f545c;
                border-radius: 5px;
                padding: 5px;
                background-color: #40444b;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #4f545c;
                selection-background-color: #7289da;
            }
            QPushButton {
                background-color: #7289da;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #677bc4;
            }
            QPushButton:pressed {
                background-color: #5b6eae;
            }
        """)
        layout = QVBoxLayout(content)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)  # Set spacing between main elements

        # Target Application selection
        target_app_layout = QVBoxLayout()
        target_app_layout.setSpacing(5)  # this is internal elements you dummy.
        target_app_layout.addWidget(QLabel("Select Target Application:"))
        self.app_selector = QComboBox()
        self.populate_running_apps()
        target_app_layout.addWidget(self.app_selector)
        layout.addLayout(target_app_layout)

        # Loop Playback checkbox
        loop_checkbox_layout = QHBoxLayout()
        self.loop_checkbox = QCheckBox("Enable Loop Playback")
        loop_checkbox_layout.addWidget(self.loop_checkbox)
        layout.addLayout(loop_checkbox_layout)

        # Save and Cancel buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)
        button_layout.setSpacing(10)  # Spacing between buttons
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        main_layout.addWidget(content)

        # Connections
        save_button.clicked.connect(self.save_settings)
        cancel_button.clicked.connect(self.reject)

    def populate_running_apps(self):
        """Populate the QComboBox with the names of running applications with visible windows."""
        self.app_selector.addItem("Select an app (optional)")
        visible_windows = gw.getAllTitles()
        visible_windows = [title for title in visible_windows if title]  # Filter out empty titles
        for title in visible_windows:
            if title not in self.app_selector.currentText():
                self.app_selector.addItem(title)

    def save_settings(self):
        selected_app = self.app_selector.currentText()
        loop_playback = self.loop_checkbox.isChecked()
        # Save these settings in db.
        self.accept()
