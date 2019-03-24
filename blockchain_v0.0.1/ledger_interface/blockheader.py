# This Python file uses the following encoding: utf-8 

from convert_json import *
from metadata import *

class blockheader(PyJSON):
    def __init__(self, *argv, **kargv):
        self.version = metadata['BaseVersion']
        self.blockNumber = None
        self.timestamp = time.time()
        self.previousBlockHash = ""
        return

if __name__ == '__main__':
    b = blockheader()
    print(b.to_dict())