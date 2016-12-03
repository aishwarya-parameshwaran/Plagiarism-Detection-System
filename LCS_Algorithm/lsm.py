import nltk
import sys
import os
import time
start_time=time.time()

# sys.setrecursionlimit(3000)

def LSM(tokens1, tokens2):
    global elemCount
    global A
    global B
    if len(tokens1) <= len(tokens2):
        A = tokens1
        B = tokens2
        m = len(tokens1)
        n = len(tokens2)
    else:
        A = tokens2
        B = tokens1
        m = len(tokens2)
        n = len(tokens1)
    print ("m and n are:" + str(m) + "," + str(n))

    global lsm
    lsm = [[9999 for x in range(0, n + 1)] for y in range(0, m + 1)]

    for i in range(0, m + 1):
        lsm[i][0] = i
    for j in range(1, n + 1):
        lsm[0][j] = max(0, (j - n + m))
    #here R is for columns
    k, R = 0, 0
    while lsm[m][n] is 9999:
        l = -1
        r = -1
        for p in range(0, m + 1):
            if lsm[p][R] == k:
                if l == -1:
                    l = p
                    r = p
                else:
                    r = p
        for c in range(l, r + 1):
            try:
				if (R+1)<=n and (c+1)<=m and (c+1)>=0:
					if lsm[c + 1][R+1]==9999:
						lsm[c + 1][R+1] = computeLsmValue(c + 1, R+1)

            except Exception as e2:
                print ("Exception2: "+str(e2)+"; values of R and c is" + str(R) + " and " + str(c))
                print ("m and n are:" + str(m) + "," + str(n))
                break;

        foundK = False

        if R<n:
            for p in range(0, m + 1):
                if lsm[p][R+1] == k:
                    R = R + 1
                    foundK = True
                    break
        if foundK == False:
            R = 0
            k = k + 1


    lcs_m_n = m - lsm[m][n]
    return lcs_m_n

def computeLsmValue(a, b):
    worda = A[a - 1]

    wordb = B[b - 1]
    if b == 0:
        lsm[a][b] = a
    elif a == 0:
        m = len(lsm) - 1
        n = len(lsm[0]) - 1
        lsm[a][b] = max(0, (b - n + m))
    elif worda == wordb:
        lsm[a][b] = lsm[a - 1][b - 1]
    else:
        m = len(lsm) - 1
        n = len(lsm[0]) - 1
        X = (m - a) - (n - b)

        if X < 0:
            lsm[a][b] = min(lsm[a][b - 1],lsm[a - 1][b] + 1)
        if X == 0:
            lsm[a][b] = min(lsm[a][b - 1],lsm[a - 1][b])
        if X > 0:
            lsm[a][b] = min(lsm[a][b - 1] + 1,lsm[a - 1][b])
    if lsm[a][b] is None or lsm[a][b] is 9999:
        print ("value being returned from compute lsm for a->"+str(a)+" and b->"+str(b)+" is "+str(lsm[a][b]))
        print ("values were: lsm[a][b - 1]= "+str(lsm[a][b - 1])+", lsm[a - 1][b]="+str(lsm[a - 1][b]))
    return lsm[a][b]


def getLSMvalue(i, j):
    if lsm[i][j] is not 9999:
        return lsm[i][j]
    else:
        return computeLsmValue(i, j)


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


def main():

    filepath1 = sys.argv[1]
    filepath2 = sys.argv[2]
    fileopen1 = open(filepath1, 'r')
    content1 = unicode(fileopen1.read(), errors='ignore')
    fileopen1.close()
    fileopen2 = open(filepath2, 'r')
    content2 = unicode(fileopen2.read(), errors='ignore')
    fileopen2.close()
    list1 = nltk.word_tokenize(content1)
    list2 = nltk.word_tokenize(content2)
    lcs_val = LSM(list1, list2)
    print ("lcs val is:" + str(lcs_val))
    print("---------------time taken for execution: %s seconds-------------------------------" % (time.time() - start_time))

main()
