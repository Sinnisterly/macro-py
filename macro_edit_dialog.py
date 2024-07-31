from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QDoubleSpinBox, QLabel, QMessageBox, QWidget
from PySide6.QtCore import Qt
from styled_widgets import StylizedButton
from title_bar import TitleBar
from key_translator import KeyTranslator

class MacroEditDialog(QDialog):
    def __init__(self, macro, parent=None):
        super().__init__(parent)
        self.macro = macro
        self.initUI()

    def initUI(self):
        print("Setting up MacroEditDialog UI")
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        self.title_bar = TitleBar(self, "Edit Macro")
        main_layout.addWidget(self.title_bar)

        content = QWidget(self)
        content.setObjectName("contentWidget")
        content.setStyleSheet("""
            QWidget#contentWidget {
                background-color: #36393f;
                color: #dcddde;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
            }
            QLabel {
                color: #ffffff;
            }
        """)
        layout = QVBoxLayout(content)

        self.edit_area = QTextEdit(content)
        self.edit_area.setStyleSheet("""
            QTextEdit {
                background-color: #40444b;
                color: #dcddde;
                border: 2px solid #4f545c;
                border-radius: 5px;
            }
        """)
        self.edit_area.setPlainText(self.macro_to_text())
        layout.addWidget(self.edit_area)

        normalize_layout = QHBoxLayout()
        normalize_layout.addWidget(QLabel("Normalize duration:"))
        self.normalize_input = QDoubleSpinBox(content)
        self.normalize_input.setRange(0.01, 1.0)
        self.normalize_input.setValue(0.1)
        self.normalize_input.setSingleStep(0.01)
        self.normalize_input.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #40444b;
                color: #dcddde;
                border: 2px solid #4f545c;
                border-radius: 5px;
            }
        """)
        normalize_layout.addWidget(self.normalize_input)
        self.normalize_button = StylizedButton("Normalize")
        self.normalize_button.clicked.connect(self.normalize_durations)
        normalize_layout.addWidget(self.normalize_button)
        layout.addLayout(normalize_layout)

        button_layout = QHBoxLayout()
        save_button = StylizedButton("Save")
        save_button.clicked.connect(self.save_macro)
        cancel_button = StylizedButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)
        main_layout.addWidget(content)

        self.setFixedSize(500, 400)
        print("MacroEditDialog UI setup complete")

    def macro_to_text(self):
        return self.macro_to_text_from_list(self.macro)

    def macro_to_text_from_list(self, macro):
        return "\n".join([f"{KeyTranslator.vk_to_string(vk)}: {duration:.2f}s {press_time:.2f}s" for vk, press_time, duration in macro])

    def text_to_macro(self):
        lines = self.edit_area.toPlainText().split("\n")
        macro = []
        for line in lines:
            if line.strip():
                parts = line.split(":", 1)  # Split only on the first colon, this does not work, I hate this. Spent more than 2 hours on this.
                if len(parts) != 2:
                    raise ValueError(f"Invalid line format: {line}")
                key_name = parts[0].strip()
                time_parts = parts[1].strip().split()
                if len(time_parts) != 2:
                    raise ValueError(f"Invalid time format in line: {line}")
                try:
                    duration = float(time_parts[0][:-1]) 
                    press_time = float(time_parts[1][:-1]) 
                except ValueError:
                    raise ValueError(f"Invalid time values in line: {line}")
                
                vk = KeyTranslator.string_to_vk(key_name)
                macro.append((vk, press_time, duration))
        return macro

    def normalize_durations(self):
        print("Normalize button clicked")
        target_duration = self.normalize_input.value()
        try:
            macro = self.text_to_macro()
            normalized_macro = [(vk, press_time, target_duration) for vk, press_time, _ in macro]
            self.edit_area.setPlainText(self.macro_to_text_from_list(normalized_macro))
            print(f"Macro normalized with duration: {target_duration}")
        except ValueError as e:
            print(f"Error during normalization: {str(e)}")
            QMessageBox.warning(self, "Normalization Error", str(e))

    def save_macro(self):
        print("Save button clicked in MacroEditDialog")
        try:
            self.macro = self.text_to_macro()
            print(f"Parsed macro: {self.macro}")
            self.accept()
        except ValueError as e:
            print(f"Error parsing macro: {str(e)}")
            QMessageBox.warning(self, "Invalid Input", str(e))

    def showEvent(self, event):
        super().showEvent(event)
        print("MacroEditDialog is being shown")

    def closeEvent(self, event):
        print("MacroEditDialog is being closed")
        super().closeEvent(event)