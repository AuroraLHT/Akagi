import json
import os
import codecs

absfilep=os.path.dirname(__file__)
'''
{
    "code": [
        "abcdcd",
        "sadfasdfsdaf",
        "asdfasdf"
    ],
    "instruction_mode": 1,
    "modifytime": "",
    "DefaultPath": "C:/Users/macbook/Desktop/",
    "author": "aurora",
    "MacroSavingPath": "C:/Users/macbook/Desktop/研究数据/个股/AutoMacro/",
    "StockSavingpath": "C:/Users/macbook/Desktop/研究数据/股票历史/",
    "DataSavingtype": "excel",
    "Force": 0
}
'''


class configfile(json.JSONEncoder):
    configf=None
    configstr=None
    path=None
    configjson=None

    def __init__(self,filepath):
        if os.path.isfile(filepath):
            self.path=filepath
        elif os.path.isfile(os.path.join(absfilep,filepath)):
            self.path=os.path.join(absfilep,filepath)
        else:
            raise Exception( 'the format of filepath is not correct or the file in:%s, %s, %s is not existed'%(filepath,os.path.join(os.getcwd(),filepath),os.path.join(absfilep,filepath)  ) )

    def _open(self):
        enc='utf-8'
        self.configf=codecs.open(self.path,encoding=enc,mode='r+')
        self.configstr=self.configf.read()
        self.configjson=json.loads(self.configstr)
        #print(self.configjson)


    def KW_modify(self,**arg):
        #或用迭代器arg.iteritems(), 迭代字典
        self._open()
        for Na, Va in arg.items():
            if  'code DataSavingtype instruction_mode Force StockSavingpath MacroSavingPath DefaultPath DataSavingtype'.find(Na) != -1 and Na!=' ':
                self.configjson[Na]=Va

    def KW_save_config(self):
        # use with self.configf as f:
        if not self.configf.closed:
            self.configstr=json.dumps(self.configjson,ensure_ascii=False,indent=4,sort_keys=True)
            self.configf=deleteContent(self.configf)
            self.configf.write(self.configstr)
            self.configf.close()

        else:
            raise Exception('Make sure we iniial the file')

    def Set_Stock_Download(self):
        self._open()
        RE=[]
        Keysets='code DataSavingtype instruction_mode Force StockSavingpath MacroSavingPath DefaultPath'
        for key in Keysets.split(' '):
            RE.append(self.configjson[key])

        self.configf.close()
        return RE

def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()
    return pfile



def test():
    path='C:/Users/macbook/Anaconda3/MyCode/StockP_config.json'
    path1='StockP_config.json'
    a=configfile(path)
    b=configfile(path1)

    a.KW_modify(code=['abcdcd','sadfasdfsdaf','asdfasdf'])
    a.KW_save_config()

    [code,DataSavingtype,I_Mode,Force,StockSavingpath,MacroSavingPath,DefaultPath]=a.Set_Stock_Download()
    print(code)
    print(DataSavingtype)
    print(DefaultPath)
    print(I_Mode)
    print(Force)
    print(StockSavingpath)
    print(MacroSavingPath)


if __name__ =='__main__':
    test()
    print("----------------------Clear----------------------")
