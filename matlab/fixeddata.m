%sheetname={'300284.xlsx'};
stockpath='C:\Users\macbook\Desktop\研究数据\股票历史\';
allsheet = dir(stockpath);
lengthc=0;
for i=1:length(allsheet)
%for i=3:4
    if ( ~allsheet(i).isdir )
        lengthc=lengthc+1;
    end
end
sheetname= cell(1,lengthc);
j=1;
for i=1:length(allsheet)    
    if (~allsheet(i).isdir )
        sheetname{j}=allsheet(i).name;
        j=j+1;
    end
end


clearvars allsheet i j lengthc 