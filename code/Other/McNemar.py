def McNemar(truth,a0,a1):
    n01,n10=0,0
    n00,n11=0,0

    for x in range(len(truth)):
        if ((truth[x]==a0[x])and(truth[x]!=a1[x])): n10+=1
        elif ((truth[x]==a1[x])and(truth[x]!=a0[x])): n01+=1
        elif ((truth[x]==a0[x])and(truth[x]==a1[x])): n11+=1
        elif ((truth[x]!=a0[x])and(truth[x]!=a1[x])): n00+=1
        
    chi=(abs(n01-n10)-1)**2/(n01+n10)
    return chi,n00,n01,n10,n11
