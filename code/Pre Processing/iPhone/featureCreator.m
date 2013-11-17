function featureCreator(savedTxt)
%Function takes in a text file made from the data collector app
%and returns a new .mat file that has the respective features
%in a more friendly array format and the stored activity

activity = input('Enter what activity this is for (example format: 4, 3, 2, 1 (Running, Walking, Sitting, Lying respectively): ', 's');
subject = input('Enter the subject (Sam, Nick, Akshay): ', 's');
myD = importdata(savedTxt);
features = myD.data(:,2:4);

%Get rid of altitude data
x = linspace(1,length(features),length(features));
y = x(1:5:end)';
features(y,:)=[];
%Put all features on one line
x = linspace(1,length(features),length(features));
y = x(1:4:end);
newFeatures = zeros(length(y),9);
for i = 1:length(y)
    newFeatures(i,1:9) = [features(i,:) features(i+1,:) features(i+2,:)];
end
    
    
%Figure out duration
startTime = myD.data(1,1);
endTime = myD.data(end,1);
duration = endTime - startTime;
duration = round(duration);

%Save data file
saveString = ['C:\Users\Sam\Documents\Cornell University\Fall 12 Semester\CS 4780\Final Project\iPhone Data\' subject '_' activity '_' num2str(duration) '.mat'];
save(saveString, 'newFeatures', 'activity');