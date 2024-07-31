from PySide6.QtCore import QThread
import time
import pygetwindow as gw
import win32api
import win32con
from key_translator import KeyTranslator

class MacroPlayer(QThread):
    def __init__(self, macro, app_name=None, loop=False):
        super().__init__()
        self.macro = macro
        self.app_name = app_name
        self.loop = loop

    def run(self):
        while True:
            # Activate the target application
            if self.app_name and self.app_name != "Select an app (optional)":
                windows = gw.getWindowsWithTitle(self.app_name)
                if windows:
                    window = windows[0]
                    window.activate()
                    time.sleep(0.5)

            start_time = time.time()
            shift_pressed = False
            for action in self.macro:
                key_name, press_time, duration = action
                current_time = time.time() - start_time
                if current_time < press_time:
                    time.sleep(press_time - current_time)

                vk_code = KeyTranslator.string_to_vk(key_name) if isinstance(key_name, str) else key_name

                if vk_code is not None:
                    try:
                        if isinstance(vk_code, int):
                            if KeyTranslator.is_shift_key(vk_code):
                                if not shift_pressed:
                                    win32api.keybd_event(0x10, 0, 0, 0)  
                                    shift_pressed = True
                            else:
                                win32api.keybd_event(vk_code, 0, 0, 0)
                                time.sleep(duration)
                                win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)
                                if shift_pressed:
                                    win32api.keybd_event(0x10, 0, win32con.KEYEVENTF_KEYUP, 0)  
                                    shift_pressed = False
                        else:
                            print(f"Simulating key: {key_name}")
                    except Exception as e:
                        print(f"Error playing key {key_name}: {str(e)}")
                else:
                    print(f"Skipping unsupported key: {key_name}")

            if shift_pressed:
                win32api.keybd_event(0x10, 0, win32con.KEYEVENTF_KEYUP, 0)  # Ensure Shift is released at the end for the love...

            if not self.loop:
                break
        print("Macro playback completed")