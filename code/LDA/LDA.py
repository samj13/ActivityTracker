def LDA(work_dir):
    """Run Linear Discriminant Analysis on PAMAP Dataset in work_dir (string path)."""
    import re
    import math
    import numpy as np
    import operator

    train_path=work_dir+"\PAMAP1120.train"
    test_path=work_dir+"\PAMAP1120.test"
    nfeatures=140

    #get class means
    act=[1,2,3,4,5,6,7,12,13,16,17,24]
    u,nex={j:{(i+1):0 for i in range(nfeatures)} for j in act},{j:0 for j in act}
    f=open(train_path)
    for line in f:
        x=re.split(': | |:',line.strip())
        a=int(x[0])
        nex[a]+=1
        for i in range(1,len(x),2):
            u[a][int(x[i])]+=float(x[i+1])

    f.close()
    #divide through to get class means
    tot=0
    for i in act:
        for j in u[i]:
            u[i][j]/=nex[i]
        tot+=nex[i]

    #prior probabilities
    prior={j:0 for j in act}
    for i in act:
        prior[i]=nex[i]/tot

    #classify test examples
    f=open(test_path)
    err,tot=0,0
    truth,pred=[],[]
    for line in f:
        x=re.split(': | |:',line.strip())
        a=int(x[0])
        
        #Compute max across activities
        h={j:0 for j in act}
        for y in act:
            #prior probability for activity y
            h[y]+=math.log(prior[y],math.exp(1))
            new_x={(j+1):0 for j in range(nfeatures)}
            mult_x=[]
            #get feature vector for instance
            for i in range(1,len(x),2):
                new_x[int(x[i])]+=float(x[i+1])
            #calculate difference from mean for activity y
            for i in new_x:
                mult_x.append(new_x[i]-u[y][i])
            #include dot product of difference
            h[y]-=0.5*np.dot(mult_x,mult_x)

        #predict as max h
        p=max(h.items(), key=operator.itemgetter(1))[0]
        if (p!=a): err+=1
        truth.append(a)
        pred.append(p)
        tot+=1
    f.close()
    
    return err,tot,truth,pred

work_dir="C:\\Users\dhawan\Documents\CS 5870\Project"
out=LDA(work_dir)











                
            
