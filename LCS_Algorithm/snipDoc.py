import sys
import os
import nltk


def snipper(path_to_dir):
    for outerdir, innerdirs, files in os.walk(path_to_dir):
        for file in files:
            if file.endswith('.txt'):
                concat = os.path.join(outerdir, file)
                fileopen = open(concat, 'r')
                content = unicode(fileopen.read(), errors='ignore')
                fileopen.close()
                tokenized_content = nltk.word_tokenize(content)
                snipped_tokenized_content = tokenized_content[:3000]
                new_content = ""
                for word in snipped_tokenized_content:
                    new_content = new_content + word + " "
                fileopen = open(concat, 'w')
                fileopen.write(new_content)
                fileopen.close()


def main():
    source_dir_path = sys.argv[1]
    snipper(source_dir_path)


main()
