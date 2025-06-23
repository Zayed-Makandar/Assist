from pywinauto.application import Application
import pyautogui
import time
import os

def open_app(app_path):
    app = Application().start(app_path)
    return app

def focus_app(window_title):
    app = Application().connect(title_re=window_title)
    app.top_window().set_focus()

def type_in_app(window_title, text):
    app = Application().connect(title_re=".*Notepad.*")
    app.top_window().set_focus()
    time.sleep(0.5)  # Give focus time to settle
    pyautogui.typewrite(text, interval=0.005)  # Much faster typing


def open_app_via_search(app_name):
    pyautogui.hotkey('win')
    time.sleep(0.3)
    pyautogui.typewrite(app_name)
    time.sleep(0.3)
    pyautogui.press('enter')

def close_app(process_name):
    os.system(f'taskkill /im {process_name}.exe /f')