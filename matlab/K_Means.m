% K-means
function [ KMat ] = K_Means( DMat,k ) %DMat = demension * length
%the columns num represent the number of dataset
%the row num represent the dimension
%the row num in KMat represent the order of the centroids
    %s= rng;

    centroids=randCent(DMat,k); %return Dmat's demension *k matrix
    Dmatsize=size(DMat);
    clusterAssement= zeros(k,Dmatsize(2)); %return k*Dmatsize matrix
    clusterChanged=true;
    
    while( clusterChanged==true )
      clusterChanged = false;
      for i=1:Dmatsize(2)
        minDist= Inf(1);
        minIndex = -1;
        for j=1:k  %：k
            D=disEclud(centroids(:,j),DMat(:,i) );
            if minDist>D
                minDist=D;
                minIndex= j;
            end
        end
        if (clusterAssement(1,i)~=minIndex)
            clusterChanged=true;
        end
        clusterAssement(:,i)= minIndex;
        %minDist=minDist^2;

      end

      for i= 1:k
        index_all = clusterAssement(1,:);%取出样本�?��簇的索引�?
        %disp(index_all);
        thiscen_ind=[];
        sampleInClust=[];
        for j=1:length(index_all)
          if(index_all(j)==i)
            thiscen_ind =[thiscen_ind,j] ;    %取出�?��属于第ci个簇的索引�?
          end          
        end  
        sampleInClust = DMat(:,thiscen_ind);%取出属于第i个簇的所有样本点
        centroids(:,i) = mean(sampleInClust');  %return 1*samLen vector        
      end
      
    end
    KMat= centroids;
    %Ind=sampleInClust;
end

function distance= disEclud(X,Y)
    distance= sqrt((X - Y)'*(X - Y)) ;
end

function RE =randCent(Mat,k)
  Matsize=size(Mat);
  n=Matsize(1);
  centroids= zeros(n,k);
  for j=1:n
    MinM=min( Mat(j,:) );
    MaxM=max(Mat(j,:) );
    rangeJ= (MaxM-MinM);
    centroids(j,:) = MinM + rangeJ *rand(1,k);
  end
  RE=centroids;
end
