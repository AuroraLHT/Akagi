# news key word catch
import os
import random
import time
import tushare as ts
import math
import pandas
import threading
from MYSORT import *
from programdiary import *
import Stock_config_kit as Skit
import ForgeModel

COLLECTORSHOWNUM=5
fgt={'a':0.01,'a_2':0.01,'lam':0.01}
DIARYNAME='DIARY_Ver.0.1_ty2_0.01_0.01'

def readsinatime(timestr):
    if timestr:
        try:
            Year=int(time.strftime('%Y',time.gmtime()) )
            [F,L]=timestr.split(' ')
            [mon,day]=F.split('-')
            [hour,minus]=L.split(':')
            mon=int(mon)
            day=int(day)
            hour=int(hour)
            minus=int(minus)
            # in time.mktime the #6, #7's value do not matter (#0--#8)
        except:
            print('the timestr is not enough for unpacking process :%s'%timestr)
            [Year,mon,day,hour,minus]=[2016,0,0,0,0]
    else:
        [Year,mon,day,hour,minus]=[2016,0,0,0,0]
    return time.mktime( (Year,mon,day,hour,minus,0,0,0,0) )

class loopobj(threading.Thread):
    loopflag=0 #1 means stop
    def __init__(self):
        threading.Thread.__init__(self)

    def setlooppara(self,span,funchandle,*funcpara):
        self.span=span
        self.funch=funchandle
        self.funcpara=funcpara

    def stoploop(self):
        self.loopflag=1

    def timeloop(self):
        print(self.name+ ': loop start')
        while self.loopflag==0:
            time.sleep(self.span)
            if self.funcpara[0]==None:
                self.funch()
            else:
                #self.funch(self.funcpara)
                #print('stock')
                parastr=''
                for i in range(len( self.funcpara)):
                    parastr+='self.funcpara[%d]'% (i)
                eval('self.funch(%s)'%parastr)


        print(self.name+ '  timeloop end')

    def run(self):
        self.timeloop()

class Keyword:

    wordset=None
    Counter=0
    distribution=None
    weight=None
    show_dis_flag=False

    def __init__(self,wordset,weight):
        if(isinstance(wordset,list)):
            self.wordset=wordset
            self.distribution=[0 for n in range(len( wordset) )]   ######################## good!
            self.weight=weight
            self._sortkeyword()

    def modify_keyword(self,mode,M_KW):
        if not isinstance(mode,1):

            if(mode==1):
                # delte keyword from KW
                # delte the relavant distri from KW
                for KW in M_KW:
                    I=self.index(KW)
                    self.wordset.remove(KW)
                    self.distribution.remove(self.distribution[I])
                    self.weight.remove(self.weight[I])
                    # or del self.distribution[I]

            elif(mode==2):
                for KW in M_KW:
                    self.wordset.append(KW)
                    self.distribution.append(0)
                    self.weight.append(1)

                self._sortkeyword(self)
                # creat%
                # creat$
            else:
                print('Unknown Mode Number. mode=1 for subtracting keywords,mode=2 for adding keywords')

    def modify_distri(self,prey):
        ind=0
        for ele in prey:
            self.distribution[ind]+=ele
            ind+=1

    def show_distri(self):
        # print like 'word': times 'word2': times
        i=0
        output=''
        while i<len(self.distribution):
            output+='%s: %s  '%(self.wordset[i],self.distribution[i])
            i+=1
        print(output)

    def hunt(self,preystr):
        i=0
        dis=[0 for n in range(len( self.wordset))]
        c_flag=False
        for key in self.wordset:
            findcounter=False
            findhead=-1
            for j in range(len(self.wordset)):
                findhead=preystr.find( key , findhead+1 )
                if findhead == -1:
                    break
                findcounter+=int(bool(1+findhead))
                c_flag=True
            dis[i]+=findcounter
            #self.distribution[i]+=findcounter
            i+=1

        self.modify_distri(dis)
        if c_flag==True and self.show_dis_flag==True:
            self.show_distri()

    def _sortkeyword(self):
        try:
            List_one=self.wordset
            Capital_L_one=[]
            for element in List_one:
                try:
                    Capital_L_one.append( ord( element[0] ) )
                except:
                    print(self.name,'   :',element )
            [self.wordset,self.distribution,self.weight]=mysort(Capital_L_one,self.wordset,self.distribution,self.weight)
        except:
            print(self.name,'  ',self.wordset)

class stock_info(Keyword,loopobj,ForgeModel.Forge):
    name=''
    code=''
    browsetime=''
    Name_W=1
    Code_W=1
    Area_W=1
    Ind_W=2
    Con_W=2

    def __init__(self,name='',code='',area=[],industry=[],concept=[],a=fgt['a'],a_2=fgt['a_2'],lam=fgt['lam']):
        #some time later would add a return to creat more cal
        self.name=name
        self.code=code
        self.area=area
        self.industry=industry
        self.concept=concept
        #self.business=business
        ForgeModel.Forge.__init__(self,a,a_2,lam)

        Keyword.__init__(self,[code]+[name]+area+industry+concept,self.ini_weight() )
        loopobj.__init__(self)

    def ini_weight(self):
        W=[self.Code_W,self.Name_W]

        if self.area:
            W.append(self.Area_W)

        if isinstance( self.industry,list) and self.industry!=[]:
            for i in self.industry:
                W.append(self.Ind_W)


        if isinstance( self.concept,list) and self.concept!=[]:
            for i in self.concept:
                W.append(self.Con_W)
        return W

    def Trum(self,Newsobj):
        if Newsobj.latesttime!=self.browsetime:
            brt=readsinatime(self.browsetime)
            newst=readsinatime(Newsobj.latesttime)
            if brt==(0,0,0,0,0,0,0,0,0):
                deltat=0
            elif newst==(0,0,0,0,0,0,0,0,0):
                deltat=0
            else:
                deltat=newst-brt

            self.stimulate_forge_type2(self.distribution,deltat)
            self.browsetime=Newsobj.latesttime
            self.hunt(Newsobj.latestnew)
        else:
            pass

class News(loopobj):
    name=None
    newslength=1
    show_c=True
    Newsmemory= pandas.DataFrame()
    latesttime=''
    latestnew=''

    def __init__(self,name):
        self.name=name
        loopobj.__init__(self)

    def modify_newspara(self,nl,show_c):
        self.newslength=nl
        self.show_c=show_c

    def Newsget(self):
        #PDnews=ts.get_latest_news(top=self.newslength,show_content=self.show_c)
        PDnews=ts.get_latest_news(top=self.newslength,show_content=False)

        try:
            if PDnews.ix[0,'time']!=self.latesttime:
                Newsmemory=pandas.concat([self.Newsmemory,PDnews],axis=0) #按行合并
                #self.latesttime=PDnews.ix[0,'time']
                if self.show_c:
                    try:
                        Content=None
                        C_C=0
                        while not Content and C_C<5:
                            Content=ts.latest_content(PDnews.ix[0,'url'])
                            C_C+=1
                    except:
                        print('latest_content api fail to load url:%s'%PDnews.ix[0,'url'])
                        Content=''

                    #self.latestnew=PDnews.ix[0,'classify']+PDnews.ix[0,'title']+Content
                    self.latestnew=PDnews.ix[0,'title']+Content
                else:
                    #self.latestnew=PDnews.ix[0,'classify']+PDnews.ix[0,'title']  #maybe content later
                    self.latestnew=PDnews.ix[0,'title']
                print(PDnews[['classify','title','time']])

                if PDnews.ix[0,'time']:
                    print('old latesttime %s'%self.latesttime)
                    self.latesttime=PDnews.ix[0,'time']
                    print('new latesttime %s'%self.latesttime)


        except:
            print('Get Latest News Error')


class Collector(loopobj):
    name=None
    dissum=None
    showNum=COLLECTORSHOWNUM

    def __init__(self,name,diary,configfile):
        self.name=name
        self.diaryfile=diary
        self.configfile=configfile
        loopobj.__init__(self)

    def info_collect(self,stocklist):
        self.dissum=[0 for i in range(len(stocklist))]
        #try:
        i=0
        for i, stock in enumerate( stocklist):
            _dissum=0
            for j,ele_dis in enumerate( stock.distribution):
                _dissum+=ele_dis*stock.weight[j]
            self.dissum[i]=_dissum
        #except:
        #    print('Collector Error')

    def info_process(self,stocklist):
        self._indexlist=[]
        self.counterlist=[]
        self.orderlist=[]
        Ind=0
        OldInd=None
        indexlist=[n for n in range(len(stocklist)) ]

        [indexlist]=mysort(self.dissum,indexlist)
        self.dissum.reverse()
        indexlist.reverse()

        for i in range(self.showNum):
            temp=self.dissum[Ind]
            self.orderlist.append(temp)
            counter=1
            if Ind+1<len(self.dissum):
                for j in range(Ind+1,len(self.dissum)):
                    if self.dissum[j]==temp:
                         counter+=1
                    else:
                        OldInd=Ind
                        Ind=Ind+counter
                        break
            if OldInd!=None :
                self.counterlist.append(counter)
                self._indexlist.append(indexlist[OldInd:OldInd+counter])

    def report(self,stocklist):
        reportlist=[]

        for i in range( len(self.counterlist) ):

            freq=self.counterlist[i]
            order=self.orderlist[i]
            if order!=0 and freq != len(stocklist):
                SNameList=[]
                for j in range( len( self._indexlist[i] )):
                    ind=self._indexlist[i][j]
                    SNameList.append(stocklist[ind].name)

                restr='Order: %.5f , Freq: %d, Stock: %s'%(order,freq,','.join(SNameList))
                reportlist.append(restr)

            else:
                reportlist.append('Order is Zero or Frequency is the lenth of stocklist')

        self.diaryfile.get_message(reportlist)
        self.diaryfile.update_txtdiary()

    def change_conf(self,stocklist):
        SNameList=[]
        for i in range( len(self.counterlist) ):
            if self.orderlist[i]!=0 and self.counterlist[i] != len(stocklist):
                for j in range( len( self._indexlist[i] )):
                    ind=self._indexlist[i][j]
                    SNameList.append(stocklist[ind].code)
        self.configfile.KW_modify(code=SNameList)
        self.configfile.KW_save_config()

    def collector(self,stocklist):
        print('##############Inking the diary#############')
        self.info_collect(stocklist)
        self.info_process(stocklist)
        self.report(stocklist)
        self.change_conf(stocklist)
        print('#############Report Finish#############')

def ini_classfication():
    Industry=ts.get_industry_classified()
    Concept=ts.get_concept_classified()
    Area=ts.get_area_classified()
    _Codelist=Area[['code']]
    Codelist=[]
    for i in range(len(_Codelist) ):
        Codelist.append(_Codelist.ix[i,0])
    return [Codelist,Area,Concept,Industry]

def stock_classfication(code,Area,Concept,Industry):
    area=Area.query('code=='+"'"+code+"'")
    _area=area[['area']]
    _name=area[['name']]

    try:
        _name=str(_name.iloc[0,0])
    except:
        _name='未知'

    #   area=area.get_value(0,0)
    try:
        _area=[_area.iloc[0,0]]
    except:
        _area=[]
    #or Area[Area.code.isin([code])]
    concept=Concept.query('code=='+"'"+code+"'")
    _concept=concept[['c_name']]

    try:
        __concept=[]
        for i in range( len(_concept) ):
            __concept.append( _concept.iloc[i,0] )
    except:
        __concept=[]

    industry=Industry.query('code=='+"'"+code+"'")
    try:
        _industry=industry[['c_name']]
        _industry=_industry.iloc[0,0]
        _industry=_industry.replace('行业','')
        if len(_industry)==4:
            _industry=[_industry[0:2],_industry[2:4]]
        else:
            _industry=[_industry]

    except:
        _industry=[]

    return [_name,_area,__concept,_industry]

def prelearn_weight_s(stockobj,STR):
    stockobj.hunt(STR)

def prelearn_weight(stockobjlist,strlist):
    for STR in strlist:
        for stock in stockobjlist:
            try:
                prelearn_weight_s(stock,STR)
            except:
                print("Stock %s prelearn failed"%stock.name)
#12 min to download 1000 news with content.
def SINA_prelearn(stockobjlist,newslength,with_c=False):
    download_flag=False
    while not download_flag:
        PDnews=ts.get_latest_news(top=newslength,show_content=with_c)

        try:
            len(PDnews)
            download_flag=True
            print("prelearn news download finished.")
        except:
            print("the newslength %d didn't work. We minus it with 100 and try again."%newslength)
            newslength=newslength-100

    Newsstr=[]
    if(with_c):
        for i in range( len( PDnews) ):     #len(PDnews.index)
            Newsstr.append(PDnews.ix[i,'classify']+PDnews.ix[i,'title']+PDnews.ix[i,'content'])
    else:
        for i in range(len( PDnews)):
            Newsstr.append(PDnews.ix[i,'classify']+PDnews.ix[i,'title'])
    prelearn_weight(stockobjlist,Newsstr)

def test():

#    a=stock_info(name='a',code='000000',area=['概率'],industry=['方法','还好'],concept=['沪江','了就'])
#    a.distribution=[0,0,0,0,0,0,0]
#    b=stock_info(name='b',code='000000',area=[],industry=['方法','还好'],concept=['沪江','了就'])
#    b.distribution=[0,0,0,0,0,2]
#    c=stock_info(name='c',code='000000',area=['概率'],industry=[],concept=['沪江','了就'])
#    c.distribution=[0,0,0,0,1]
#    d=stock_info(name='d',code='000000',area=['概率'],industry=['方法','还好'],concept=[])
#    d.distribution=[0,0,0,0,0]
#    e=stock_info(name='e',code='000000',area=['概率'],industry=['方法'],concept=['沪江','了就'])
#    e.distribution=[0,0,0,0,0,1]
#    f=stock_info(name='f',code='000000',area=['概率'],industry=['方法'],concept=['沪江','了就'])
#    f.distribution=[0,0,0,0,0,2]

    path='%s%s'%(os.path.dirname(__file__),'/diary/')
    #path='%s%s'%(os.path.dirname(os.path.abspath('__file__')),'/diary/')
    #path='%s%s'%(os.getcwd(),'/diary/')
    diary=diaryfile(rootpath=path,name=DIARYNAME,suffix='txt')

#    testColl=Collector('SINA_COLLECTOR',diary)
#    testColl.collector([a,b,c,d,e,f])

#    diary.get_message('test')
#    diary.update_txtdiary()
#    diary.txtfile.close()

    Conf=Skit.configfile('StockP_config.json')

#    Testobj=stock_info(name='首钢',code='000959',industry=['普钢'])
#    Testobj.setlooppara(5,Testobj.News)
#    Testobj.start()

#--------------------News test-----------------------------
    Newsobj=News('SINA_FORCAST_NEWS')
    Newsobj.setlooppara(1,Newsobj.Newsget,None)
    Newsobj.start()

#    a=0
#    while not a:
#        a=bool(input())
#        if a==1 or a==' ':
#            Testobj.stoploop()
#            print('stop loop  The world!!!!!')

#----------------------Sort test-------------------------#
#    Testobj=stock_info(name='首钢',code='000959',industry=['普钢','美少女','名给','哲学'])
#    Testobj.show_distri()
#    Testobj.hunt('普钢里面有美少女不过也有个明给')
#    Testobj.show_distri()
#----------------------Initial test--------------#
#    [Codelist,Area,Concept,Industry]=ini_classfication()
#    [name,ar,co,ind]=stock_classfication('000959',Area,Concept,Industry)
#    Stockobj=stock_info(name=name,code='000959',area=[ar],industry=[ind],concept=[co])
#    Stockobj.show_distri()
#---------------------hunt test----------------------#
    Stockobj_chain=[]
    ini_class_flag = True
    while ini_class_flag:
        try:
            [Codelist,Area,Concept,Industry]=ini_classfication()
            ini_class_flag=False
        except:
            print("Fail to download the stock classification data, We try it again...")
            ini_class_flag = True

    testcoun=0
    #print(Codelist)
    for code in Codelist:

        [name,ar,co,ind]=stock_classfication(code,Area,Concept,Industry)
        Stockobj=stock_info(name=name,code=code,area=ar,industry=ind,concept=co)
        if Stockobj.name!='未知':
            Stockobj.setlooppara(1,Stockobj.Trum,Newsobj)
            Stockobj.start()
    #    Stockobj.show_distri()

        Stockobj_chain.append(Stockobj)

    SINA_prelearn(Stockobj_chain,2000,0)

    #    except:
    #        print('stock initial error')

#    for stock in Stockobj_chain:

    Coll=Collector('SINA_COLLECTOR',diary,Conf)
    Coll.setlooppara(60*10,Coll.collector,Stockobj_chain)
    Coll.start()

if __name__ == '__main__': test()
