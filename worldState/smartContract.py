# This Python file uses the following encoding: utf-8

import os, json

contractPATH = os.path.dirname(os.path.realpath(__file__))

# 스마트 컨트랙트 파일 리스트 불러오기
def listup(dir = contractPATH):
    contractList = []
    dirlist = os.listdir(dir)
    for i in dirlist:
        if ".json" in i:
            contractList.append(i)
    return contractList

# 계약 파일 중 파일이름에 맞는 계약 데이터를 반환
def findContract(contractID):
    if contractID not in listup():
        return False

    print(os.path.join(contractPATH, contractID))

    try:
        data = open(os.path.join(contractPATH, contractID)).read()
        contract = json.loads(data)
        if "type" in contract:
            if contract['type'] != "contract":
                return False
    except Exception as e:
        print(e)
    else:
        return contract
    
    return False

# 다른 노드와 같은 계약인지 확인해주는 함수
def matchContract(contract = {}, filename = ''):
    if type(contract) is not type(dict()):
        return False
    if len(contract) == 0:
        return False

    data=open(os.path.join(contractPATH, filename)).read()
    fileContract = json.loads(data)

    if fileContract == contract:
        return True

    return False

# 데이터가 계약에 맞게 작성되었는지 확인하는 함수
def checkContract(data = {}, contract = {}, myProfile = {}):
    try:
        if len(data) == 0 or len(contract) == 0 or len(myProfile) == 0:
            return False

        if not contract['owner'] == myProfile:
            return False

        if not contract['product'].keys() == data.keys():
            return False

        if not data['eventType'] in contract['event']:
            return False

    except Exception as e:
        print(e)
    else:
        return True

    return False

# world state와 마지막 블록이 일치하는지 확인하는 함수
def checkLastBlockInWorld(chainList):
    if not type(chainList) == type(list()):
        return False
    try:
        for i in chainList:
            with open(i).read() as chain:
                pass
    except:
        return False
    else:
        return True
    return False

if __name__ == '__main__':

    filename = 'jn4583nh226632.json'
    c = findContract(filename)
    print(c)

    print(type(c))


    print(matchContract(contract = c, filename = 'jn4583nh226632.json'))


    tx = {
        'name' : "asd",
        'price' : 10000,
        'eventType' : 'production'
        }

    my = {
        "ID": "creatorID1",
        "name": "creatorName1",
        "key": "prikey1",
        "priHash": "proHash1"
        }

    print(checkContract(data = tx, contract = c, myProfile = my))