%%
% config for plot 
outlook=0;
distribution=1;

returndis=1;
returndis_cOo=1;
returndis_ycOc=1;
returndis_ycOo=1;
subor=1;
plotnum=outlook+distribution+returndis;

%% basic statement
 disp(sheetname(fig_c))
 
 fprintf( 'open:  %4.2f\n', Av_Oset) ;
 fprintf( 'close:  %4.2f\n', Av_Cset );
 fprintf( 'turnover:  %4.1f %% \n', ( (Av_Cset-Av_Oset)/LastClose*100 ) )
 h=figure(fig_c); 
%%  outlook data
if outlook==1
     Y=sim(net,P(:,1:PLen));
     DLen=length(stock{1});
     Ydate=stock{1};
     Ydate=[Ydate;Ydate(SDLen)+1];
     YDateLen=DLen+1;
     PS=0;
end

%% returndis data
if returndis==1
    if returndis_cOo
        returnVector_cOo=(Cset-Oset)./Oset;
        nbins = 50;
        returnVector_cOo=returnVector_cOo.*100;  %convert to percentage

        mu_cOo=mean(returnVector_cOo);
        sigma_cOo=std(returnVector_cOo);

        %Normalization 

        X=-10:0.1:10;
        [Counts_cOo,Edge_cOo]=histcounts(returnVector_cOo,nbins);    

        %PosDensity= 1/(sigma*sqrt(2*pi)  ) *exp ( -(X-mu ).^2/(2*sigma^2)   );
        PosDensity_cOo= max(Counts_cOo) *exp ( -(X-mu_cOo ).^2/(2*sigma_cOo^2)   );
    end
    if returndis_ycOo
        returnVector_ycOo=(Oset-LastClose)./LastClose;
        nbins = 50;
        returnVector_ycOo=returnVector_ycOo.*100;  %convert to percentage

        mu_ycOo=mean(returnVector_ycOo);
        sigma_ycOo=std(returnVector_ycOo);

        %Normalization 

        X=-10:0.1:10;
        [Counts_ycOo,Edge_ycOo]=histcounts(returnVector_ycOo,nbins);    

        %PosDensity= 1/(sigma*sqrt(2*pi)  ) *exp ( -(X-mu ).^2/(2*sigma^2)   );
        PosDensity_ycOo= max(Counts_ycOo) *exp ( -(X-mu_ycOo ).^2/(2*sigma_ycOo^2)   );        
    end
    if returndis_ycOc
        returnVector_ycOc=(Cset-LastClose)./LastClose;
        nbins = 50;
        returnVector_ycOc=returnVector_ycOc.*100;  %convert to percentage

        mu_ycOc=mean(returnVector_ycOc);
        sigma_ycOc=std(returnVector_ycOc);

        %Normalization 

        X=-10:0.1:10;
        [Counts_ycOc,Edge_ycOc]=histcounts(returnVector_ycOc,nbins);    

        %PosDensity= 1/(sigma*sqrt(2*pi)  ) *exp ( -(X-mu ).^2/(2*sigma^2)   );
        PosDensity_ycOc= max(Counts_ycOc) *exp ( -(X-mu_ycOc ).^2/(2*sigma_ycOc^2)   );           
        
    end
end
%% Outlook plot
   if outlook==1
     subplot(plotnum ,1,subor)
     subor=subor+1;
     
     plot(Ydate(6+PS:YDateLen),Y(1,1+PS:PLen),'b--o');
     hold on;
     plot(Ydate(6+PS:YDateLen),Y(2,1+PS:PLen),'y--o');
     hold on; 
     plot(Ydate(6+PS:DLen),T(1,2+PS:TLen),'r');
     hold on;
     plot(Ydate(6+PS:DLen),T(2,2+PS:TLen),'g');
     hold off;
 
     xlabel('date (d)','Interpreter','Latex','FontSize',12)
     ylabel('Price (rmb)','Interpreter','Latex','FontSize',12)
     legend('Simulated Open','Simulated Close','Open','Close')
     tit= strcat( 'simulation of stock: ',sheetname(fig_c)) ;
     title(tit);
     %set(gca, 'XMinorTick','on','YMinorTick','on','xtick',...
     %    [6:1:12],'ytick',[1.2:0.3:2.5],'xticklabel',...
     %    [6:1:12],'yticklabel',[1.2:0.3:2.5]);
     %axis([5.75 12.5 1.14 2.54])
   end
   
 %% Distribution  
    if distribution==1
     subplot(plotnum,1,subor)
     subor=subor+1;
     
     plot(Oset,Cset,'o','MarkerEdgeColor','k','MarkerFaceColor','b','MarkerSize',4)
     hold on
     plot(Av_Oset,Av_Cset,'o','MarkerEdgeColor','k','MarkerFaceColor','r','MarkerSize',6)
     hold on
     plot(KMset(1,:),KMset(2,:),'o','MarkerEdgeColor','k','MarkerFaceColor','g','MarkerSize',8  )
     hold off
     
     xlabel('Open Price (rmb)','Interpreter','Latex','FontSize',12)
     ylabel('Close Price (rmb)','Interpreter','Latex','FontSize',12)
     
    % axis equal
    % axis([LastClose*0.9,LastClose*1.1,LastClose*0.9,LastClose*1.1])
     
     legend('Open Over Close','Mean','KMean')
     title('Multiple Simulation Distribution')
    end
    
 %% Return Distribution   
    if returndis
       subplot(plotnum,1,subor)
       subor=subor+1;
       
      if returndis_cOo
       histogram(returnVector_cOo,nbins);  %Syntax :histogram(X,nbins)
       hold on       
       plot(X,PosDensity_cOo,'r','LineWidth',1.5);
       hold on
       
      end
      
      if returndis_ycOo 
       histogram(returnVector_ycOo,nbins);
       hold on
       
      end
      
      if returndis_ycOc
       histogram(returnVector_ycOc,nbins); 
       hold on
       
      end
      
       hold off
       
       if returndis_cOo==1 && returndis_ycOo==1 && returndis_ycOc==1  
        legend('cOo','Nor_cOo','ycOo','ycOc');
       elseif returndis_cOo==1 && returndis_ycOo==1 && returndis_ycOc==0
        legend('cOo','Nor_cOo','ycOo');
       elseif returndis_cOo==1 && returndis_ycOo==0 && returndis_ycOc==1  
        legend('cOo','Nor_cOo','ycOc');
       elseif returndis_cOo==0 && returndis_ycOo==1 && returndis_ycOc==1  
        legend('ycOo','ycOc');
       elseif returndis_cOo==0 && returndis_ycOo==0 && returndis_ycOc==1  
        legend('ycOc');
       elseif returndis_cOo==0 && returndis_ycOo==1 && returndis_ycOc==0  
        legend('ycOo');
       elseif returndis_cOo==1 && returndis_ycOo==0 && returndis_ycOc==0  
        legend('cOo','Nor_cOo');
       else     
         1;  %......
       end
       
       %xlabel('ReturnRatio (%)','Interpreter','Latex','FontSize',12)
       xlabel('ReturnRatio (%)','FontSize',12)
       ylabel('Distribution ','Interpreter','Latex','FontSize',12)
       title('Overday Returning Ratio Distribution')
       T=strcat('mu:', num2str(mu_cOo),' sigma:',num2str( sigma_cOo) );
       
       text( X( ceil( length(PosDensity_cOo) /2 ) ) +1 , PosDensity_cOo(ceil( length(PosDensity_cOo)/2 ) ) -1,T );
       
    end
    
    
%% Save fig
figset=[figset,h];
figsavename=sheetname{fig_c};
for i=1:length(figsavename)
    if(figsavename(i)=='.')
        figsavename=figsavename(1:i-1);
        break;
    end
    if( i==length(figsavename))
        disp('sheetname do not have dot ');
    end
end
storepath=strcat(figsavepath,'\',figsavename);
storepath2=strcat(storepath,'.fig');
print(h,storepath,'-r300','-dpng');
saveas(h,storepath2)