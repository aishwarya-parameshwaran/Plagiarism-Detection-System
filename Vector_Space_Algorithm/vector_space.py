import codecs
import glob
import math
import os
from collections import Counter
import time
import sys
import xml.etree.ElementTree as et
import nltk
from nltk.stem import WordNetLemmatizer

'''Metadata to compare to in order to train the model
and set a suitable threshold for the data'''
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


def get_token_count_from_file(file_path):
    wordnet_lemmatizer = WordNetLemmatizer()
    try:
        with codecs.open(file_path, 'r') as current_file:
            data = current_file.read().decode('unicode_escape').encode('ascii', 'ignore')
    except Exception as e:
        return {}

    tokens_from_file = nltk.word_tokenize(data)
    tagged_tokens = nltk.pos_tag(tokens_from_file)
    all_tokens = []
    for each_token in tagged_tokens:
        if each_token[1][0] == 'V':
            word = wordnet_lemmatizer.lemmatize(each_token[0], pos="v")
            word = word.lower()
            all_tokens.append(word)
        elif each_token[1] == 'NNP' or each_token[1] == 'NNPS':
            all_tokens.append(each_token[0])
        elif not each_token[1].isalpha():
            continue
        else:
            all_tokens.append(each_token[0].lower())

    all_tokens = nltk.ngrams(all_tokens, 3)
    token_count = dict(Counter(all_tokens))

    return token_count


def create_model(path_to_folder):
    os.chdir(path_to_folder)
    model_data = {}
    for each_file in glob.glob("*.txt"):
        full_path = path_to_folder + '/' + each_file
        token_count = get_token_count_from_file(full_path)
        model_data[each_file] = token_count

    return model_data


'''Creating a model with tf-idf values as term weights instead of term frequencies to
combine tf-idf with cosine similarity

number_of_docs: total number of documents in the model
t_count: for each token, count of documents where the token occurs
generic_model: initially contains token counts for each token in the documents
idf_value: computed value of inverse document frequency
tf_idf_value: computed value of tf-idf weight for each token'''

def create_model_tf_idf(path_to_folder):
    generic_model = create_model(path_to_folder)
    number_of_docs = len(generic_model)
    for each_file in generic_model:
        for each_token in generic_model[each_file]:
            t_count = 0
            for each_other_file in generic_model:
                if each_token in generic_model[each_other_file]:
                    t_count += 1

            idf_value = math.log10(number_of_docs) - math.log10(t_count)
            tf_idf_value = generic_model[each_file][each_token] * idf_value
            generic_model[each_file][each_token] = tf_idf_value

    return generic_model


def dot_product(model_data, document_1, document_2):
    sum_of_products = 0
    for each_token in model_data[document_1]:
        if each_token in model_data[document_2]:
            sum_of_products += (model_data[document_1][each_token] * model_data[document_2][each_token])

    return sum_of_products


def cosine_value(dot_product_value, model_data, document_1, document_2):
    document_1_mod = 0
    for each_token in model_data[document_1]:
        document_1_mod += (model_data[document_1][each_token] ** 2)

    document_1_mod = math.sqrt(document_1_mod)

    document_2_mod = 0
    for each_token in model_data[document_2]:
        document_2_mod += (model_data[document_2][each_token] ** 2)

    document_2_mod = math.sqrt(document_2_mod)
    try:
        cosine_distance_value = dot_product_value / (document_1_mod * document_2_mod)
    except ZeroDivisionError, z:
        return 0
    return cosine_distance_value


def vector_model_matrix(model_source_data, model_suspicious_data):

    vector_model = {}
    model_data = model_source_data.copy()
    model_data.update(model_suspicious_data)
    for each_doc in model_suspicious_data:
        for each_other_doc in model_source_data:
            if each_doc != each_other_doc:
                if each_doc in vector_model and each_other_doc in vector_model[each_doc]:
                    continue
                dot_product_value = dot_product(model_data, each_doc, each_other_doc)
                cosine_distance = cosine_value(dot_product_value, model_data, each_doc, each_other_doc)

                if each_doc not in vector_model:
                    vector_model[each_doc] = {}
                vector_model[each_doc][each_other_doc] = cosine_distance

            if each_doc == each_other_doc:
                if each_doc not in vector_model:
                    vector_model[each_doc] = {}
                vector_model[each_doc][each_other_doc] = 0

    return vector_model


def get_trained_threshold(source_directory, test_directory):
    plagiarism_md = get_plagiarism_metadata(test_directory)
    sum_of_cosine_values = 0
    training_model = {}

    for each_file in plagiarism_md:
        if len(plagiarism_md[each_file]) == 0:
            continue
        test_file_tokenized = get_token_count_from_file(test_directory+'/'+each_file)
        training_model[each_file] = test_file_tokenized
        plagiarised_from = list(plagiarism_md[each_file])
        average_cosine_values = 0
        count_files = 0
        for each_source_file in plagiarised_from:
            source_file_tokenized = get_token_count_from_file(source_directory+'/'+each_source_file)
            if each_source_file not in training_model:

                training_model[each_source_file] = source_file_tokenized
                dot_product_val = dot_product(training_model,each_file,each_source_file)
                cosine_distance = cosine_value(dot_product_val,training_model,each_file,each_source_file)
                average_cosine_values += cosine_distance
                count_files += 1
        sum_of_cosine_values += average_cosine_values/float(count_files)

    trained_threshold = sum_of_cosine_values/len(plagiarism_md)
    return trained_threshold


def get_plagiarism_status(vector_model, threshold):
    plagiarized = []
    for each_suspicious_file in vector_model:
        maximum_key = max(vector_model[each_suspicious_file], key=vector_model[each_suspicious_file].get)
        max_cosine_score = vector_model[each_suspicious_file][maximum_key]
        if max_cosine_score >= threshold:
            plagiarized.append(each_suspicious_file)
    return plagiarized


if __name__ == '__main__':
    start_time = time.time()
    train_suspicious = sys.argv[1]
    train_source = sys.argv[2]
    test_suspicious = sys.argv[3]
    test_source = sys.argv[4]
    algorithm = sys.argv[5]
    threshold = get_trained_threshold(train_source,train_suspicious)
    if algorithm == 'tf':
        source_model = create_model(test_source)
        print "Source model created"
        test_model = create_model(test_suspicious)
        print "Test model created"
    elif algorithm == 'tfidf':
        source_model = create_model_tf_idf(test_source)
        print "Source model created"
        test_model = create_model_tf_idf(test_suspicious)
        print "Test model created"
    vector_model = vector_model_matrix(source_model, test_model)
    print "Vector model matrix created"
    plagiarized_docs = get_plagiarism_status(vector_model, threshold)
    actual_plagiarized_md = get_plagiarism_metadata(test_suspicious)
    print "Plagiarism Metadata obtained"
    actual_plagiarized = []
    for each_doc in actual_plagiarized_md:
        if len(actual_plagiarized_md[each_doc]) != 0:
            actual_plagiarized.append(each_doc)
    print "-------------------------------------------------------------"
    print "List of all documents classifies as plagiarized"
    print plagiarized_docs
    print "-------------------------------------------------------------"
    print "Comparing"
    print "List of correctly classified docs as plagiarized"
    correctly_classified = list(set(plagiarized_docs) & set(actual_plagiarized))
    print correctly_classified
    print "-------------------------------------------------------------"

    print "Precision"
    print len(correctly_classified)/float(len(plagiarized_docs))

    print "Mission accomplished!"
    print "-------------"+str(time.time()-start_time)+"----------------"
