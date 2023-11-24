import json
from operator import itemgetter
import sys, getopt


def LoadJobDescription(filePath):
    try:
        fh = open(filePath, "r")
        jdData = fh.read()
        jdData = jdData.lower()
        replacements = [",", ".", "'s", "\r", "\n", "\t"]
        for r in replacements:
            jdData = jdData.replace(r, "")
        jdData = jdData.replace("  ", " ")
        return jdData.split()
    finally:
        fh.close()

def LoadRequiredKeywordsDictionary(filePath):
    try:
        fh = open(filePath, "r")
        data = fh.read()
        data = data.lower()
        return json.loads(data)
    finally:
        fh.close()
         
def GetRequiredKeywordsMatch(splitedJs, keywords):
    m = {}

    for word in splitedJs:
        if word in keywords:
            if word in m:
                m[word] = m[word] + 1
            else:
                m[word] = 1
    return dict(sorted(m.items(), key=lambda x: x[1], reverse=True))



def main(argv):
    jobDescriptionFile = ""
    keywordsFile = ""
    resultFile = ""
    try:
        opts, args = getopt.getopt(argv,"",["jobDescriptionFile=","keywordsFile=", "resultFile="])
    except getopt.GetoptError:
        print ('keywordsFinder.py --jobDescriptionFile <jobDescriptionFilePath> --keywordsFile <keywordsFilePath> --resultFile <resultFilePath>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('keywordsFinder.py --jobDescriptionFile <jobDescriptionFilePath> --keywordsFile <keywordsFilePath> --resultFile <resultFilePath>')
            sys.exit()
        elif opt in ("--jobDescriptionFile"):
            jobDescriptionFile = arg
        elif opt in ("--keywordsFile"):
            keywordsFile = arg
        elif opt in ("--resultFile"):
            resultFile = arg
    splitedJs = LoadJobDescription(jobDescriptionFile)
    keywords = LoadRequiredKeywordsDictionary(keywordsFile)


    with open(resultFile, 'w') as fp:
        json.dump(GetRequiredKeywordsMatch(splitedJs, keywords), fp)

if __name__ == "__main__":
    main(sys.argv[1:])
