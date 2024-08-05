function [] = calculateMeanError(fileIn,fileOut)

if ~exist("fileIn","var")
    [filename, pathname] = uigetfile( ...
       {'*.txt';'*.*'}, ...
        'Import data');
    if filename==0
        return;
    end
    fileIn=[pathname,filename];
    
end
data=importdata(fileIn);

siz=size(data.data);
if siz(2)<2
    warning('Not enough data found');
    return;
end

[C,~,IC]=unique(data.data(:,1));

[pathname,name,~]=fileparts(fileIn);

if ~exist("fileOut","var")
    [filename, pathname] = uiputfile( ...
       {'*.txt';'*.*'}, ...
        'Save data',sprintf('%s/%s_MeanSigma',pathname,name));
    if filename==0
        return;
    end
    fileOut=[pathname,filename];
    
end

fid=fopen(fileOut,"w");
fprintf(fid,"%s",data.textdata{1});
fprintf(fid,"\t%s\tsigma_%s",data.textdata{ceil(1.5:0.5:end)});
fprintf(fid,"\n");

for k=1:numel(C)
    ind=find(IC==k);
    values=zeros(1,(siz(2)-1)*2);
    for q=1:siz(2)-1
        values(2*q-1)=mean(data.data(ind,1+q));
        values(2*q)=std(data.data(ind,1+q));
    end
    fprintf(fid,'%e',C(k));
    fprintf(fid,'\t%e',values);
    fprintf(fid,'\n');

end
fclose(fid);

end