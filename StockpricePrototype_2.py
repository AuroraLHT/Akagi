import sys
import tushare as ts
import time
import pandas
import math
from datetime import date


RDate=time.strftime("%Y-%m-%d",time.gmtime())
RYear=time.strftime("%Y",time.gmtime())
RMonth=time.strftime("%m",time.gmtime())
RQuarter=str(math.ceil( int(RMonth)/4 ) +1)

class HDR:
    'to creat a class hold basic infomation for the handler'
    Hancount=0
    def __init__(self,name,display,defaultPara=''):
        self.name=name
        self.defaultPara=defaultPara
        self.Hancount+=1
        self.display=display
    def __del__(self):
        print('delete '+self.__class__.__name__)

    def _Modifydpara(self,para):
        self.defaultPara=para

    def _display(self):
        return self.display

    def _Han(self,RecentPara=''):
        if RecentPara:
            return self.name+'('+RecentPara+')'
        elif not self.defaultPara:
            return self.name+'()'
        else:
            return self.name+'('+self.defaultPara+')'

class PST:
    def __init__(self,hanset,itera,para,display):
            self.hanset=hanset
            self.iter=itera
            self.para=para
            self.display=display
    def __del__(self):
        print("del "+self.__class__.__name__)
    def _display(self):
        return (self.display)



    def Pind(self,Para):
        if not Para:
            return
        ParaArr=Para.split('|')
        PArr2=[];
        con=0
        Mainco=-1
        for PCell in ParaArr:
            ParaArr[con]=PCell.split(',')
            if len(ParaArr[con])>1:
                Mainco=con
            con+=1
        RE=[]
        con=0
        self.NameSet=ParaArr[Mainco]

        while con<len(ParaArr[Mainco]):
            i=0
            str=''
            while i<len(ParaArr):
                if i != Mainco:
                    str=str+"'"+ParaArr[i][0]+"'"
                else:
                    str=str+"'"+ParaArr[i][con]+"'"
                if i != len(ParaArr)-1:
                    str=str+","
                i+=1
            RE.append(str)
            con+=1
    #    print (RE)
        return RE


    def sets(self,Para=''):
        REArr=[]
    #    print(self)
        Para=self.Pind(Para)

        if Para:
            if isinstance(Para,list):
                con=0
                while con<self.iter and con<len(Para):
                    REArr.append(self.hanset+'('+ Para[con]+')')
                    con+=1
        else:
            con=0
            while con<self.iter:
                REArr.append(self.hanset+'()' )
                con+=1

    #    print (REArr)
        return REArr

S_todayall= HDR('get_today_all','今日股票')
S_Srltequote= HDR('get_realtime_quotes','实时五档',"['sh','sz','hs300','sz50','zxb','cyb'] ")
S_Stodaytick= HDR('get_today_ticks','个股详情','000826')

H_all= HDR('get_hist_data','个股历史快捷','000826')
H_F_all= HDR('get_h_data','个股历史',"'000826','2010-01-01'" )
H_Stick= HDR('get_tick_data','个股大盘历史详细'," '000826',"+"'"+RDate+ "'")
H_F_all_handy= PST('get_h_data',1000,'','个股历史批量')

I_today= HDR('get_index','今日大盘')
B_S= HDR('get_sina_dd','大笔交易','000826,'+RDate )

IR_D= HDR('get_deposit_rate','存款利率')
IR_L= HDR('get_loan_rate','贷款利率')
IR_RRR= HDR('get_rrr','准备金利率')
IR_Shi= HDR('shibor_data','SHIBOR')
IR_SHiQuo= HDR('shibor_quote_data','SHIBOR_问询')
IR_SHiMa= HDR('shibor_ma_data','SHIBOR_MA')
IR_LPR= HDR('lpr_data','LPR')
IR_LPRMa= HDR('lpr_ma_data','LPR_MA')

M_ms= HDR('get_money_supply','货币供给')
M_msbal= HDR('get_money_supply_bal','货币供给余量')

GDP_Y= HDR('get_gdp_year','GDP_Year')
GDP_Q= HDR('get_gdp_quarter','GDP_Quarter')
GDP_Y_for= HDR('get_gdp_for','GDP_Year_For')
GDP_Y_pull= HDR('get_gdp_pull','GDP_Year_Pull')
GDP_Y_ctb= HDR('get_gdp_contrib','GDP_Year_Contribution')

CPI_M= HDR('get_cpi','CPI_Month')
PPI_M= HDR('get_ppi','PPI_Month')
SR_Basic= HDR('get_stock_basics','基本面')
SR_Report= HDR('get_report_data','财务',RYear+','+RQuarter)
SR_Profit= HDR('get_profit_data','盈利',RYear+','+RQuarter)
SR_Opera= HDR('get_operation_data','运营',RYear+','+RQuarter)
SR_Growth= HDR('get_growth_data','成长',RYear+','+RQuarter)
SR_Debtpay= HDR('get_debtpaying_data','偿付',RYear+','+RQuarter)
SR_CashFlow= HDR('get_cashflow_data','现金流',RYear+','+RQuarter)
SR_Forcast= HDR('forecast_data','业绩预报',RYear+','+RQuarter)


MG_SH= HDR('sh_margins','融资融券_SH', "'"+RYear+"-01-01'"  )
MG_SZ= HDR('sz_margins','融资融券_SZ',"'"+RYear+"-01-01'")


def allnum_sub(PDD,conj,imax):
    i=0
    while i<imax:
        S=PDD.ix[i,conj]
        if S!='--':
            PDD.ix[i,conj]=float(S)
        i+=1
    return PDD

def allnum(PDD):
    PDD=PDD[0]
    #PDDBac=PDD
    imax=PDD.shape[0]
    jmax=PDD.shape[1]
    conj=1
    print(imax)
    print(jmax)
    while conj<jmax:
        PDD=allnum_sub(PDD,conj,imax)
        conj+=1
    return [PDD]

def timefix(PDDataF):
    i=0
    Ti={'quarter':0,'month':1,'date':2,'opDate':3}
    try:
        N =Ti[ PDDataF.columns[0] ]
    except:
        return PDDataF

    for M in PDDataF.ix[:,0]:
       PDDataF.ix[i,0]=timefix_single(PDDataF.ix[i,0],N)
       i+=1
    return PDDataF

def timefix_single(STR,N):

    if  type(STR) == pandas.tslib.Timestamp:
        return STR

    if isinstance(STR,float):
        STR=str(STR)

    if(STR.find('.')!=-1 and N==1):
        TS=STR.split('.')
        STR+='/30'
        if(TS[1]!='2' and TS[1]!='02'):
            return pandas.to_datetime('30' + TS[1] + TS[0], format="%d%m%Y")
        else:
            return pandas.to_datetime('28' + TS[1] + TS[0], format="%d%m%Y")

    if(STR.find('.')!=-1 and N==0):
        B= STR.split('.')
        B[1]=str( int(B[1])*3 )
        return pandas.to_datetime('30' + B[1] + B[0], format="%d%m%Y")

    if(STR.find('-')!=-1 and N==2 or N==3):
        TS=STR.split('-')
        return pandas.to_datetime(TS[2] + TS[1] + TS[0], format="%d%m%Y")

def savname():
    # 要判断开市还是收市了  不用了没收市前都没数据

    return time.strftime("%Y-%m-%d",time.gmtime())

def to_mongodb():
    import pymongo
    import	json
    conn=pymongo.Connection	('127.0.0.1',port	=27017)
    df=ts.get_tick_data('600848',date='2014-12-22')
    conn.db.tickdata.insert(json.loads(df.to_json(orient	='records')))

def getallkeys(sdir):
    dkeystr=str(sdir.keys() )
    allkeys=[]
    end=0
    con=-1
    Ocon=0
    while(end!=200):
        con=dkeystr.find("'",con+1)
        if con==-1:
            break

        Ocon=con+1
        con=dkeystr.find("'",con+1)

        allkeys.append(dkeystr[Ocon:con])
        end+=1

    return allkeys

def _menu(lib):
    keys=getallkeys(lib)
    j=0
    for key in keys:
        lib_list=lib[key]
        print(str(j)+'. '+key+':')
        i=0
        for hdr in lib_list:
            print('\t'+str(i)+'. '+hdr._display())
            i+=1
        j=j+1

def  _SAVE(Type='excel',Path='C:\\Users\\macbook\Desktop\\',NA='TEST',para=''):

    Type=Type.lower()
    SAVEHDL={'excel':['to_excel','xlsx'],'csv':['to_csv','csv'],'hdf5':['to_hdf','h5'],'json':['to_json'],'mysql':['to_sql'],'mongodb':['to_mongodb']}
    SAVEPATH= Path+NA
    #Active the handler
    if para!='':
        para=','+para
    try:
        if len(SAVEHDL[Type])>1:
            ST= SAVEHDL[Type][0] + "(" + "'" + SAVEPATH + "." + SAVEHDL[Type][1] +"'" + para + ")"

        else:
            ST= SAVEHDL[Type][0] + "(" + SAVEPATH  + para + ")"
    except:
        print('jj')

    else:
        if not ST:
            return 'ERROR'
        else:
            return ST

def _getdata(s_handle=[],para='',columns=['']):  #colums should be keys arrays
    dataset=[]
    if isinstance(s_handle , HDR):
        s_handle=[s_handle]

        for part_han in s_handle:
            data= pandas.DataFrame()
            #handle=eval('ts.'+part_han)
            #print('ts.'+part_han.han() )
            if para=='':
                data=eval( 'ts.'+part_han._Han() )
            else:
                #data=handle(para)
                data=eval('ts.'+part_han._Han(para) )

            if not columns[0] :
                dataset.append( timefix(data) )
            else:
                dataset.append( timefix( data[columns] ) ) #columns is array
        return dataset

    if isinstance(s_handle, PST):
        data= pandas.DataFrame()

        if para=='':
            Hans= s_handle.sets()
        else:
            Hans= s_handle.sets(para)

        print(Hans)  #test

        for Han in Hans:
            data=eval('ts.'+Han )

            if not columns[0] :
                dataset.append( data )
            else:
                dataset.append( data[columns] ) #columns is array
        return dataset


def _intergralsheet(dataset):
    '''
    a = Series(range(5))
    b = Series(np.linspace(4, 20, 5))
    df = pd.concat([a, b], axis=1)
    print df

    df = DataFrame()
    index = ['alpha', 'beta', 'gamma', 'delta', 'eta']
    for i in range(5):
        a = DataFrame([np.linspace(i, 5*i, 5)], index=[index[i]])
        df = pd.concat([df, a], axis=0)
    print df
    '''
    finaldata=pandas.DataFrame()
    for datasheet in dataset:
        finaldata=pandas.concat([finaldata,datasheet],axis=1)
        #其中的axis=1表示按列进行合并，axis=0表示按行合并，并且，Series都处理成一列，所以这里如果选axis=0的话，将得到一个10×1的DataFrame。下面这个例子展示了如何按行合并DataFrame成一个大的DataFrame：

    return [finaldata]

def main():

    print("--------------Game Starting------------")

    # print(dir(ts))
    NameSpace=dir(ts)
    # Make a self lib, Good for search
    HTFlib={'TodayStock':[S_todayall,S_Srltequote,S_Stodaytick],'HistoryStock':[H_all,H_Stick,H_F_all,H_F_all_handy],'TodayIndex':[I_today],'TodayBig':[B_S],'InterestRate':[IR_D,IR_L,IR_RRR,IR_Shi,IR_SHiQuo,IR_SHiMa,IR_LPR,IR_LPRMa],'Monetory':[M_ms,M_msbal],'GDP':[GDP_Y,GDP_Q,GDP_Y_for,GDP_Y_pull,GDP_Y_ctb],'CPI':[CPI_M],'PPI':[PPI_M],'StockReport':[SR_Basic,SR_Report,SR_Profit,SR_Opera,SR_Growth,SR_Debtpay,SR_CashFlow,SR_Forcast],'Margin':[MG_SH,MG_SZ]}

    while( input (" type 'R' to start everyday work       ").lower()== 'r'):
        routine_Bool=int( input('for stock or macro: 0 or 1         ' ) )
        if(routine_Bool):

            savingcont=0
            Path='C:\\\\Users\\\\macbook\\\\Desktop\\\\研究数据\\\\个股\\\\AutoMacro\\\\'
            NA=['GDP','CPI','SHIBOR','LPR','PPI','MS','RRR','MG_SH']
            Type='excel'
            Rou=[]
            i=0

            Rou.append(_getdata(GDP_Q,'',['quarter','gdp_yoy','pi_yoy','si_yoy','ti_yoy']) )
            Rou.append(_getdata(CPI_M,'',['month','cpi']) )
            Rou.append(_getdata(IR_Shi,'',['date','ON','1W','2W','1M','3M','6M','9M','1Y']) )
            Rou.append(_getdata(IR_LPR,'',['date','1Y']) )
            Rou.append(_getdata(PPI_M,'',['month','ppiip','ppi','qm','rmi','pi','cg','food','clothing','roeu','dcg']) )
            Rou.append( allnum( _getdata(M_ms,'',['month','m2_yoy','m1_yoy','m0_yoy','cd','qm','ftd','sd','rests']) ) )
            Rou.append( allnum(_getdata(IR_RRR,'',['date','now']) ) )
            Rou.append(_getdata(MG_SH,'',['opDate','rzye','rzmre','rqyl','rqylje','rqmcl','rzrqjyzl'])  )


            for N in Rou:
                if type(N[0])==pandas.DataFrame:

                    STail=_SAVE(Type,Path,NA[i],'')
                    print('Rou['+str(i)+'][0]'+'.'+STail)
                    eval('Rou['+str(i)+'][0]'+'.'+STail)
                    i+=1

        else:
            savingcont=0
            Path='C:\\\\Users\\\\macbook\\\\Desktop\\\\研究数据\\\\股票历史\\\\'  #change this
            NA=['000826启迪桑德','000959首钢股份','300187永清环保','300284苏交所','600428中远航运','600896中海海盛','601808中海油服','601866中海集运','601919中国远洋','600276恒瑞医药','002004华邦健康','600470六国化工','600576万家文化','002432九安医疗']
            #change this
            Type='excel'
            Rou=[]
            i=0

            Rou=_getdata(H_F_all_handy,'000826,000959,300187,300284,600428,600896,601808,601866,601919,600276,002004,600470,600576,002432|2013-01-01',[''])   #change this



            for na in NA:
                STail=_SAVE(Type,Path,na,para="")
                print('Rou['+ str(i)+']'+'.'+STail)
                eval('Rou['+str(i)+']'+'.'+STail)
                i+=1
                if i == len(NA):
                    break


    while( input(" type 'end' to end the program ").lower() !='end'):

        _menu(HTFlib)
        keys=getallkeys(HTFlib)
        Key=input("--Key--:   ")
        if Key.isdigit():
            Key=keys[int(Key) ]


        Sub=(input("\t--Subscript--:   ") )
        Columns=input("--ColumnsKey like 'a,b,c,d'--:  ").split(',')
        para=input("--Para--")

        Han=eval( 'HTFlib[Key]['+Sub+']')

        dataset=_getdata(Han,para,Columns)

        #dataset=_intergralsheet(dataset)
        defaultNA=[]

        if isinstance(Han, HDR):
            defaultNA.append(savname()+Han.display)
        elif isinstance(Han,PST):
            for Han_NA in Han.NameSet:
                defaultNA.append( savname()+Han_NA  )
        else:
            for P_Han in Han:
                defaultNA.append( savname()+P_Han.display )

        Type='excel'
        #Path='C:\\\\Users\\\\macbook\\\\Desktop\\\\'
        Path='C:\\\\Users\\\\macbook\\\\Desktop\\\\研究数据\\\\股票历史\\\\'
        NA_SET=input("type your nameset like 'a,b,c' :" ).split(',')
        if not NA_SET[0]:
            NA_SET=defaultNA

        i=0
        for NA in NA_SET:
            STail=_SAVE(Type,Path,NA,para="")
            print('dataset['+ str(i)+']'+'.'+STail)
            eval('dataset['+str(i)+']'+'.'+STail)
            i+=1
            if i == len(NA_SET):
                break
    #TuHandle=eval('ts.'+NameSpace[N])
    #Active
    #TuHandle()
    #eval('ts.'+NameSpace[N]+'()')
    input("--------------End----------------")

main()
