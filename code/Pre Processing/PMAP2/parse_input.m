function parse_input(files,out)
%This script writes a new txt file from one subject file and generates
%attributes for each window of data. The output is in the format of input to SVMlight

%Input - files is a cell array of strings: subject .dat file paths. out is a string: output file path
%Output - none. Writes SVM examples to text file in out

fid=fopen(out,'w');
a=1;
line_store=zeros(20185,141);

for j=1:length(files)
    file=files{j};
    data=load(file);
    %Fill in missing heart rate values
    for i=1:size(data,1)
        if (isnan(data(i,3)))
            if (i==1)
                data(i,3)=data(find(data(:,3)>0,1),3);
                continue;
            end
            data(i,3)=data(i-1,3);
        end
    end
    data=data(data(:,2)~=0,:);  %get rid of transient data
    window=500; %length of window

    for activity = 1:24
        start=find(data(:,2)==activity,1);  %find start of activity
        last=find(data(:,2)==activity,1,'last');    %find end of activity
        if (isempty(start) || isempty(last))
            continue;
        end
        %form overlapping windows where overlap = window/2
        for i = start:window/5:(last-window)
            win_start=i;    %start time for window
            win_end=i+500;  %end time for window
            %array of data for user, rows are variables, columns are instances
            win_data=data(win_start:win_end,[3 5:7 11:16 22:24 28:33 39:41 45:50])'; 

            %TIME ANALYSIS FUNCTION
            line=time(win_data);
            line_store(a,:)=[activity line];
            a=a+1;

%             %WRITE EXAMPLE TO SVM FILE
%             svmWriter(line,fid);
        end
    end
end

%NORMALIZE FEATURES
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

%Function writes to a text file specified by fid in the following format
%[activityID subjectID features----->], line is an array with this same
%format
%
%Assume ID's and features are numbers
%
%The file fid must be opened and closed out of this program

function svmWriter(line, fid)
    %Make lineString
    lineString = [num2str(line(1))];
    for i = 2:length(line)
        if (isnan(line(i)) || isinf(line(i)))
            continue
        end
        lineString = [lineString,' ', num2str(i-1), ':', num2str(line(i))];
    end
        
    %Write line to file
    fprintf(fid, '%s\n%', lineString);  
end


%takes an array and calcualtes mean, standard deviation, absolute integral,
%and energy
%outputs this into an array

function out = time(ar)
    [h,w]=size(ar);
    analysis=zeros(5,h);
    analysis(1,:)=mean(ar,2);
    analysis(2,:)=std(ar,0,2);
    analysis(3,:)=sum(abs(ar),2);%absolute integral
    analysis(4,:)=sum(ar.^2,2);
    analysis(5,:)=max(ar,[],2);%we can decide if this is what we want
    %analysis(6,:)=%frequency analysis stuff will use up time
    
    out=[analysis(1,:) analysis(2,:) analysis(3,:) analysis(4,:) analysis(5,:)];
end