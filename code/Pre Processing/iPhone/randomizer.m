function randomizer(dataFile, newdataFile)
%Takes in SVM_light ready and shuffles all the examples
fid = fopen(dataFile);
myd = textscan(fid, '%s', 'Delimiter', '\n');
fclose(fid);
myperm = randperm(length(myd{1}));
mynewd = myd{:}(myperm);

fidnew = fopen(newdataFile,'w');
for i = 1:length(mynewd)
    fprintf(fidnew, '%s\n', mynewd{i});
end
fclose(fidnew);