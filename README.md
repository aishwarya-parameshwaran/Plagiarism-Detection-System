# Plagiarism-Detection-System

##N-Gram Overlap Algorithm

The goal of this algorithm is to find whether a document has been plagiarised or not. The main motivation behind using n-gram overlap approach is that comparing n-grams is much faster and efficient rather than single word matching.

Usage:

For executing the algorithm,

Command : ngram_algorithm.py source_document_directory suspicious_train suspicious_test

2 output files are generated, output.txt and suspicious_reference.txt

For evaluating the results,

Command : evaluate.py output.txt suspicious_reference.txt

##Longest Common Subsequence Algorithm

This subfolder has codes that implement LCS to find whether a document has been plagiarised or not. Also includes modified LCS approach named 'Lost Score Matrix'
Usage:

For executing the generic LCS algorithm,

Command : lcs.py snipped_source_directory_path snipped_suspicious_directory_path

The code divides suspicious documents directory content for training and testing. A source-map mapping each training file to corresponding source documents that it is copied from is pre-defined.
All the suspicious documents not in the map are considered for testing. The output is the name of testing files along with the decision label (i.e. Plagiarized or Not Plagiarized)

For executing the LSM version of algorithm,

Command : lsm.py source_file.txt suspicious_file.txt

This is an alternative to LCS implementation. This mainly demonstrates the time taken for execution is different depending upon the LCS value. Takes path to two text documents as input. 
Outputs/Prints the LCS value and the time taken for execution in the console.

For executing the snipDoc script,

Command : snipDoc.py source_directory_path

This script is used to shorten the length of text files during preprocessing for training and testing purpose. Takes the path to directory containing files to be shortened. Changes made to the same copy of files permanently.

