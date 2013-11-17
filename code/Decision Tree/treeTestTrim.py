"""Module that includes tree pruning and testing functions for CS4780 Activity Monitoring
Final project"""

import re
import pickle


class DecisionTree:

    def __init__(self):
        """Initialized the data members"""
        self.left = None
        self.right = None
        self.featureID = 0
        self.featureVal = 0
        self.activityCounts = []
        self.isEmpty = True
        self.isLeaf = False
        self.activity = 1 #Default
        self.parent = None
        self.gain = 0

    def update(self, featureID, featureVal, activityCounts,gain):
        self.featureID = featureID
        self.featureVal = featureVal
        self.activityCounts = activityCounts
        self.isEmpty = False
        self.gain = gain

    def makeLeaf(self, activity, activityCounts):
        self.isEmpty = False
        self.isLeaf = True
        self.activity = activity
        self.activityCounts = activityCounts



def pruneTreeDepth(tree, d):
    """Prunes tree to specific depth d"""
    return pruneRecurseDepth(tree, d, 0)

def pruneRecurseDepth(node, d, depth):
    """Recurive helper function for pruning to a specific depth"""
    activities = [1,2,3,4,5,6,7,9,10,11,12,13,16,17,18,19,20,24]
    if not(node.isLeaf):
        if (depth >= d):
            node.loc = activities[node.activityCounts.index(max(node.activityCounts))]
            node.isLeaf = True
        else:
            pruneRecurseDepth(node.left, d, 1 + depth)
            pruneRecurseDepth(node.right, d, 1 + depth)

def pruneTreeIG(tree,gCO):
    """Prunes current tree to create leafs that split above the gainCutOff"""
    return pruneRecurseIG(tree, gCO)

def pruneRecurseIG(node, gainCutOff):
    """Recursive helper function for pruning on information gain"""
    activities = [1,2,3,4,5,6,7,9,10,11,12,13,16,17,18,19,20,24]
    if not(node.isLeaf):
        if (node.gain < gainCutOff):
            node.loc = activities[node.activityCounts.index(max(node.activityCounts))]
            node.isLeaf = True
        else:
            pruneRecurseIG(node.left, gainCutOff)
            pruneRecurseIG(node.right, gainCutOff)

def testAll(tree, points):
    """Tests tree on test points"""
    incorrect=sum(mismatchesPerAct(tree, points))
    return incorrect/len(points)

def testLoc(tree, points, act):
    """Tests on certain activity"""
    if tree.activityCounts[act]:
        return mismatchesPerAct(tree,points)[act]/tree.activityCounts[act]
    else:
        return 0
    

def mismatchesPerAct(tree, points):
    """Calculates the number of misclassified examples of a specific activity"""
    mismatched=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #18 activities
    activities = [1,2,3,4,5,6,7,9,10,11,12,13,16,17,18,19,20,24]
    for point in points:
        if point[0] != recursetest(tree, point):
            mismatched[activities.index(point[0])]=mismatched[activities.index(point[0])]+1
    return mismatched

def recursetest(tree, point):
    """Recursive helper function for testing a point"""
    if(tree.isLeaf):
        return tree.activity
    else:
        if (point[tree.featureID] < tree.featureVal):
            return recursetest(tree.left,point)
        else:
            return recursetest(tree.right,point)


def saveClassifications(tree, points):
    """Saves two files, one for the labeles using the tree and one for the actual labels"""
    f = open('treeLabels.txt','w')
    f1 = open('actualLabels.txt','w')
    for point in points:
        f.write(str(recursetest(tree,point)))
        f.write('\n')
        f1.write(str(point[0]))
        f1.write('\n')
    f.close()
    f1.close()

#Testing Script. Load decision tree, and run gainCutOff vs test accuracy
#tests, then output those respective vectors

#Train Mappings
#The data is coming in line by line as specified by [activityID featureID:featureVal....]
train = open('C:/Users/Sam/Documents/Cornell University/Fall 12 Semester/CS 4780/Final Project/PAMAP2_Dataset/PAMAP1207.train')
trainpoints = []
for line in train:
    splits = re.split(':|\s',line)
    tempVec = [float("infinity")]*141 #One index has activityID the other 140 are the features
    tempVec[0]=int(splits.pop(0))
    while(len(splits)>1):   #An unwanted empty string comes at the end of splits
        featureID = int(splits.pop(0))
        featureVal = float(splits.pop(0))
        tempVec[featureID]=featureVal
    trainpoints.append(tempVec)
print('Length of Training Data:',len(trainpoints))

#Test Mappings
#The data is coming in line by line as specified by [activityID featureID:featureVal....]

test = open('C:/Users/Sam/Documents/Cornell University/Fall 12 Semester/CS 4780/Final Project/PAMAP2_Dataset/PAMAP1207.test')
testpoints = []
for line in test:
    splits = re.split(':|\s',line)
    tempVec = [float("infinity")]*141 #One index has activityID the other 140 are the features
    tempVec[0]=int(splits.pop(0))
    while(len(splits)>1):   #An unwanted empty string comes at the end of splits
        featureID = int(splits.pop(0))
        featureVal = float(splits.pop(0))
        tempVec[featureID]=featureVal
    testpoints.append(tempVec)
print('Length of Test Data:',len(testpoints))

#Save classifications
tree = pickle.load(open('C:/Users/Sam/Documents/Cornell University/Fall 12 Semester/CS 4780/Final Project/PAMAP2_Dataset/Results/12.7 88% IGC.001 D34/savedTreeA.txt','rb'))
saveClassifications(tree, testpoints)
                
#Calculate the accuracy while varying gainCutOff on a saved tree
cuts = [.1,.2,.3,.4,.5,.6,.7,.8,.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3]
acc = []
for cut in cuts:
    #Load tree
    tree = pickle.load(open('C:/Users/Sam/Documents/Cornell University/Fall 12 Semester/CS 4780/Final Project/PAMAP2_Dataset/Results/12.7 88% IGC.001 D34/savedTreeA.txt','rb'))
    #Trim on IG
    pruneTreeIG(tree,cut)
    acc.append(1-testAll(tree,testpoints))
print(cuts)
print(acc)

#Calculate the accuracy while varying the maxDepth on a saved tree
depths = [24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1]
acc1 = []
acc1Train = []
for depth in depths:
    #Load tree
    tree = pickle.load(open('C:/Users/Sam/Documents/Cornell University/Fall 12 Semester/CS 4780/Final Project/PAMAP2_Dataset/Results/12.7 88% IGC.001 D34/savedTreeA.txt','rb'))
    #Trim on depth
    pruneTreeDepth(tree,depth)
    acc1.append(1-testAll(tree,testpoints))
    acc1Train.append(1-testAll(tree,trainpoints))
print(depths)
print(acc1)
print(acc1Train)


#Calculate confusion matrix for specific activity
activities = [1,2,3,4,5,6,7,9,10,11,12,13,16,17,18,19,20,24]
tree = pickle.load(open('C:/Users/Sam/Documents/Cornell University/Fall 12 Semester/CS 4780/Final Project/PAMAP2_Dataset/Results/12.7 88% IGC.001 D34/savedTreeA.txt','rb'))
actAc = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
i=0
for act in activities:
    actAc[i]=1-testLoc(tree, testpoints, i)
    i=i+1
print
print(actAc)



