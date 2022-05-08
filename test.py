from sklearn.ensemble import RandomForestClassifier
import numpy as np
import math

class Domain:
    def __init__(self, _name, _label, _length, _num, _entropy, _seg):
        self.name = _name
        self.label = _label
        self.length = _length
        self.num = _num
        self.entropy = _entropy
        self.seg = _seg
    
    def returnData(self):
        return [self.length, self.num, self.entropy, self.seg]
 
    def returnLabel(self):
        if self.label == "dga":
            return 1
        else:
            return 0

def numOFname(str):
    num = 0
    for i in str:
        if i.isdigit():
            num += 1
    return num

def numOFseg(str):
    num = 0
    for i in str:
        if i == '.':
            num += 1
    return num

def calEntropy(str):
    h = 0.0
    sumLetter = 0
    letter = [0] * 26
    str = str.lower()
    for i in range(len(str)):
        if str[i].isalpha():
            letter[ord(str[i]) - ord('a')] += 1
            sumLetter += 1
    for i in range(26):
        p = 1.0 * letter[i] / sumLetter
        if p > 0:
            h += -(p * math.log(p, 2))
    return h

def initData(filename,domainList):
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith("#") or line == "":
                 continue
            tokens = line.split(",")
            name = tokens[0]
            length = len(name)
            if tokens[0] != line:
                label = tokens[1]
            else:
                label = "?"
            num = numOFname(name)
            entropy = calEntropy(name)
            seg = numOFseg(name)
            domainList.append(Domain(name, label, length, num, entropy, seg))

def main():
    domainlist1 = []
    domainlist2 = []
    initData("train.txt",domainlist1)
    featureMatrix = []
    labelList = []
    for item in domainlist1:
         featureMatrix.append(item.returnData())
         labelList.append(item.returnLabel())
    clf = RandomForestClassifier(random_state = 0)
    clf.fit(featureMatrix,labelList)
    initData("test.txt",domainlist2)
    with open("result.txt","w") as f:
        for i in domainlist2:
            f.write(i.name)
            f.write(",")
            if clf.predict([i.returnData()])[0] == 0:
                f.write("notdga\n")
            else:
                f.write("dga\n")
            
if __name__ == '__main__':
    main()

