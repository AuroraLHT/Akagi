%neural test
%% plot preparing
 stock{1}=antiorder(stock{1});
 SDLen=length(stock{1});
 PLen=length(P);
 TLen=length(T);

loopflag=1; % determine the necessary to simulate the stock more than one time
loopTimes=50*4; %Minimum loop time also determin the size of the dataset
loopExit=0;
Oset=zeros(1,loopTimes);
Cset=zeros(1,loopTimes);
LastClose=P(11,PLen);
%% Neural Network
 
 if loopflag==1
     j=1; %storage counter
     i=1; %while loop counter
     
     while i<=loopTimes
     %network
         net=feedforwardnet(10,'trainlm'); %initial a BP neural net work  train	

        %trainlm	Levenberg-Marquardt backpropagation
        %trainbr	Bayesian regularization backpropagation
        %trainscg	Scaled conjugate gradient backpropagation
        %trainrp	Resilient backpropagation
        
         net=train(net,P(:,1:PLen-2),T(:,2:TLen-1)); %training
         TP=sim(net,P(:,PLen));
         if(TP(1)<=LastClose*1.1 && TP(1)>=LastClose*0.9 && TP(2)<=LastClose*1.1 && TP(2)>=LastClose*0.9 )
            Oset(j)=TP(1);Cset(j)=TP(2); 
            j=j+1;
         else
             loopTimes=loopTimes+1;
         end
         i=i+1;
         
         if loopExit==1
             break;
         end
     end
     Av_Oset=mean(Oset);
     Av_Cset=mean(Cset);
     KMset=K_Means([Oset;Cset],2);
     Mse_Oset=mse(Oset);
     Mse_Cset=mse(Cset);
 else
     net=feedforwardnet; %initial a BP neural net work
     net=train(net,P(:,1:PLen-2),T(:,2:TLen-1)); %training
 end
 netset=[netset,net];  %store the net
 
 %%drawing department
    figcreat;
    figset=[figset,h]; 
 %% backup
%  
%  Y=sim(net,P(:,1:PLen));
%  
%  disp(sheetname(fig_c))
%  fprintf( 'open:  %4.2f\n', Y(1,PLen) )
%  fprintf( 'close:  %4.2f\n', Y(2,PLen) )
%  fprintf( 'turnover:  %4.1f %% \n', (Y(2,PLen)-Y(1,PLen))/Y(1,PLen)*100 )
%  
%  DLen=length(stock{1});
%  Ydate=stock{1};
% 
%  Ydate=[Ydate;Ydate(SDLen)+1];
%  YDateLen=DLen+1;
%  
%  PS=0;
%  
%  h=figure(fig_c); 
%      subplot(2,1,1)
%     
%      plot(Ydate(6+PS:YDateLen),Y(1,1+PS:PLen),'b--o');
%      hold on;
%      plot(Ydate(6+PS:YDateLen),Y(2,1+PS:PLen),'y--o');
%      hold on; 
%      plot(Ydate(6+PS:DLen),T(1,2+PS:TLen),'r');
%      hold on;
%      plot(Ydate(6+PS:DLen),T(2,2+PS:TLen),'g');
%      hold off;
%  
%      xlabel('date (d)','Interpreter','Latex','FontSize',12)
%      ylabel('Price (rmb)','Interpreter','Latex','FontSize',12)
%      legend('Simulated Open','Simulated Close','Open','Close')
%      tit= strcat( 'simulation of stock: ',sheetname(fig_c)) ;
%      title(tit);
%      %set(gca, 'XMinorTick','on','YMinorTick','on','xtick',...
%      %    [6:1:12],'ytick',[1.2:0.3:2.5],'xticklabel',...
%      %    [6:1:12],'yticklabel',[1.2:0.3:2.5]);
%      %axis([5.75 12.5 1.14 2.54])
%      
%      subplot(2,1,2)
%      plot(Oset,Cset,'o','MarkerEdgeColor','k','MarkerFaceColor','b','MarkerSize',4)
%      hold on
%      plot(Av_Oset,Av_Cset,'o','MarkerEdgeColor','k','MarkerFaceColor','r','MarkerSize',6)
%      hold on
%      plot(KMset(1,:),KMset(2,:),'o','MarkerEdgeColor','k','MarkerFaceColor','g','MarkerSize',8  )
%      hold off
%      
%      xlabel('Open Price (rmb)','Interpreter','Latex','FontSize',12)
%      ylabel('Close Price (rmb)','Interpreter','Latex','FontSize',12)
%      legend('Open Over Close','Mean','KMean')
%      title('Multiple Simulation Distribution')
%  
