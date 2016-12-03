import nltk
import sys
import os


def tokenize_file_content(path_to_dir):
    outer_list = []
    for outerdir, innerdirs, files in os.walk(path_to_dir):
        for file in files:
            if file.endswith('.txt'):
                concat = os.path.join(outerdir, file)
                inner_list = []
                content_tokens = []
                inner_list.append(file)
                fileopen = open(concat, 'r')
                content = unicode(fileopen.read(), errors='ignore')
                fileopen.close()
                content_tokens = nltk.word_tokenize(content)
                inner_list.append(content_tokens)
                outer_list.append(inner_list)
    return outer_list


def lcs(X, Y):
    # find the length of the strings
    m = len(X)
    n = len(Y)

    # declaring the array for storing the dp values
    L = [[None] * (n + 1) for i in xrange(m + 1)]

    """Following steps build L[m+1][n+1] in bottom up fashion
    Note: L[i][j] contains length of LCS of X[0..i-1]
    and Y[0..j-1]"""
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])

    # L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
    return L[m][n]


def tokenizeFileContentInDirectory(path_to_dir):
    # returns list of list. One inner list as entry for each file. Each inner list has corresponding filename and a list of tokens of content in that file
    Outer_list = []
    for outerdir, innerdirs, files in os.walk(path_to_dir):
        for file in files:
            if file.endswith('.txt'):
                concat = os.path.join(outerdir, file)
                inner_list = []
                content_tokens = []
                inner_list.append(file)
                fileopen = open(concat, 'r')
                content = unicode(fileopen.read(), errors='ignore')
                fileopen.close()
                content_tokens = nltk.word_tokenize(content)
                inner_list.append(content_tokens)
                Outer_list.append(inner_list)
    return Outer_list


if __name__ == '__main__':

    source_dir_path = sys.argv[1]
    documents_dir_path = sys.argv[2]

    stop_words = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

    source_fw_tokens_list = tokenizeFileContentInDirectory(source_dir_path)
    for each_file_token in source_fw_tokens_list:
        all_tokens = each_file_token[1]
        all_tokens = [x for x in all_tokens if x.lower() not in stop_words]
        each_file_token[1] = all_tokens

    documents_fw_tokens_list = tokenizeFileContentInDirectory(documents_dir_path)
    for each_file_token in documents_fw_tokens_list:
        all_tokens = each_file_token[1]
        all_tokens = [x for x in all_tokens if x.lower() not in stop_words]
        each_file_token[1] = all_tokens
    lcs_values = {}
    for doc in documents_fw_tokens_list:
        lcs_values[doc[0]] = {}
        for src in source_fw_tokens_list:
            lcs_val = lcs(doc[1], src[1])
            lcs_values[doc[0]][src[0]] = lcs_val/float(len(doc[1]))

    source_map = {'suspicious_7.txt': ['source-document00045.txt'],
                  'suspicious_4.txt': ['source-document00047.txt','source-document00086.txt'],
                  'suspicious_3.txt': ['source-document00039.txt','source-document00076.txt'],
                  'suspicious_2.txt': ['source-document00080.txt','source-document00004.txt','source-document00074.txt'],
                  'suspicious_1.txt': ['source-document00001.txt','source-document00053.txt','source-document00075.txt']
                  }

    average_lcs = 0
    count_file = 0
    for each_susp_file in lcs_values:
        if each_susp_file in source_map:
            source_list = source_map[each_susp_file]
            file_avg_lcs = 0
            if len(source_list) != 0:
                count_file += 1
                for each_src in source_list:
                    current_lcs_val = lcs_values[each_susp_file][each_src]
                    file_avg_lcs += current_lcs_val
                file_avg_lcs = file_avg_lcs/float(len(source_list))
            average_lcs += file_avg_lcs

    threshold = average_lcs/float(count_file)
    print "Threshold: "+str(threshold)

    for each_file in lcs_values:
        if each_file not in source_map:
            max_key = max(lcs_values[each_file], key=lcs_values[each_file].get)
            max_lcs = lcs_values[each_file][max_key]
            print each_file+" -- "+str(max_lcs)
            if max_lcs >= threshold:
                print each_file+" => plagiarized"

