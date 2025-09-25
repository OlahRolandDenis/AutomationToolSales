import sys
import os

def resource_path(relative_path):
    """Get the absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # We're running in a normal Python environment
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)