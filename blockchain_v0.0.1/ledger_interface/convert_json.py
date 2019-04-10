# This Python file uses the following encoding: utf-8

# https://stackoverflow.com/questions/49084842/creating-a-python-object-from-a-json-string/49085020#49085020

import json, time

class PyJSON(object):
    def __init__(self, d):
        if type(d) is str:
            d = json.loads(d)

        self.from_dict(d)

    def from_dict(self, d):
        self.__dict__ = {}
        for key, value in d.items():
            if type(value) is dict:
                value = PyJSON(value)
            self.__dict__[key] = value

    def to_dict(self):
        d = {}
        for key, value in self.__dict__.items():
            if type(value) is PyJSON:
                value = value.to_dict()
            d[key] = value
        return d

    def __repr__(self):
        return str(self.to_dict())

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]
    

    def to_json(self, path = '', filename = '', data = {}):
        print(path)
        print(filename)
        try:
            if 'filedata' in data and 'filename' in data:
                print("파일 별도 저장 실행")
                with open(path + data['filename'], 'wb') as f:
                    f.write(data['filedata'])
        except:
            print("저장 실패")
            data['filedata'] = False
        else:
            print("저장 성공")
            data['filedata'] = True

        try:
            with open(path + filename, 'w', encoding="utf-8") as make_file:
                print("파일을 제외한 데이터 json으로 저장")
                json.dump(data, make_file, ensure_ascii=False, indent="\t")
        except:
            print("저장 실패")
        else:
            print("저장 성공")
        return 

    def from_json(self, path = '', filename = ''):
        data=open(path + filename).read()
        data = json.loads(data)
        self.from_dict(data)
        return
