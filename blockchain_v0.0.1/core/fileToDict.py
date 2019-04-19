# This Python file uses the following encoding: utf-8
import os

class fileToDict:
    def __init__(self):
        self.path = os.path.dirname(__file__)
        return

    def fileread(self, filename):
        try:
            with open(filename, "rb") as f:
                data = f.read()
                size = len(data)
                f.close()
                return {
                    "filename" : filename.split("\\")[len(filename.split("\\"))-1],
                    "data" : data,
                    "size" : size
                    }
        except Exception as e:
            print("class fileToDict def fileread Exception")
            print(e)
        return False

    def filesave(self, dic):
        try:
            if (not "data" in dic) and (not "filename" in dic):
                return False
            if "\\" in dic["filename"]:
                with open(dic["filename"], "wb") as f:
                    f.write(dic["data"])
                    f.close()
                    return dic["filename"]
            else:
                path = os.path.join(self.path, dic["filename"])
                with open(path, "wb") as f:
                    f.write(dic["data"])
                    f.close()
                    return path
        except Exception as e:
            print("class fileToDict def filesave Exception")
            print(e)
        return False

    def setFolder(self, path):
        if not type(path) is type(str()):
            return False
        self.path = path
        return self.path

if __name__ == "__main__":
    f = fileToDict()
    dic = f.fileread("C:\\Users\\milk1\\Downloads\\이력서_20190417.pdf")
    print(dic)

    path = f.setFolder("C:\\Users\\milk1\\Desktop\\170305_hwpconverter")
    print(path)

    savepath = f.filesave(dic)
    print(savepath)