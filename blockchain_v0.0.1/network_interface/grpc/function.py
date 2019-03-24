# This Python file uses the following encoding: utf-8

import sys, os, json

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from ledger_interface.transaction import transaction

def maketx(dict):
    print('function maketx')
    print(type(dict))
    print(dict)
    print()
    tx = transaction()
    tx.update(dict)
    print()
    print(type(tx))
    print(tx)
    print()
    print()
    print()
    print()

    return tx.to_dict()

if __name__ == "__main__":
    dict = maketx({'TXID' : "123"})
    print(dict)
    print(type(dict))
