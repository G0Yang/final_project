# This Python file uses the following encoding: utf-8

from couchDBHandler import *

URL = 'localhost'
PORT = 5984
adminID = 'admin'
adminPW = 'admin'

def checkLastBlock(ID = '', CHID = '', blockHash = ''):
    try:
        if isUserOnline(ID) == "offline":
            return "not online"
        if not CHID in getUserChains(ID):
            return "CHID not found"

        block = getlastBlock(ID, CHID)
        if 'B_Hash' in block:
            if block['B_Hash']== blockHash:
                return True
    except:
        return False
    return False

def getlastBlock(ID = '', CHID = ''):
    try:
        db = getDatabase(runServer(URL, PORT, adminID, adminPW), "lastblock")
        for item in db.view('view/lastBlock'):
            if item['key'] == ID and item['value'][0] == CHID:
                return item['value'][1]
    except:
        return False
    else:
        return "not found"
    return False


def getUserChains(ID = ''):
    try:
        db = getDatabase(runServer(URL, PORT, adminID, adminPW), "users")
        for item in db.view('view/userChains'):
            if item['key'] == ID:
                return item['value']
    except:
        return False
    else:
        return "not found"
    return False

def isUserOnline(ID = ''):
    try:
        db = getDatabase(runServer(URL, PORT, adminID, adminPW), "users")
        for item in db.view('view/userOnline'):
            if item['key'] == ID:
                return item['value']
    except:
        return "error"
    else:
        return "not found"
    return False




if __name__ == "__main__":
    print(getlastBlock("asd00125", "qwe00125"))
    print(isUserOnline("asd00125"))
    print(getUserChains("asd00125"))
    print(checkLastBlock("asd00125", "qwe00125", "F9F3E7874D43EAFB0619618951B0B91C57F4E24E857D528AF6F811BB0897EF93"))
    
    pass
