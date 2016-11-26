function [ res,res2 ] = dateextend( Ori,Raw,Rawd )
%[a,b]=dateextend(date1,quarter,[gdp';gdp_yoy']');
%   数据要降序才有用
    j=1;
    Rawsize=size(Raw);
    Rawsize=Rawsize(1);
    Orisize=size(Ori);
    for i=1:Orisize(1)
       
     if ((Ori(i)>=Raw(j)))
         Raw=[Raw(1:j);Raw(j);Raw(j+1:Rawsize(1) )];
         Rawd=[Rawd(1:j,:);Rawd(j,:);Rawd(j+1:Rawsize(1),:)];
         Rawsize=Rawsize+1;
     end
     j=j+1;
     
    
    end
    
    res=Raw(1:Orisize(1));
    res2=Rawd(1:Orisize(1),:);
end

