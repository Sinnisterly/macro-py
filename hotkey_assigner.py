from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt
from pynput import keyboard

class HotkeyAssigner:
    def __init__(self, macro_tool):
        self.macro_tool = macro_tool
        self.db_manager = macro_tool.db_manager
        self.hotkeys = self.db_manager.get_all_hotkeys()
        self.listener = None
        self.create_listener()

    def create_listener(self):
        try:
            hotkey_dict = self.create_hotkey_dict()
            if hotkey_dict:
                self.listener = keyboard.GlobalHotKeys(hotkey_dict)
                self.listener.start()
            else:
                print("No valid hotkeys to listen for.")
        except ValueError as e:
            print(f"Error creating hotkey listener: {e}")
            print("Continuing without global hotkey functionality.")

    def update_listener(self):
        if self.listener:
            self.listener.stop()
        self.create_listener()

    def create_hotkey_dict(self):
        valid_hotkeys = {}
        for hotkey, macro_name in self.hotkeys.items():
            try:
                # Attempt to parse the hotkey
                keyboard.HotKey.parse(hotkey)
                valid_hotkeys[hotkey] = (lambda name=macro_name: lambda: self.macro_tool.play_macro(name))()
            except ValueError:
                print(f"Invalid hotkey '{hotkey}' for macro '{macro_name}'. Skipping.")
        return valid_hotkeys

    def assign_hotkey(self, macro_name):
        dialog = QDialog(self.macro_tool)
        dialog.setWindowTitle("Assign Hotkey")
        dialog.setStyleSheet("""
            QDialog {
                background-color: #36393f;
                color: #dcddde;
                border-radius: 10px;
            }
            QLabel {
                color: #ffffff;
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
        """)
        layout = QVBoxLayout()

        label = QLabel(f"Press a key combination for '{macro_name}':")
        layout.addWidget(label)

        key_label = QLabel("Pressed Keys: ")
        layout.addWidget(key_label)

        button_layout = QHBoxLayout()
        cancel_button = QPushButton("Cancel")
        save_button = QPushButton("Save")
        clear_button = QPushButton("Clear Hotkey")
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)
        button_layout.addWidget(clear_button)
        layout.addLayout(button_layout)

        dialog.setLayout(layout)

        pressed_keys = set()

        def on_press(key):
            try:
                key_char = key.char
            except AttributeError:
                key_char = str(key)
            pressed_keys.add(key_char)
            key_label.setText("Pressed Keys: " + " + ".join(sorted(pressed_keys)))

        def on_release(key):
            pass
            # try:
            #     key_char = key.char
            # except AttributeError:
            #     key_char = str(key)
            # if key_char in pressed_keys:
            #     pressed_keys.remove(key_char)
            # key_label.setText("Pressed Keys: " + " + ".join(sorted(pressed_keys)))

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()

        def save_hotkey():
            hotkey = " + ".join(sorted(pressed_keys))
            if hotkey:
                self.db_manager.save_hotkey(macro_name, hotkey)
                self.hotkeys = self.db_manager.get_all_hotkeys()
                self.update_listener()
                dialog.accept()

        def clear_hotkey():
            self.db_manager.delete_hotkey(macro_name)
            self.hotkeys = self.db_manager.get_all_hotkeys()
            self.update_listener()
            dialog.accept()

        save_button.clicked.connect(save_hotkey)
        cancel_button.clicked.connect(dialog.reject)
        clear_button.clicked.connect(clear_hotkey)

        dialog.exec()
        listener.stop()

    def remove_hotkey(self, macro_name):
        hotkey_to_remove = None
        for hotkey, name in list(self.hotkeys.items()):  # Use list() to avoid runtime error
            if name == macro_name:
                hotkey_to_remove = hotkey
                break
        if hotkey_to_remove:
            del self.hotkeys[hotkey_to_remove]
            self.db_manager.delete_hotkey(macro_name)
        self.update_listener()

    def get_hotkey_for_macro(self, macro_name):
        return self.db_manager.get_hotkey(macro_name)

    def stop_listener(self):
        if self.listener:
            self.listener.stop()