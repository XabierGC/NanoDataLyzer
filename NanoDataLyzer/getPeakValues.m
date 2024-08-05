function getPeakValues(dirName,filePath)

CD=cd;

scanDir(dirName,filePath);

cd(CD);
end


function scanDir(dirName,filePath)

cd(dirName)
dirs=dir;
for k=3:numel(dir)
    if dirs(k).isdir
        scanDir(dirs(k).name,filePath);
    else
        [~,~,ext]=fileparts(dirs(k).name);
        if strcmp(ext,'.ndl')
            load(dirs(k).name,'-mat','data');
            if exist('data','var')&&isfield(data,'R')&&isfield(data,'plotY')&&isfield(data,'plotX')
                r=data.R;
                y=data.plotY;
                x=data.plotX;

                saveParams(filePath,r,x,y,data.mode);
            end
        end
    end
end
cd ..
end

function saveParams(filePath,r,x,y,mode)

%Get positive peak
[pos,fwhm,maxY]=getPeak(x,y);
num=ceil(numel(x)/1000);
[pos2,fwhm2]=getPeak(x,movmean(y,num));
if (abs(pos-pos2)>min([fwhm,fwhm2]))||max([fwhm,fwhm2])/min([fwhm,fwhm2])>10
    %disp('Not found')
    pos=0;
    fwhm=0;
    maxY=0;
end

MaxVpos = maxY;
FWHMpos = fwhm;
tpos = pos;

%Get negative peak
[pos,fwhm,maxY]=getPeak(x,-y);
num=ceil(numel(x)/1000);
[pos2,fwhm2]=getPeak(x,movmean(-y,num));
if isempty(fwhm)||isempty(fwhm2)||(abs(pos-pos2)>min([fwhm,fwhm2]))||max([fwhm,fwhm2])/min([fwhm,fwhm2])>10||pos/max(x)>0.8
    %disp('Not found')
    pos=0;
    fwhm=0;
    maxY=0;
end

MaxVneg = maxY;
FWHMneg = fwhm;
tneg = pos;

switch mode
    case 'V - t with R'
        MAXpower=max([MaxVneg,MaxVpos]).^2/r;
    case 'I - t with R'
        MAXpower=max([MaxVneg,MaxVpos]).^2*r;
    otherwise
        MAXpower=0;
end

try
    data = importdata(filePath);
    R = data.data(:,1);
    MaxVPOS = data.data(:,2);
    MaxVNEG = data.data(:,3);
    MaxPOWER = data.data(:,4);
    FWHMPOS = data.data(:,5);
    FWHMNEG = data.data(:,6);
    tPOS = data.data(:,7);
    tNEG = data.data(:,8);
catch e
    R = [];
    MaxVPOS = [];
    MaxVNEG = [];
    MaxPOWER = [];
    FWHMPOS = [];
    FWHMNEG = [];
    tPOS = [];
    tNEG = [];
end
R(end+1) = r;
MaxVPOS(end+1) = MaxVpos;
MaxVNEG(end+1) = MaxVneg;
MaxPOWER(end+1) = MAXpower;
FWHMPOS(end+1) = FWHMpos;
FWHMNEG(end+1) = FWHMneg;
tPOS(end+1) = tpos;
tNEG(end+1) = tneg;

[R,i] = sort(R);
MaxVPOS = MaxVPOS(i);
MaxVNEG = MaxVNEG(i);
MaxPOWER = MaxPOWER(i);
FWHMPOS = FWHMPOS(i);
FWHMNEG = FWHMNEG(i);
tPOS = tPOS(i);
tNEG = tNEG(i);

fid = fopen(filePath,'w');
fprintf(fid,'R(Ohm)  MaxV+(V) MaxV-(V)  MaxPower(W) FWHM+(s) FWHM-(s) t+(s) t-(s)\n');
for n=1:numel(R)
    fprintf(fid,'%e  %e  %e  %e  %e  %e  %e  %e\n',R(n), MaxVPOS(n), MaxVNEG(n), MaxPOWER(n), FWHMPOS(n), FWHMNEG(n), tPOS(n), tNEG(n));
end
fclose(fid);
end

function [pos,fwhm,M]=getPeak(x,y)
[M,I]=max(y);
pos=x(I(1));
halfMaxValue = M / 2; % Find the half max value.
% Find indexes of power where the power first and last is above the half max value.
leftIndex = find(y >= halfMaxValue, 1, 'first');
rightIndex = find(y >= halfMaxValue, 1, 'last');
% Compute the delta time value by using those indexes in the time vector.
fwhm = x(rightIndex) - x(leftIndex);

% figure
% plot(x,y)
% hold on
% plot(pos,M,'kx')
% area(x(leftIndex:rightIndex),y(leftIndex:rightIndex));

end