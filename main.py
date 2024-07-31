import sys
from PySide6.QtWidgets import QApplication
from macro_tool import MacroTool

def exception_hook(exctype, value, traceback):
    print(f"An uncaught exception occurred: {exctype.__name__}: {value}")
    sys.__excepthook__(exctype, value, traceback)

if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    ex = MacroTool()
    ex.show()
    sys.exit(app.exec())