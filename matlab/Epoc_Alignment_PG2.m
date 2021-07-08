%% Goals: input smoothed and aligned data from script 1 in order to evaluate
%signal changes surrounding epocs

%revise to add outputs for group averaging
%revise with if/then statements indicating where to look for TTL epocs if
%manual times are not provided.

function [] = Epoc_Alignment_CF(savedata, savefigs,matdata,epocs,wind)
%% Clear workspace
clearvars -except savedata savefigs matdata epocs wind;
close all;

%% Load dFF and time variables from Extract_Batch_CF.m

loaded_data = load(data);
dff = loaded_data.dFF;

loaded_time = load('/Volumes/GoogleDrive/Shared drives/Schwartz/Data/MATLAB/PG exported variables/downtime.mat');
time = loaded_time.downtime;

%% Do not edit this

%CF needs to make sure that these will be saved properly with each animal
%if two are recorded at once.

%Also need to figure out how to deal with looking at all behaviors - needs
%to be looped separately? 
if epocs == 'manual'
    epocs = cell(1,n);
    epocs(:) = {'empty'};
else if epocs == 'leftpoke'
        epocs = cell(1,n);
        epocs = 'epoc.Left.onset';
    else if epocs == 'rightpoke'
            epocs = cell(1,n);
            epocs = 'epoc.Right.onset';
        else if epocs == 'pellet'
                epocs = cell(1,n);
                epocs = 'epoc.Pelt.onset';
            end
        end
    end
end
%% Turn Licking Events into Lick Bouts

% Priority #1: Plot all epocs together -(dff/time trace of entire
% experiment) - save figures

% Priority #2: Plot heat map of individual epocs per animal, also in trace
% format - may need to change if number of epocs gets really high - save
% figures

%% heat map (x dim: time, ydim: event, zdim: deltaF/F)
% figure(sess+300)
% 
% hold on
% imagesc(linspace(-timewindow,timewindow,length(photoPerLick)),1:size(LickTrig,1),LickTrig)
% L = line([0 0],[0 length(licks)+1]);
% set(L,'Color','black')
% xlabel('Peri-Event Time (sec)')
% ylabel('Bout Number')
% cb = colorbar;
% title(cb,'Z score')
% caxis([-1.5 1.5])
% colormap(flipud(brewermap([],'YlGnBu')))
% xlim([-timewindow timewindow])
% ylim([0 length(licks)+1])
% hold off

%print

%%
% Priority #3: Plot heat map of average response to epoc, plot average
% trace with SEM - save figures

% Priority #4: Save a .csv and .mat into folder specified in batch script, save figures of heat maps, traces. 

% tasks for later: 
% Area under the curve, above the curve

% Peak - max dF/F after an epoc


%% Manual epocs
% Manually extract time around each epoc - need to modify because manual
% timepoints will be added in input script.
events = [100; 140; 230; 500; 560; 600; 760; 900];
before = events-20;
after = events+20;
x = reshape(kron([before, after], [1, 1])', [], 1);
size = length(events);
d = ones(1,size); % 8
y = reshape([zeros(1, size); d; d; zeros(1, size)], 1, []);

y_scale = 10; % adjust according to data needs
y_shift = -20; % scale and shift are just for aesthetics

% Individual epocs are each size(x) / size = 4
%% Manual plot
figure('Position',[100, 100, 800, 400]);
p1 = plot(time, dff); hold on;
p2 = plot(x, y_scale*(y) + y_shift);
hold off;
legend([p1 p2],'GCaMP','Epoc');
axis tight;

% SAVE FIGURE
%% From data stream
% Epocs from data stream
% Make a continuous time series of Licking TTL events (epocs) and plot
LICK_on = data.epocs.(LICK).onset; % array of start times
LICK_off = data.epocs.(LICK).offset; % array of end times
LICK_x = reshape(kron([LICK_on, LICK_off], [1, 1])', [], 1); 
sz = length(LICK_on); % number of events
d2 = data.epocs.(LICK).data'; % vector of 1s (1/4 of events)
y_scale = 10; % adjust according to data needs
y_shift = -20; % scale and shift are just for aesthetics
LICK_y = reshape([zeros(1, sz); d2; d2; zeros(1, sz)], 1, []);

%% Data stream plotting
% First subplot in a series: dFF with lick epocs
figure('Position',[100, 100, 800, 400]);
p1 = plot(time, dff); hold on;
p2 = plot(LICK_x, y_scale*(LICK_y) + y_shift);
hold off; 
title('Detrended, y-shifted dFF','fontsize',16);
legend([p1 p2],'GCaMP','Lick Epoc');
axis tight;

% SAVE FIGURE 
%% Batch processing
import_dff_1 = load();
import_time_1 = load();
dff1 = import_dff_1.dFF1;
time1 = import_time_1.downtime;

import_dff_2 = load();
import_time_2 = load();
dff2 = import_dff_2.dFF1;
time2 = import_time_2.downtime;


