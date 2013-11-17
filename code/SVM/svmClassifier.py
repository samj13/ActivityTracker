import os
import glob
C=[.0001, .001, .01, .1, 1, 5, 10,50,75,100,200,500,1000]
labels=[2,3,4]
output=[]
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def valSet(examples):
    val_size=file_len(examples)*.3
    f=open(examples,'r')
    val=open('validationSet.train','w')
    valtrain=open('valtrain.train','w')
    i=0
    for line in f:
        if i<val_size:
            val.write(line)
        else:
            valtrain.write(line)
        i=i+1

#def replace_target(oldfile):
#    """Method replaces all classes other than target with -1. Target with 1."""
#    f=open(oldfile,'r')
#    fs=[]
#    numLabels=len(labels)
#    print(numLabels)
#    for label in labels:
#        fs.append(open('bin'+str(label)+'.train','w'))
#    for line in f:
#        l=line.split()[0]
#        for i in range(numLabels):
#            print(labels[i])
#            print(l)
#            if (l[0]==labels[i]): l[0]='1'
#            else: l[0]='-1'
#            fs[i].write(" ".join(l))
#            fs[i].write("\n")
#    for fl in fs:
#        fl.close()
#    f.close()
    

    
def replace_target(oldfile,newfile,target):
    """Method replaces all classes other than target with -1. Target with 1."""
    f=open(oldfile,'r')
    f2=open(newfile,'w')
    for line in f:
        l=line.split()
        if (l[0]==str(target)): l[0]='1'
        else: l[0]='-1'
        f2.write(" ".join(l))
        f2.write("\n")
    f.close()
    f2.close()
    

def replaceAll(oldfile):
    for label in labels:
        replace_target(oldfile,'bin'+str(label)+'.train',label)
    
    
"""This line is used to build the 1 vs all files"""
#replaceAll('validationSet.train')





def trainer():
   
    # Errors for different C value
    for CVal in C:
        
        for label in labels:
            
            #Train
            os.system('svm_learn.exe -c ' + str(CVal) + ' bin' + str(label) + '.train ' + 'svm' + str(label) +'c'+str(CVal)+ '.svm_model')
            #Validate
            
            
            """
            #Create a List Of True Classifications for Validation Set
            valData = open('t'+str(x) + '.train','r')
            lines = valData.readlines()
            trueClass = []
            for line in lines:
                trueClass.append(line[0:2])

            #Open Predictions
            predictData = open('prediction','r')
            predicts = predictData.readlines()

            #Count the number of erros
            for i in range(len(trueClass)):
                if (trueClass[i]=='+1' and predicts[i][0]=='-') or (trueClass[i]=='-1' and predicts[i][0]!='-'):
                    numErrors=numErrors+1

            print(CVal)
            print(x)
            print(numErrors)
            
        errors.append(numErrors)
        
    minCidx = errors.index(min(errors))
    print(C[minCidx])
"""
#trainer()



def validate():
    f=open('validationSet.train','r')
    numExamples=file_len('validationSet.train')
    classification=[]
    maxVals=[]
    errors=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    accuracy=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    testData=f.readlines()
    Cindex=0
    for i in range(numExamples):
        classification.append(0)
    for CVal in C:
        maxVals[:]=[]
        for i in range(numExamples):
            maxVals.append(0)
        for label in labels:
            print(os.system('svm_classify.exe ' + 'validationSet.train svm' +str(label)+'c'+str(CVal)+'.svm_model ' + 'prediction'+str(label)+'c'+str(CVal)+'.txt'))
            #Create a List Of True Classifications for Validation Set
            fpredicts=open('prediction'+str(label)+'c'+str(CVal)+'.txt')
            answers=fpredicts.readlines()
            for i in range(numExamples):
                if (maxVals[i] < float(answers[i])):
                    maxVals[i]=float(answers[i])
                    classification[i]=label
        for i in range(numExamples):
            if(classification[i]!=float(testData[i].split()[0])):
                errors[Cindex]=errors[Cindex]+1
        errors[Cindex]=errors[Cindex]/numExamples
        accuracy[Cindex]=1.0-errors[Cindex]
        Cindex=Cindex+1
        
        
        
    print(errors)
    print("accuracy: ",end="")
    print(accuracy)
    
    
def test(testset,CVal):
    f=open(testset,'r')
    numExamples=file_len(testset)
    classification=[]
    maxVals=[]
    for i in range(numExamples):
        classification.append(0)
        maxVals.append(0)
    error=0
    testData=f.readlines()
    print(testData[4])
    for label in labels:
        print(os.system('svm_classify.exe ' + testset+' svm' +str(label)+'c'+str(CVal)+'.svm_model ' + 'prediction'+str(label)+'c'+str(CVal)+'.txt'))
        #Create a List Of True Classifications for Validation Set
        fpredicts=open('prediction'+str(label)+'c'+str(CVal)+'.txt')
        answers=fpredicts.readlines()
        for i in range(numExamples):
            if (maxVals[i] < float(answers[i])):
                maxVals[i]=float(answers[i])
                classification[i]=label
    for i in range(numExamples):
        if(classification[i]!=float(testData[i].split()[0])):
            error=error+1
    error=error/numExamples
    accuracy=1.0-error
    f1=open(testset + '_labeledbySVM','w')
    for clas in classification:
        f1.write(str(clas)+"\n")
    f1.close()
        
    print(error)
    print("accuracy: ",end="")
    print(accuracy)
    output.append(accuracy)
    
#THE PROCESS    
    
valSet('AkshayiPhoneData66.train')
replaceAll('validationSet.train')
trainer()
validate()
test('AkshayiPhoneData33.test',500)
valSet('NickiPhoneData66.train')
replaceAll('validationSet.train')
trainer()
validate()
test('NickiPhoneData33.test',500)
valSet('SamiPhoneData66.train')
replaceAll('validationSet.train')
trainer()
validate()
test('SamiPhoneData33.test',500)
valSet('iPhoneData66.train')
replaceAll('validationSet.train')
trainer()
validate()
test('iPhoneData33.test',500)
valSet('AkshayiPhoneDataO66.train')
replaceAll('validationSet.train')
trainer()
validate()
test('AkshayiPhoneDataO33.test',50)
valSet('NickiPhoneDataO66.train')
replaceAll('validationSet.train')
trainer()
validate()
test('NickiPhoneDataO33.test',500)
valSet('SamiPhoneDataO66.train')
replaceAll('validationSet.train')
trainer()
validate()
test('SamiPhoneDataO33.test',500)
valSet('iPhoneDataO66.train')
replaceAll('validationSet.train')
trainer()
validate()
test('iPhoneDataO33.test',500)
print(output)












#            lines = valData.readlines()
#            trueClass = []
#            for line in lines:
#                trueClass.append(line[0:2])
#
#            #Open Predictions
#            predictData = open('prediction','r')
#            predicts = predictData.readlines()
#
#            #Count the number of erros
#            for i in range(len(trueClass)):
#                if (trueClass[i]=='+1' and predicts[i][0]=='-') or (trueClass[i]=='-1' and predicts[i][0]!='-'):
#                    numErrors=numErrors+1
#
#            print(CVal)
#            
#            print(numErrors)
#            
#        errors.append(numErrors)
        
#   minCidx = errors.index(min(errors))
#   print(C[minCidx])



#
#""" Function for performing testing with the optimal C value found in trainer as specified by HW4P2A"""
#def tester():
#    bestC = 1
#    falsePos = 0
#    falseNeg = 0
#    print('hello')
#
#    #Train
#    os.system('svm_learn -c ' + str(bestC) + ' webspam_train.svm model')
#    #Test
#    os.system('svm_classify webspam_test.svm model predicts')
#
#    #Create a List Of True Classifications for Test Set
#    valData = open('webspam_test.svm','r')
#    lines = valData.readlines()
#    trueClass = []
#    for line in lines:
#        trueClass.append(line[0:2])
#
#    #Open Predictions
#    predictData = open('predicts','r')
#    predicts = predictData.readlines()
#
#    #Count the number of erros
#    for i in range(len(trueClass)):
#        if (trueClass[i]=='+1' and predicts[i][0]=='-'):
#            falseNeg = falseNeg + 1
#        elif (trueClass[i]=='-1' and predicts[i][0]!='-'):
#            falsePos = falsePos + 1
#
#    numErrors = falseNeg + falsePos
#
#    accuracy = 1-numErrors/len(predicts)
#
#    print(accuracy)
#    print(falseNeg)
#    print(falsePos)