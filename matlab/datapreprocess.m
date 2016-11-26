% preprocess data
 stock={date1,open1,high,close,low,volume,amount};

[a,G]=dateextend(stock{1},GDP{1},Col_concat(GDP,2));
[a,C]=dateextend(stock{1},CPI{1},Col_concat(CPI,2));
%[a,LR]=dateextend(stock{1},LPR{1},Col_concat(LPR,2));
[a,ms]=dateextend(stock{1},MS{1},Col_concat(MS,2));
[a,Pro]=dateextend(stock{1},PPI{1},Col_concat(PPI,2));
[a,Rrr]=dateextend(stock{1},rrr{1},Col_concat(rrr,2));
[a,SHIB]=dateextend(stock{1},SHIBOR{1},Col_concat(SHIBOR,2));
[a,SHM]=dateextend(stock{1},SHMargin{1},Col_concat(SHMargin,2));
[a,SH_I]=dateextend(stock{1},SH_Index{1},Col_concat(SH_Index,2));

opensize=size(stock{2});
%P=antiorder([ stock{2}(1:opensize(1)-4)';stock{2}(2:opensize(1)-3)';stock{2}(3:opensize(1)-2)';stock{2}(4:opensize(1)-1)';stock{2}(5:opensize(1))';stock{4}(1:opensize(1)-4)';stock{4}(2:opensize(1)-3)';stock{4}(3:opensize(1)-2)';stock{4}(4:opensize(1)-1)';stock{4}(5:opensize(1))';G';C';LR';ms';Pro';Rrr';SHIB';SHM']');
%P=antiorder([ stock{2}(1:opensize(1)-4)';stock{2}(2:opensize(1)-3)';stock{2}(3:opensize(1)-2)';stock{2}(4:opensize(1)-1)';stock{2}(5:opensize(1))';stock{4}(1:opensize(1)-4)';stock{4}(2:opensize(1)-3)';stock{4}(3:opensize(1)-2)';stock{4}(4:opensize(1)-1)';stock{4}(5:opensize(1)),G(1:opensize(1)-4,:),C(1:opensize(1)-4,:),ms(1:opensize(1)-4,:),Pro(1:opensize(1)-4,:),Rrr(1:opensize(1)-4,:),SHIB(1:opensize(1)-4,:),SHM(1:opensize(1)-4,:)]);
P=antiorder([StockDaDate(stock{2},5,opensize(1)),StockDaDate(stock{3},5,opensize(1)),StockDaDate(stock{4},5,opensize(1)),StockDaDate(stock{5},5,opensize(1)),StockDaDate(stock{6},5,opensize(1)),StockDaDate(stock{7},5,opensize(1)),G(1:opensize(1)-4,:),C(1:opensize(1)-4,:),ms(1:opensize(1)-4,:),Pro(1:opensize(1)-4,:),Rrr(1:opensize(1)-4,:),SHIB(1:opensize(1)-4,:),SHM(1:opensize(1)-4,:),SH_I(1:opensize(1)-4,:)]);

P=P';
%T=antiorder([ stock{2}(1:opensize(1)-4),stock{4}(1:opensize(1)-4)]);
T=antiorder([ stock{2}(1:opensize(1)-4),stock{4}(1:opensize(1)-4)]);
T=T';