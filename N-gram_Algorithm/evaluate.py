import sys
import ast
import os

result = sys.argv[1]
f1 = open(result, 'r')

check = sys.argv[2]
print check
read_contents = open(check, "r")
data = ast.literal_eval(read_contents.read())

correctly_classified_files = 0
count_documents = 0

for line in f1:
    count_documents += 1
    words = line.split()
    if len(words) > 1:
        if "Not" in words:
            continue
        else:
            filename = words[0]
            file_name = os.path.basename(filename)
            print file_name
            if data[file_name] == True:
                correctly_classified_files+=1

print correctly_classified_files
print count_documents
precision = correctly_classified_files / float(count_documents)

