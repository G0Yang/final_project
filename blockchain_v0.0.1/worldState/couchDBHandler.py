# This Python file uses the following encoding: utf-8

import couchdb


def runServer(URL, PORT, ID, PW):
    if "//" in URL:
        URL = URL.split("//")[1]
    if not type(URL) == type(str()) or not type(PORT) == type(str()) or not type(ID) == type(str()) or not type(PW) == type(str()):
        URL = str(URL)
        PORT = str(PORT)
        ID = str(ID)
        PW = str(PW)
    
    couch = couchdb.Server(URL + ":" + PORT)
    couchserver = couchdb.Server("http://%s:%s@"% (ID, PW) + URL + ":" + PORT + "/")
    return couchserver

def getDocumentInDB(server, DBname):
    if not type(DBname) == type(str()):
        return False
    db = server[DBname]
    doc = []
    for j in db:
        att = {}
        for i in db[j]:
            att[i] = db[j][i]
        doc.append(att)
    return doc

def makeDatabase(server, DBname):
    if not type(DBname) == type(str()):
        return False
    if DBname in server:
        db = server[DBname]
        return "exist"
    else:
        db = server.create(DBname)
        return True
    return False

def writinDocument(server, DBname, data):
    if not type(data) == type(dict()):
        return False
    
    db = server[DBname]
    doc_id, doc_rev = db.save(data)
    return doc_id, doc_rev

def blockExist(server, DBname, data):
    if not type(data) == type(dict()):
        return False
    if '_id' not in data:
        return False
    
    db = server[DBname]
    doc = db[data['_id']]
    if doc == data:
        return True
    return False

if __name__ == "__main__":
    URL = "localhost"
    PORT = 5984
    ID = "admin"
    PW = "admin"

    server = runServer(URL, PORT, ID, PW)

    DBname = 'lastblock'

    doc = getDocumentInDB(server, DBname)

    for i in doc:
        print(i)

    data = {'key': 'value'}

    #id, rev = writinDocument(server, DBname, data)


    #print(id, rev)


    doc = getDocumentInDB(server, DBname)

    for i in doc:
        print(i)

    result = blockExist(server, DBname, doc[0])

    print(result)












        



