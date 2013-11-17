"""Module contains functions for investigating the structures of saved decision trees"""

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


def printTree(savedTree):
    """Function prints the attributes split on and their respective gain for each
    depth in the tree. DOES NOT PRINT LEAFS

    savedTree = file location of tree to be loaded"""

    tree = pickle.load(open(savedTree,'rb'))
    d = 1
    #Do first node outside while loop
    thisLevel = tree
    nextLevel = list()
    print('Height', d, ':\n')
    print(tree.featureID, ':', tree.gain)
    if tree.left:
        if not tree.left.isLeaf:
            nextLevel.append(tree.left)
    if tree.right:
        if not tree.right.isLeaf:
            nextLevel.append(tree.right)
    print
    thisLevel = nextLevel
    d = 2

    #Do rest of tree in while loop
    while thisLevel:
        nextLevel = list()
        print('Height', d, ':\n')
        for n in thisLevel:
            print(n.featureID, ':', n.gain)
            if n.left:
                if not n.left.isLeaf:
                    nextLevel.append(n.left)
            if n.right:
                if not n.right.isLeaf:
                    nextLevel.append(n.right)
        print('\n')
        thisLevel = nextLevel
        d = d + 1        



sT = 'C:/Users/Sam/Documents/Cornell University/Fall 12 Semester/CS 4780/Final Project/iPhone Data/Results/12.10 iid all/savedTree.txt'
printTree(sT)
