function dataTextWriterOverlap(outName, workDir)
%Function merges the features of all .mat files in the directory and does
%time domain analysis to create the final features. The features are put
%into svm ready format specified by [activity featureID:featureval...]
%Assume each file only has one activity

fid=fopen([workDir outName],'w');
%Initialize line_store
line_store = [];
a=1;
    
dataFiles = dir([workDir, '\*.mat']);
%For each .mat file in the directory
for i = 1:length(dataFiles)
    data = load([workDir dataFiles(i).name]);
    features = data.newFeatures;
    activity = data.activity;
    

    %Assume 100Hz collection rate, get 5s windows, this may be different
    %for each iPhone, be aware. As long as the same number of readings are
    %being read I don't think it is critical
    for j = 1:40:length(features)-199
        win_data = features(j:j+199,:);
        line = time(win_data);
        line_store(a,:)=[str2num(activity) line];
        a = a + 1;
    end
    
end

%Normalize Features
for j=2:size(line_store,2)
    fmean=mean(line_store(:,j));
    fstd=std(line_store(:,j));
    line_store(:,j)=(line_store(:,j)-fmean)/fstd;
end

%WRITE EXAMPLE TO SVM FILE
for j=1:size(line_store,1)
    svmWriter(line_store(j,:),fid);
end

fclose(fid);

end




%takes an array and calcualtes mean, standard deviation, absolute integral,
%and energy
%outputs this into an array

function out = time(ar)
    [h,w]=size(ar);
    analysis=zeros(5,w);
    analysis(1,:)=mean(ar,1);
    analysis(2,:)=std(ar,0,1);
    analysis(3,:)=sum(abs(ar),1);%absolute integral
    analysis(4,:)=sum(ar.^2,1);
    analysis(5,:)=max(ar,[],1);%we can decide if this is what we want
    %analysis(6,:)=%frequency analysis stuff will use up time
    
    out=[analysis(1,:) analysis(2,:) analysis(3,:) analysis(4,:) analysis(5,:)];
end%Write to txt file


%Function writes to a text file specified by fid in the following format
%[activityID subjectID features----->], line is an array with this same
%format
%
%Assume ID's and features are numbers
%
%The file fid must be opened and closed out of this program

function svmWriter(line, fid)
    %Make lineString
    lineString = num2str(line(1));
    for i = 2:length(line)
        if (isnan(line(i)) || isinf(line(i)))
            continue
        end
        lineString = [lineString,' ', num2str(i-1), ':', num2str(line(i))];
    end
        
    %Write line to file
    fprintf(fid, '%s\n%', lineString);  
end