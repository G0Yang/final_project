# This Python file uses the following encoding: utf-8


import sys, os

sys.path.append(os.path.dirname(__file__))

from couchDBHandler import *

URL = 'localhost'
PORT = 5984
adminID = 'admin'
adminPW = 'admin'

def login(ID = "", PW = ""):
    try:
        if isUserOnline(ID) == True:
            return "이미 온라인임"
        else:
            db = getDatabase(runServer(URL, PORT, adminID, adminPW), "users")
            for item in db.view('view/login'):
                if item['key'] == ID and item['value'] == PW:
                    doc = db.get(item['id'])
                    doc['online'] = "online"
                    doc = db.save(doc)
                    return "로그인 완료"
            
    except Exception as e:
        print(e)
        return False
    return False

def logout(ID = ""):
    try:
        if not isUserOnline(ID) == True:
            return "온라인이 아닙니다."
        db = getDatabase(runServer(URL, PORT, adminID, adminPW), "users")
        for item in db.view('view/userOnline'):
            if item['key'] == ID:
                doc = db.get(item['id'])
                doc['online'] = "offline"
                doc = db.save(doc)
                return True            
            
    except Exception as e:
        print(e)
        return False
    return False

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
                if item['value'] == 'online':
                    return True
    except:
        return "error"
    return False




if __name__ == "__main__":
    #print(getlastBlock("asd00125", "qwe00125"))
    #print(isUserOnline("asd00125"))
    #print(isUserOnline("asd00124"))
    print(getUserChains("id00125"), "\n", type(getUserChains("id00125")))
    #print(checkLastBlock("asd00125", "qwe00125", "F9F3E7874D43EAFB0619618951B0B91C57F4E24E857D528AF6F811BB0897EF93"))
    #print(login("asd00125","asd00125"))
    #print(login("asd00124","asd00124"))


    #print(logout("asd00125"))
    #print(logout("asd00124"))
    
    pass
