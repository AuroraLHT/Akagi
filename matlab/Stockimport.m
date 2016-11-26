function [ date1,open1,high,close,low,Vol,amount ] = Stockimport( sheetname,add )

%% Import data from spreadsheet
% Script for importing data from the following spreadsheet:
%
%    Workbook: 
%    Worksheet: Sheet1
%
F_add=[add,sheetname];
SlArea='A2:G';
A=size(xlsread(F_add));
SlArea=[SlArea,int2str(A(1)+1)];

%% Import the data, extracting spreadsheet dates in Excel serial date format
[~, ~, raw, dates] = xlsread(F_add,'Sheet1',SlArea,'',@convertSpreadsheetExcelDates);
raw = raw(:,[2,3,4,5,6,7]);
dates = dates(:,1);

%% Create output variable
data = reshape([raw{:}],size(raw));

%% Allocate imported array to column variable names
date1 = datetime([dates{:,1}].', 'ConvertFrom', 'Excel');
open1 = data(:,1);
high = data(:,2);
close = data(:,3);
low = data(:,4);
Vol = data(:,5);
amount = data(:,6);

% For code requiring serial dates (datenum) instead of datetime, uncomment
% the following line(s) below to return the imported dates as datenum(s).

% date1=datenum(date1);

%% Clear temporary variables
%clearvars data raw dates;


end

