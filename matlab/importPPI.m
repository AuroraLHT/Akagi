%% Import data from spreadsheet
% Script for importing data from the following spreadsheet:
%
%    Workbook: C:\Users\macbook\Desktop\�о�����\����\AutoMacro\PPI.xlsx
%    Worksheet: Sheet1
%
% To extend the code for use with different selected data or a different
% spreadsheet, generate a function instead of a script.

% Auto-generated by MATLAB on 2016/10/21 20:52:02
SlArea='B2:M';
A=size(xlsread('C:\Users\macbook\Desktop\�о�����\����\AutoMacro\PPI.xlsx'));
SlArea=[SlArea,int2str(A(1)+1)];

%% Import the data, extracting spreadsheet dates in Excel serial date format
[~, ~, raw, dates] = xlsread('C:\Users\macbook\Desktop\�о�����\����\AutoMacro\PPI.xlsx','Sheet1',SlArea,'',@convertSpreadsheetExcelDates);
raw(cellfun(@(x) ~isempty(x) && isnumeric(x) && isnan(x),raw)) = {''};
dates(cellfun(@(x) ~isempty(x) && isnumeric(x) && isnan(x),dates)) = {''};
raw = raw(:,[2,3,4,5,6,7,8,9,10,11]);
dates = dates(:,1);

%% Exclude rows with non-numeric cells
I = ~(all(cellfun(@(x) (isnumeric(x) || islogical(x)) && ~isnan(x),raw),2) & all(cellfun(@isnumeric,dates),2)); % Find rows with non-numeric cells
raw(I,:) = [];
dates(I,:) = [];

%% Create output variable
data = reshape([raw{:}],size(raw));

%% Allocate imported array to column variable names
PPI_M = datetime([dates{:,1}].', 'ConvertFrom', 'Excel');
ppiip = data(:,1);
ppi = data(:,2);
qm = data(:,3);
rmi = data(:,4);
pi1 = data(:,5);
cg = data(:,6);
food = data(:,7);
clothing = data(:,8);
roeu = data(:,9);
dcg = data(:,10);

% For code requiring serial dates (datenum) instead of datetime, uncomment
% the following line(s) below to return the imported dates as datenum(s).

% month1=datenum(month1);

%% Clear temporary variables
clearvars data raw dates I SlArea A;