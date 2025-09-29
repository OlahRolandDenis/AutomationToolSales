import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    full_path = os.path.join(base_path, relative_path)
    full_path = os.path.normpath(full_path)
    exists = os.path.exists(full_path)

    if not exists and hasattr(sys, '_MEIPASS'):
        alt_path = os.path.join(base_path, os.path.basename(relative_path))
        alt_path = os.path.normpath(alt_path)
        if os.path.exists(alt_path):
            return alt_path


    return full_path