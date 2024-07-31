from PySide6.QtCore import QThread, Signal  # Change pyqtSignal to Signal
import win32api
import time
from key_translator import KeyTranslator

class MacroRecorder(QThread):
    finished = Signal(list)  # Change pyqtSignal to Signal because pyqt only got me 85% of the way there

    def __init__(self):
        super().__init__()
        self.recording = False
        self.macro = []
        self.pressed_keys = {}

    def run(self):
        self.recording = True
        start_time = time.time()
        while self.recording:
            for i in range(1, 256):
                state = win32api.GetAsyncKeyState(i)
                if state & 0x8000:  # Key is pressed
                    if i not in self.pressed_keys:
                        self.pressed_keys[i] = time.time() - start_time
                elif i in self.pressed_keys:  # Key was released
                    press_time = self.pressed_keys[i]
                    release_time = time.time() - start_time
                    duration = release_time - press_time
                    key_name = KeyTranslator.vk_to_string(i)
                    self.macro.append((key_name, press_time, duration))
                    del self.pressed_keys[i]
            time.sleep(0.001)
        self.finished.emit(self.macro)

    def stop(self):
        self.recording = False