function [] = Faber_Extract2(savedata,savefigs,blockname1,tankdir,filename1,filename2,trimstart,trimend)    

clearvars -except blockname1 filename1 filename2 savedata savefigs tankdir trimstart trimend;
close all;

warning('off','all')
warning

blockname = blockname1;
tankname = tankdir;

sd=savedata;
sf=savefigs;

%% Extract data 

f=fullfile(tankname,blockname);
data=TDTbin2mat(f);

%% Automatic naming of streams

fields = fieldnames(data.streams);
if length(fields) < 5
            GCAMP1 = fields{1};
             ISOS1 = fields{2};
             num = 1;
else if length(fields) == 5 && (~strcmp(filename1,'empty')&& ~strcmp(filename2,'empty'))
    GCAMP1 = fields{3};
    ISOS1 = fields{4}; 
    GCAMP2 = fields{1}; 
    ISOS2 = fields{2};
    num = 2;
else if length(fields) == 5 && (strcmp(filename1,'empty') && ~strcmp(filename2,'empty'))
        GCAMP1 = fields{1};
        ISOS1 = fields{2};
        num = 1;
    else if length(fields) == 5 && (~strcmp(filename1,'empty') && strcmp(filename2,'empty'))
            GCAMP1 = fields{3};
            ISOS1 = fields{4};
            num = 1;
            end
        end
    end
end

%% Loop each animal's data through the pre-processing steps below: 
n = num;
for p = 1:n
    
filenameTemp{1} = filename1;
filenameTemp{2} = filename2;
filename = filenameTemp{p};

if p == 1
GCAMP = GCAMP1; %GCaMP (calcium-dependent) signal, 470nm wavelength 
ISOS = ISOS1;  %isosbestic control, 405nm wavelength data stream
end

if p == 2
GCAMP =GCAMP2; %name of the 470 store for cable 2
ISOS =ISOS2; %name of the 405 store for cable 2
end

%% Trim

fs=data.streams.(GCAMP).fs;

st=trimstart; % start time - can be changed, 30 default
et=trimend; % end time - can be changed, 30 default

start=st*fs;
stop=et*fs;
time=(1:length(data.streams.(GCAMP).data))/(data.streams.(GCAMP).fs); 

Signal470=data.streams.(GCAMP).data(start:end-stop);
Signal405=data.streams.(ISOS).data(start:end-stop);

trimtime=time(start:end-stop);

%% Downsample
N=fs; % rate of downsampling desired, default value = 1, can be changed

down_GCAMP= arrayfun(@(i)...
    mean(Signal470(i:i+N-1)),...
    1:N:length(Signal470)-N+1);
down_ISOS= arrayfun(@(i)...
    mean(Signal405(i:i+N-1)),...
    1:N:length(Signal405)-N+1);

downtime=trimtime(1:N:end);
downt=downtime(1:length(down_GCAMP));

%% Smooth with a moving mean

smooth_win=10; % window of data smoothing (number of downsampled data points for moving mean)
% smooth_win default = 10
smooth_GCAMP=movmean(down_GCAMP,smooth_win);
smooth_ISOS=movmean(down_ISOS,smooth_win);

%% Fit and calculate dFF

pf='poly1'; % number for polyfit function, usually set at 1
fitdata= fit(smooth_ISOS',smooth_GCAMP',pf,'Robust','on');
fit_ISOS=fitdata(smooth_ISOS)';
dF=smooth_GCAMP-fit_ISOS;
dFF=100*(dF)./fit_ISOS;

%% Graphs showing basic data analysis

figure
subplot(4,1,1)
plot(time,data.streams.(GCAMP).data,'g','LineWidth',1); hold on;
plot(time,data.streams.(ISOS).data,'b','LineWidth',1);
xlabel('Time (s)','FontSize',10);
ylabel('mV','FontSize',10);
legend('GCaMP','Isosbestic', 'AutoUpdate', 'off');
axis tight;
title(['Raw Signals ' (filename)],'FontSize',12);

subplot(4,1,2)
plot(downt,smooth_GCAMP,'g','LineWidth',1); hold on;
plot(downt,smooth_ISOS,'b','LineWidth',1);
plot(downt,fit_ISOS,'color','b','LineWidth',1);
xlabel('Time (s)','FontSize',10);
ylabel('mV','FontSize',10);
legend('processed GCaMP','processed Isosbestic','fit Isosbestic','AutoUpdate', 'off');
axis tight;
title(['Smoothed, Fit and Aligned Signals ' (filename)],'FontSize',12);

subplot(4,1,3)
plot(downt,dF,'color','k','LineWidth',1);
axis tight;
xlabel('Time (s)','FontSize',10);
ylabel('\Delta mV', 'FontSize', 10);
legend('baseline corrected GCaMP','AutoUpdate', 'off');
title(['Subtracted Signal ' (filename)],'FontSize',12);

subplot(4,1,4)
plot(downt,dFF,'g','LineWidth',1);
axis tight;
xlabel('Time (s)','FontSize',10);
ylabel('\Delta F/F (%)', 'FontSize', 10);
title(['\Delta F/F, ' (filename)],'FontSize',12)

sgtitle('Data Processing','FontSize',14)
sname=['Data Processing ' (filename)];
sdat=fullfile(sf,sname);
print(sdat,'-dtiff')

%% Graph of just dFF

figure
plot(downt,dFF,'g','LineWidth',1);
xlim([min(downt) max(downt)]);
ylim([-25 115]);
xlabel('Time (s)','FontSize',10);
ylabel('\Delta F/F (%)', 'FontSize', 10);
title(['\Delta F/F, ' (filename)],'FontSize',14)

pname=['dFF ' (filename)];
sdff=fullfile(sf,pname);
print(sdff,'-dtiff')

%% Saving .mat files with relevant information

%NEED TO MODIFY TO INCLUDE PROCESSED ISOSBESTIC IN .mat!!
%change format of .mat to be one struct with each parameter in it

%Nicole - let me know what you rename this to be! :) 

savename=sprintf('dFFdata_%s.mat',filename);
m=fullfile(sd,savename);
epoc=data.epocs;
save(m,'dFF','downt','epoc')

end

%% would also be nice to save a file with all relevant processing information and any errors/warnings that occurred.

%% Saving .csv files with relevant information (removed for now)
% could use, needs to have notes added in...
% 3 columns as CSV
% dff, time, epoc onsets

% % filename3=sprintf('dFFdata_%s.xlsx',name1);
% % dFFC1=vertcat(dFF1,downt);
% % writematrix(dFFC1',filename3);

% % filename4=sprintf('dFFdata_%s.xlsx',name2);
% % dFFC2=vertcat(dFF2,downt);
% % writematrix(dFFC2',filename4);
