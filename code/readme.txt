This readme gives a quick description of the layout of this folder and the files in it.


Decision Tree	
	
	iPhone Results - 	This folder contains the saved decision trees and results from all decision
				tree learning.
	
	PMAP2 Results -	This folder contains the saved decision trees and results from all
			decision tree learning.

	activityC45.py -	Script for PMAP2 data activity classification.

	activityC45Intensity.py -	Script for PMAP2 data intensity classification.

	activityC45IntensityiPhone.py -	Script for iPhone data activity classification.

	dtInvestigate.py -	Script for printing out decision tree.

	treeTestTrim.py -	Script for investigating pruning effects on activity classification.

	treeTestTrimI.py - 	Script for investigating pruning effects on intensity classification.


LDA 
	LDA.py -	Module that has all functions related to the LDA algorithm.

Other 

	makeCMat.m -	Function for making confusion matricies.

	McNemar.py -	Script for running McNemar's test.

Pre Processing	

	iPhone
		
		dataTextWriter.m -	iPhone feature extraction using non overlapping windows.

		dataTextWriterOverlap.m -	iPhone feature extraction using overlapping windows.

		featureCreator.m -	Parses raw data and creates .mat files for any given record of data.

		randomizer.m -	Shuffles SVMlight ready files

	PMAP2
		
		parse_input.m - creates SVMlight ready data files from the raw data from UCI repository.

SVM
	
	svmClassifier.py - Module that contains all functions related to the SVM algorithm. Uses SVMlight.
		SVMlight can be found here: http://svmlight.joachims.org/