import sys
from PyQt5.QtWidgets import QApplication
from backend import AssistApp

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    try:
        qt_app = QApplication(sys.argv)
        app = AssistApp(qt_app)
        app.run()
    except Exception as e:
        import traceback
        print("Exception occurred:", e)
        traceback.print_exc()
    sys.exit(app.exec_())