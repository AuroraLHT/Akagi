function [ R ] = StockDaDete( Ori, X, Len )
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here
    RT=zeros(Len-4,5);
    for i=1:X
        RT(:,i)=Ori(i:Len-X+i);
    end
    R=RT;
end

