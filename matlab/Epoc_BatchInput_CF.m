clear all
close all
clc
%% Editable parts:

% Specify the folder where the files live.
myFolder = '/Volumes/GoogleDrive/Shared drives/Schwartz/Data/Fiber Photometry Experiments/Faber DMH Project/Circadian Chow Presentation/Data';

%Manual or TTL epocs? Type 'manual' 'FED3' or 'other'
epocs = 'manual';

%Time window around each epoc?
wind = 60;

% Where do you want to save your data and alignment figures?
% savedata='';
% savefigs='';

%% Checks to make sure that folder actually exists.  Warn user if it doesn't.
if ~isfolder(myFolder)
    errorMessage = sprintf('Error: The following folder does not exist:\n%s\nPlease specify a new folder.', myFolder);
    uiwait(warndlg(errorMessage));
    myFolder = uigetdir(); % Ask for a new one.
    if myFolder == 0
         % User clicked Cancel
         return;
    end
end

% Get a list of all files in the folder with the desired file name pattern.
filePattern = fullfile(myFolder, '*.mat'); % Change to whatever pattern you need.
theFiles = dir(filePattern);
n = length(theFiles);
matdata = cell(1,n); %create an empty cell array to be filled with full file name to run through loop


for k = 1 : n
    baseFileName = theFiles(k).name;
    fullFileName = fullfile(theFiles(k).folder, baseFileName);
    matdata{k} = fullFileName;    
end


%% This needs work - trying to make it easy for manual epocs to be incorporated with dffs

% if epocs == 'manual'
%     manepocs = cell(1,n);
%     prompt = '';
%     
% else if epocs == 'FED3'
%         prompt = 'Which epocs do you want to analyze? Left, Right, Pellet, or All? \n'
%         epocs = input(prompt,'s');
%         %if
%     end
% end

%% Loop through Epoc Alignment function

%need to figure out how to specify output arguments so that we can group
%some processed data together for averaging below. another cell array? 

for nn = [ 1:n ]

Epoc_Alignment_CF(savedata,savefigs,matdata{nn},epocs,wind)

end