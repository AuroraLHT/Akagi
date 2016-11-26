import sys
import tushare as ts
import time
import pandas

class Han:
    'to creat a class hold basic infomation for the handler'
    Hancount=0
    def __init__(self,name,defaultPara):
        self.name=name
        self.defaultPara=defaultPara
        Hancount+=1
    def __del__(self):
        print(self.__class__.__name__)


def savname():
    return time.strftime("%Y%m%d",time.gmtime())

def to_mongodb():
    import pymongo
    import	json
    conn=pymongo.Connection	('127.0.0.1',port	=27017)
    df=ts.get_tick_data('600848',date='2014-12-22')
    conn.db.tickdata.insert(json.loads(df.to_json(orient	='records')))

def getallkeys(sdir):
    dkeystr=str(dir.keys() )
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

def _getdata(s_handle=['get_today_all'],para='',columns=['']):  #colums should be keys arrays
    dataset=[]
    if(type(s_handle)==type('')):
        s_handle=[s_handle]
    for part_han in s_handle:
        data= pandas.DataFrame()
        handle=eval('ts.'+part_han)
        if para=='':
            data=handle()
        else:
            #data=handle(para)
            data=eval('ts.'+part_han+'('+para+')')
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

    '''
    >>> import tushare
    >>> dir(tushare)
    ['Bond', 'Equity', 'Fund', 'Fundamental', 'Future', 'HKequity', 'IV', 'Idx', 'Ma
    cro', 'Market', 'Master', 'Options', 'Subject', '__author__', '__builtins__', '_
    _cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__p
    ath__', '__spec__', '__version__', 'broker_tops', 'cap_tops', 'datayes', 'day_bo
    xoffice', 'day_cinema', 'forecast_data', 'fund_holdings', 'get_area_classified',
     'get_cashflow_data', 'get_concept_classified', 'get_cpi', 'get_debtpaying_data'
    , 'get_deposit_rate', 'get_gdp_contrib', 'get_gdp_for', 'get_gdp_pull', 'get_gdp
    _quarter', 'get_gdp_year', 'get_gem_classified', 'get_growth_data', 'get_h_data'
    , 'get_hist_data', 'get_hists', 'get_hs300s', 'get_index', 'get_industry_classif
    ied', 'get_latest_news', 'get_loan_rate', 'get_money_supply', 'get_money_supply_
    bal', 'get_notices', 'get_operation_data', 'get_ppi', 'get_profit_data', 'get_re
    altime_quotes', 'get_report_data', 'get_rrr', 'get_sina_dd', 'get_sme_classified
    ', 'get_st_classified', 'get_stock_basics', 'get_suspended', 'get_sz50s', 'get_t
    erminated', 'get_tick_data', 'get_today_all', 'get_today_ticks', 'get_token', 'g
    et_zz500s', 'guba_sina', 'inst_detail', 'inst_tops', 'internet', 'is_holiday', '
    latest_content', 'lpr_data', 'lpr_ma_data', 'month_boxoffice', 'new_stocks', 'no
    tice_content', 'profit_data', 'realtime_boxoffice', 'set_token', 'sh_margin_deta
    ils', 'sh_margins', 'shibor_data', 'shibor_ma_data', 'shibor_quote_data', 'stock
    ', 'sz_margin_details', 'sz_margins', 'top_list', 'trade_cal', 'util', 'xsg_data
    ']
    '''

    # print(dir(ts))
    NameSpace=dir(ts)
    # Make a self lib, Good for search
    HTFlib={'TodayStock':['get_today_all','ts.get_realtime_quotes','get_today_ticks'],'HistoryStock':['get_hist_data','get_h_data'],'TodayIndex':['get_index'],'TodayBig':['get_sina_dd'],'InterestRate':['get_deposit_rate','get_loan_rate','get_rrr','shibor_data','shibor_quote_data','shibor_ma_data','lpr_data','lpr_ma_data'],'Monetory':['get_money_supply','get_money_supply_bal'],'GDP':['get_gdp_year','get_gdp_quarter','get_gdp_pull','get_gdp_contrib'],'CPI':['get_cpi'],'PPI':['get_ppi'],'StockReport':['get_stock_basics','get_report_data','get_profit_data','get_operation_data','get_growth_data','get_debtpaying_data','get_cashflow_data'],'Margin':['sh_margins','sz_margins']}
    while( input(" type 'end' to end the program ").lower() !='end'):

        print(str(HTFlib)+'\n\n')
        Key=input("--Key--:   ")
        Sub=(input("\t--Subscript--:   ") )
        Columns=input("--ColumnsKey like 'a,b,c,d'--:  ").split(',')
        para=input("--Para--")

        Han=eval( 'HTFlib[Key]['+Sub+']')
        if type(Han)==type(''):
            Han=[Han]
       
        dataset=_getdata(Han,para,Columns)
        dataset=_intergralsheet(dataset)
        defaultNA=[]

        for P_Han in Han:
            defaultNA.append( savname()+P_Han.replace('get_','') )

        Type='excel'
        Path='C:\\\\Users\\\\macbook\Desktop\\\\'
        NA_SET=input("type your nameset like 'a,b,c' :" ).split(',')
        if not NA_SET[0]:
            NA_SET=defaultNA

        i=0
        for NA in NA_SET:
            STail=_SAVE(Type,Path,NA,para="")
            print('dataset['+ str(i)+']'+'.'+STail)
            eval('dataset['+str(i)+']'+'.'+STail)

    #TuHandle=eval('ts.'+NameSpace[N])
    #Active
    #TuHandle()
    #eval('ts.'+NameSpace[N]+'()')
    input("--------------End----------------")

main()
