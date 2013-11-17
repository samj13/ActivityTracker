function [cMatAA, cMatAI, cMatII] = makeCMat(actualLabels, treeLabels, actualLabelsI, treeLabelsI)

cMatAA=zeros(24,25);
cMatAI=zeros(24,4);
cMatII=zeros(3,4);
for i =1:length(actualLabels)
    cMatAA(actualLabels(i),treeLabels(i))=cMatAA(actualLabels(i),treeLabels(i))+1;
    if actualLabels(i) ~= treeLabels(i)
        cMatAA(actualLabels(i),25)=cMatAA(actualLabels(i),25)+1;
    end
    cMatAI(actualLabels(i),treeLabelsI(i))=cMatAI(actualLabels(i),treeLabelsI(i))+1;
    if actualLabelsI(i) ~= treeLabelsI(i)
        cMatAI(actualLabels(i),4)=cMatAI(actualLabels(i),4)+1;
        cMatII(actualLabelsI(i),4)=cMatII(actualLabelsI(i),4) + 1;
    end
    cMatII(actualLabelsI(i),treeLabelsI(i))=cMatII(actualLabelsI(i),treeLabelsI(i))+1;
    
end

for i = 1:24
    if cMatAA(i,25)~=0
        cMatAA(i,25)=100*(1-cMatAA(i,25)/sum(cMatAA(i,1:24)));
    end
    if cMatAI(i,4)~=0
        cMatAI(i,4)=100*(1-cMatAI(i,4)/sum(cMatAI(i,1:3)));
    end
end

for i = 1:3
    
    if cMatII(i,4)~=0
        cMatII(i,4)=100*(1-cMatII(i,4)/sum(cMatII(i,1:3)));
    end
end
