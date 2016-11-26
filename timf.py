import tushare
import pandas


def timefix(STR,N):
    if isinstance(STR,float):
        STR=str(STR)
    
    if(STR.find('.')!=-1 and N==1):
        STR=STR.replace('.','/')
        STR+='/30'
        return STR

    if(STR.find('.')!=-1 and N==0):
        B= STR.split('.')
        B[1]=str( int(B[1])*3 )
        return B[0]+'/'+B[1]+'/30'
    
    if(STR.find('-')!=-1 and N==2):
        STR=STR.replace('-','/')
        return STR

Ti={'quarter':0,'month':1,'date':2}

test=tushare.get_gdp_quarter()
i=0
N =Ti[ test.columns[0] ]  
for M in test.ix[:,0]:
         
   test.ix[i,0]=timefix(test.ix[i,0],N)
   i+=1



