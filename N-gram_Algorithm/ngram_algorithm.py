from __future__ import division
from nltk.tokenize import RegexpTokenizer, sent_tokenize
from nltk import ngrams
import sys
import os
import glob
import xml.etree.ElementTree as et

#Function to extract the feature tag from every suspicious document XML file
def get_plagiarism_metadata(directory_path):
    plagiarism_metadata = {}
    os.chdir(directory_path)
    for each_file in glob.glob("*.xml"):
        full_path = directory_path+'/'+each_file
        txt_each_path = str(each_file.replace('.xml','.txt'))
        plagiarism_metadata[txt_each_path] = set()
        xml_tree = et.parse(full_path)
        root = xml_tree.getroot()
        for each_child in root:
            if each_child.tag == 'feature':
                attributes = each_child.attrib
                plagiarism_metadata[txt_each_path].add(attributes['source_reference'])
    return plagiarism_metadata

#Function to record while of the files are suspicious
def get_suspicious_documents(directory_path):
    sus_docs = {}
    os.chdir(directory_path)
    for each_file in glob.glob("*.xml"):
        full_path = directory_path+'/'+each_file
        txt_each_path = str(each_file.replace('.xml','.txt'))
        xml_tree = et.parse(full_path)
        root = xml_tree.getroot()
        for each_child in root:
            if each_child.tag == 'feature':
                sus_docs[txt_each_path] = True
    return sus_docs

#Function to get the threshold from the training data
def get_trained_threshold(data, source_list, test_directory):
    count_no_files = 0
    file_threshold = 0
    for item in data:
        if len(data[item]) == 0:
            continue
        else:
            plagiarised_from = list(data[item])
            for each_file in plagiarised_from:
                count_no_files += 1
                source_file = source_list + '/' + each_file
                source = open(source_file, 'r')
                suspicious = open(test_directory + '/' + item, 'r')
                containment = ngramAlgorithm(suspicious.read(), source.read())
                file_threshold += containment
        return (file_threshold / count_no_files)

#Function to calculate the n-gram overlap coefficient
def ngramAlgorithm(susp_data, source_data):
    data_f1 = unicode(susp_data, errors='ignore')
    data_f2 = unicode(source_data, errors='ignore')
    sentence_tokenize = sent_tokenize(data_f1)
    tokenizer = RegexpTokenizer(r'\w+')  # use regex to remove punctuations
    words = tokenizer.tokenize(data_f2)
    d_ngrams_list = list(ngrams(words, 3))
    containment = []
    for sentence in sentence_tokenize:
        sentence_words = tokenizer.tokenize(sentence)
        si_ngrams_list = list(ngrams(sentence_words, 3))
        if len(si_ngrams_list) == 0:
            continue
        value = list(set(si_ngrams_list) & set(d_ngrams_list))
        final_value = len(value)/(len(si_ngrams_list))
        containment.append(final_value)

    containment_sum = 0

    for c in containment:
        containment_sum += c

    containment_avg = containment_sum/len(sentence_tokenize)
    print containment_avg
    return containment_avg

#main function
def start():
    source_directory = sys.argv[1]
    source_file_list = {}
    for filename in os.listdir(source_directory):
        if filename.endswith(".txt"):
            file_name = os.path.join(source_directory, filename)
            f1 = open(file_name, 'r')
            content = f1.read()
            source_file_list[file_name] = content

    print len(source_file_list)

    suspicious_directory_train = sys.argv[2]
    suspicious_directory_test = sys.argv[3]
    suspicious = sys.argv[4]
    plag_metadata = get_plagiarism_metadata(suspicious_directory_train)
    suspicious_documents = get_suspicious_documents(suspicious)
    model = open("/home/champ/Documents/Plagiarism/reference.txt", "w+")
    print len(suspicious_documents)
    model.write(str(suspicious_documents))

    file_threshold = get_trained_threshold(plag_metadata, source_directory, suspicious_directory_train)
    print file_threshold

    suspicious_file_list = {}
    for filename in os.listdir(suspicious_directory_test):
        if filename.endswith(".txt"):
            file_name = os.path.join(suspicious_directory_test, filename)
            f2 = open(file_name, 'r')
            content = f2.read()
            suspicious_file_list[file_name] = content

    print len(suspicious_file_list)

    list_dict = {}

    for fileName in suspicious_file_list:
        max_result = 0
        for source_file in source_file_list:
            result = ngramAlgorithm(suspicious_file_list[fileName], source_file_list[source_file])
            if max_result < result:
                max_result = result
        list_dict[fileName] = max_result
        print max_result

    for fileName in list_dict:
        print fileName + " " + str(list_dict[fileName])

    output = open("/home/champ/Documents/Plagiarism/output.txt", "w+")
    for fileName in list_dict:
        if list_dict[fileName] >= file_threshold:
            output.write(fileName + " " + "Plagiarised" + "\n")
        else:
            output.write(fileName + " " + "Not Plagiarised" + "\n")

start()
