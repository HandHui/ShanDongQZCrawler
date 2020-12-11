import re
import json

def saveToFile(filename,con):

    with open(filename,'w+',encoding='utf-8') as fout:
        json.dump(con,fout,ensure_ascii=False,indent=4)

        
def getFromFile(filename):
    with open(filename,'r',encoding='utf-8') as fin:
        res = json.load(fin)
    return res

def S_search(pat,text):
    t = re.search(pat,text,re.S)
    if t == None:
        text1 = ''
    else:
        text1 = t.groups()[0]
    return text1