clear all
close all
clc

%%
%data=TDTbin2mat('G:\Shared drives\Schwartz\Data\MATLAB\FED3-test\FED3-TEST-210209-165119');

%% Editable parts!

tankdir='G:\Shared drives\Schwartz\Data\Fiber Photometry Experiments\Faber DMH Project\Circadian HFHS Presentation';

n = 8; %how many blocks are you extracting?

% edit accordingly, where do you want your data and figure(s) saved?
savedata='G:\Shared drives\Schwartz\Data\Fiber Photometry Experiments\Faber DMH Project\Circadian HFHS Presentation\Data';
savefigs='G:\Shared drives\Schwartz\Data\Fiber Photometry Experiments\Faber DMH Project\Circadian HFHS Presentation\Figures';

%% Create cell arrays and pre-allocate space for your specific files - don't touch this!

filename1 = cell(1,n);
filename2 = cell(1,n);
filename1(:) = {'empty'};
filename2(:) = {'empty'};

%% Condition 1: ZT7, ad lib, HFHS

filename1{1} = 'ZT7-DMH3-HFHS'; % name/identifier of mouse and expt on cable 1
%filename2{1} = ''; %cable 2
blockname1{1} = 'DMH-3-201108-123527';

filename1{2} = 'ZT7-DMH4-HFHS'; % name/identifier of mouse and expt on cable 1
%filename2{2} = ''; %cable 2
blockname1{2} = 'DMH-4-201108-132008';

filename1{3} = 'ZT7-DMH6-HFHS'; % name/identifier of mouse and expt on cable 1
%filename2{3} = ''; %cable 2
blockname1{3} = 'DMH-6-201108-140804';

filename1{4} = 'ZT7-DMH7-HFHS'; % name/identifier of mouse and expt on cable 1
%filename2{4} = ''; %cable 2
blockname1{4} = 'DMH-7-201108-153449';

%% Condition 2: ZT14, ad lib, HFHS

filename1{5} = 'ZT14-DMH3-HFHS'; % name/identifier of mouse and expt on cable 1
%filename2{5} = ''; %cable 2
blockname1{5} = 'DMH-3-201110-201611';

filename1{6} = 'ZT14-DMH4-HFHS'; % name/identifier of mouse and expt on cable 1
%filename2{6} = ''; %cable 2
blockname1{6} = 'DMH-4-201110-210026';

filename1{7} = 'ZT14-DMH6-HFHS'; % name/identifier of mouse and expt on cable 1
%filename2{7} = ''; %cable 2
blockname1{7} = 'DMH-6-201110-214402';

filename1{8} = 'ZT14-DMH7-HFHS'; % name/identifier of mouse and expt on cable 1
%filename2{8} = ''; %cable 2
blockname1{8} = 'DMH-7-201110-222751';


%% Loop it!
for nn = [ 1:n ] 

Extract_Batch_CF(savedata,savefigs,blockname1{nn},tankdir,filename1{nn},filename2{nn})

end

%% One big word document for any errors that occurred in looping through the function. 
