import time
import sys
import os

def getCurrentTime():
    t = time.time()
    return int(t * 1000)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)