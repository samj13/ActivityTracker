"""Module trains a C4.5 decision tree and then tests for accuracy, trims depth, repeats

The learning task is to classify activities based on measurements such as:
-Heartbeat
-Accelorometer
-Magnometer
There are 18 activities to be classified, specified by the integers in the following array:
activities = [1,2,3,4,5,6,7,9,10,11,12,13,16,17,18,19,20,24]
There are skipping activities because that is what the data set we were working had.
The tree splits on real valued attributes which are time domain analyses of the measurements.
"""

import pickle
import re
import math
import time
import sys


def testAll(tree, points):
    """Recursively tests tree against known activity labels"""
    incorrect=sum(mismatchesPerAct(tree, points))
    return incorrect/len(points)

def testLoc(tree, points, activity):
    """Returns accuracy for specific activity"""
    return mismatchesPerAct(tree,points)[activity]/tree.activityCounts[activity]

def mismatchesPerAct(tree, points):
    """Calculates how many misclassifications the tree made for a certain activity"""
    mismatched=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #18 activities
    activities = [1,2,3,4,5,6,7,9,10,11,12,13,16,17,18,19,20,24]
    for point in points:
        if point[0] != recursetest(tree, point):
            mismatched[activities.index(point[0])]=mismatched[activities.index(point[0])]+1
    return mismatched

def recursetest(tree, point):
    """Helper function for finding the classification of an example"""
    if(tree.isLeaf):
        return tree.activity
    else:
        if (point[tree.featureID] < tree.featureVal):
            return recursetest(tree.left,point)
        else:
            return recursetest(tree.right,point)

def pruneTree(tree, d):
    """Prunes decision tree to certain depth d"""
    return pruneRecurse(tree, d, 0)

def pruneRecurse(node, d, depth):
    """Helper function for pruning tree"""
    activities = [1,2,3,4,5,6,7,9,10,11,12,13,16,17,18,19,20,24]
    if not(node.isLeaf):
        if (depth >= d):
            node.loc = activities[node.activityCounts.index(max(node.activityCounts))]
            node.isLeaf = True
        else:
            pruneRecurse(node.left, d, 1 + depth)
            pruneRecurse(node.right, d, 1 + depth)


class DecisionTree:

    def __init__(self):
        """Initialize the data members"""
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


def makeTree(points, curNode, maxDepth, gainCutOff, gainPast):
    """Function for creating a decision tree for activity clasification

    points - the current points needing to be classified at the current node
    curNode - the current node
    maxDepth - the maximum specified depth for the decision tree
    gainCutOff - the minimum information gain needed for creating a split
    gainPast - information gain of parent node, used to prevent infinite
               recursion for a few corner cases
    """
    
    activities = [1,2,3,4,5,6,7,9,10,11,12,13,16,17,18,19,20,24]
    #Create activity counts
    activityCounts = []
    for activity in activities:
        activityCounts.append([ex[0] for ex in points].count(activity))

    maxGain = 0
    maxFeature = 0
    #Loop over each feature, 140 features as of right now-------------------------------------------
    for i in range(1,141):

        #Sort points in accordance to the feature being looked at
        sortedPoints = sorted(points, key=lambda att:att[i])
        pointsL = len(sortedPoints)
                  
        #Loop over each point in sortedPoints by index
        for j in range(0,pointsL):

            split=sortedPoints[j][i]
            #Calculate Entropy Below Split
            percentBelow = j/pointsL
            belowCounts = []
            for activity in activities:
                belowCounts.append([ex[0] for ex in sortedPoints[0:j]].count(activity))
            gain1 = percentBelow*(eHelper(belowCounts,j))

            #Calculate Entropy Above Split which includes those points that do not have feature                       
            percentAbove = (pointsL-j)/pointsL
            aboveCounts = [c - bc for c, bc in zip(activityCounts, belowCounts)]
            gain2 = percentAbove * (eHelper(aboveCounts, pointsL-j))

            #Calculate Information Gain, math.log(pointsL,2) will be the maximum entropy
            gain = math.log(pointsL,2) - gain1 - gain2 
           
            #Determine if this is better than the current max
            if gain>=maxGain:
                maxGain = gain
                maxSplit = split
                maxFeature = i
    #---------------------------------------------------------------------------------------------

    #Check if it should be a leaf - CRITERIA - all the same activity, too deep, less than gainCutOff
    if sum(1 for i in activityCounts if i) < 2 or maxGain < gainCutOff or maxGain==gainPast or depth(curNode)>=maxDepth:
        curNode.makeLeaf(activities[activityCounts.index(max(activityCounts))], activityCounts)
        #Return to parent
        return curNode
    
    curNode.update(maxFeature, maxSplit, activityCounts,maxGain)
    #Make new array with all points less than split on the maxFeature
    leftPoints = pointMaker(points, maxSplit, maxFeature, True)
    #Make new array with all points greater than split on the maxFeature or not containing maxFeature
    rightPoints = pointMaker(points, maxSplit, maxFeature, False)

    #For convention, left node are less than the split and right nodes are greater or not containing
    #Make left node
    leftNode = DecisionTree()
    curNode.left = leftNode
    leftNode.parent = curNode
    #Make right node
    rightNode = DecisionTree()
    curNode.right = rightNode
    rightNode.parent = curNode

    gainPast = maxGain
    #Recursiveley makeTree for left
    makeTree(leftPoints, leftNode, maxDepth, gainCutOff, gainPast)
    #Recursiveley makeTree for right
    makeTree(rightPoints, rightNode, maxDepth, gainCutOff, gainPast)	
    return curNode


def eHelper(aC, total):
    """Function calculates entropy given activity counts and total count"""
    s = 0.0
    for y in aC:
        if (y>0):
            #print s,y,total
            hwl=float(y)/float(total)
            #print hwl
            s=s-hwl*(math.log(hwl,2))
    return s

def pointMaker(points, split, featureID, left):
    """Extracts the examples in points that are to the specified side of the split"""
    newPoints = []
    for x in points:
        if (left):   
                if x[featureID] < split:
                    newPoints.append(x)
        else:
                if x[featureID] >= split:
                    newPoints.append(x)
    return newPoints

def height(node): 
    """Calculates height of decision tree given root originally"""
    if node.isLeaf:
        return 0
    else:
        return max(height(node.left), height(node.right)) + 1

def depth(node):
    """Calculates the depth of a given node"""
    if node.parent == None:
        return 0
    else:
        return depth(node.parent) + 1
                              

"""Train and test-----------------------------------------------------------------------------"""
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


t = time.time()
maxDepthGlobal = 40
gainCutOffGlobal = .001                              

print('Max Specified Depth:',maxDepthGlobal)
tree = makeTree(trainpoints,DecisionTree(),maxDepthGlobal, gainCutOffGlobal,0)
#Save tree
pickle.dump(tree, open('savedTreeA.txt','wb'))
print('Train Time:',time.time()-t)

print('train accuracy:',1-testAll(tree, trainpoints))

print('the overall accuracy with full depth', height(tree),'no pruning is: ', 1-testAll(tree, testpoints))

pruneTree(tree,math.ceil(height(tree)*.8))
print('the overall accuracy with depth',math.ceil(height(tree)*.8), 'is:', 1-testAll(tree, testpoints))
pruneTree(tree,math.ceil(height(tree)*.8))
print('the overall accuracy with depth',math.ceil(height(tree)*.6), 'is:', 1-testAll(tree, testpoints))
pruneTree(tree,math.ceil(height(tree)*.8))
print('the overall accuracy with depth',math.ceil(height(tree)*.4), 'is:', 1-testAll(tree, testpoints))
pruneTree(tree,math.ceil(height(tree)*.8))
print('the overall accuracy with depth',math.ceil(height(tree)*.2), 'is:', 1-testAll(tree, testpoints))





