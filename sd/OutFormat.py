
class OutFormat:

    def __init__(self):
        self.content = {}
        
        self.content['子事项信息'] = SubItem()
    
    def handleItem(self,region,rawdict):
        item = Item()
        item.handleCon(region,rawdict)
        self.content['事项信息'] = item.con
    
class Item:

    def __init__(self):
        self.con = {}
    
    def handleCon(self,region,rawdict):
        
        ## 基本编码 / 行使层级
        # print(rawdict)
        rawdict = rawdict['基本信息']
        self.con['事项名称'] = rawdict.get('权责事项名称','')
        self.con['事项类别'] = rawdict.get('事项类型','')
        self.con['实施主体'] = rawdict.get('实施主体','')
        self.con['实施依据'] = rawdict.get('设定、行使依据及有关条款','')
        self.con['所属地区'] = region
        self.con['备注'] = ''
        # print(self.con)

class SubItem:
    def __init__(self):
        self.con = {}

if __name__ == '__main__':
    from util import *
    details = getFromFile('../SDQZdata/pagedetail_sd.json')
    detail = details[0]
    print(detail)
    out = OutFormat()
    out.handleItem('山东省',detail)
    print(out.content['事项信息'])

