#--------
import time


class diaryfile:
    rootpath=''
    name=''
    suffix=''
    txtfile=None
    state=True
    messagememory=[]

    def __init__(self,rootpath,name,suffix):
        self.rootpath=rootpath
        self.name=name
        self.suffix=suffix


    def __del__(self):
        if(self.state==True):
            print('Diary crashed accidentally, path: %s%s'%(self.rootpath,self.name))
        print('Diary is closed, path:  %s%s'%(self.rootpath,self.name))

    def generate_txtdiary(self):
        if self.suffix=='txt':
            self.txtfile= open('%s%s.%s'%(self.rootpath,self.name,self.suffix),'a+',-1)


    def close_diary(self):
        self.state=False
        self.fileobj.close()
        self.__del__()

    def update_txtdiary(self):
        self.generate_txtdiary()
        renewtime=time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        self.txtfile.write(renewtime+'\n')
        self.txtfile.writelines(self.messagememory)
        self.txtfile.close()
        self.messagememory=[]

    def get_message(self,message):
        if isinstance(message,str):
            self.messagememory.append(message+'\n')
            print(self.messagememory)
        elif isinstance(message,dict):
            self.messagememory.append(dir(message)+'\n')
        elif isinstance(message,list):
            try:
                mstr=''
                for estr in message:
                    if isinstance(estr,str):
                        mstr+=estr
                self.messagememory.append(mstr+'\n')
            except:
                print('list message format is invalid, try to convert all the elements into string')
        else:
            print('Unknown type of message')
