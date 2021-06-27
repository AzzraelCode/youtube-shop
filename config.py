import os

root_path = os.path.dirname(__file__)

def get_path(path='bin', sep=os.sep):
    return root_path + sep + path