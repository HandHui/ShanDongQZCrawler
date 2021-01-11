
class BasicInfo:

    def __init__(self):
        self.con = None
        
    def handleBinfo(self,title,rawinfo,proinfo,sult_plaint,fee,legal):
        sitem = {}
        sitem['事项名称'] = title.get('标题','')
        sitem['基本编码'] = title.get('基本编码','')
        sitem['事项类型'] = rawinfo.get('事项类型','')
        sitem['权力来源'] = rawinfo.get('权力来源','')
        sitem['行使层级'] = rawinfo.get('行使层级','')
        sitem['实施编码'] = title.get('实施编码','')
        sitem['业务办理项编码'] = ''
        sitem['事项状态'] = rawinfo.get("事项状态",'')
        sitem['事项版本'] = rawinfo.get("事项版本",'')
        sitem['实施主体'] = rawinfo.get("实施主体",'')
        sitem['实施主体性质'] = rawinfo.get("实施主体性质",'')
        sitem['委托部门'] = ''

        num_unit = rawinfo.get("法定办结时限（工作日）",'')
        num_unit = num_unit.split(' ')
        if len(num_unit) == 2:
            sitem['法定办结时限'] = num_unit[0] if num_unit[0] != '-' else ''
            sitem['法定办结时限单位'] = num_unit[1]
        else:
            sitem['法定办结时限'] = '-1'       ###办结实现为-1表示该元素点未知
            sitem['法定办结时限单位'] = '工作日'
        sitem['法定办结时限说明'] = ''

        num_unit = rawinfo.get("承诺办结时限（工作日）",'')
        num_unit = num_unit.split(' ')
        if len(num_unit) == 2:
            sitem['承诺办结时限'] = num_unit[0] if num_unit[0] != '-' else ''
            sitem['承诺办结时限单位'] = num_unit[1]
        else:
            sitem['承诺办结时限'] = '-1'       ###办结实现为-1表示该元素点未知
            sitem['承诺办结时限单位'] = '工作日'
        sitem['承诺办结时限说明'] = ''

        sitem['服务对象'] = rawinfo.get("服务对象",'')
        sitem['办件类型'] = rawinfo.get("办件类型",'')
        sitem['办理形式'] = rawinfo.get('办理形式','')
        sitem['到办事现场次数'] = rawinfo.get('到办事现场次数','')
        sitem['特别程度'] = ''
        sitem['办理地点'] = proinfo.get('办理地点','')
        sitem['办理时间'] = proinfo.get('办理时间','')

        consult = sult_plaint.get('咨询方式','')
        sitem['咨询方式'] = str(consult)   ### 转为字符串的方法，一种是json 一种直接str
        complaint = sult_plaint.get("投诉方式",'')
        sitem['监督投诉方式'] = str(complaint)

        sitem['通办范围'] = rawinfo.get("通办范围",'')
        tmp = rawinfo.get("联办机构",'')
        sitem['联办机构'] = tmp if tmp != '-' else ''

        sitem['中介服务'] = ''
        sitem['数量限制'] = ''
        sitem['审批结果类型'] = ''
        sitem['审批结果名称'] = ''
        sitem['审批结果样本'] = ''
        sitem['是否支持预约办理'] = ''

        online_pay = fee.get('是否支持网上支付','')
        sitem['是否支持网上支付'] = online_pay if online_pay != '-' else ''

        sitem['是否支持快递服务'] = rawinfo.get('是否支持物流快递','')
        sitem['是否支持自助终端办理'] = ''
        sitem['是否网办'] = ''
        sitem['必须现场办理原因说明'] = ''
        sitem['适用范围'] = ''
        sitem['是否属于“工改”事项'] = ''
        sitem['业务办理系统名称'] = ''
        

        sitem['行政诉讼途径'] = str(legal.get("行政诉讼",''))    ######dict转str
        sitem['行政复议途径'] = str(legal.get('行政复议',''))

        sitem['是否进驻政务大厅'] = rawinfo.get('是否进驻政务大厅','')

        self.con = sitem


class OutFormat:

    def __init__(self):
        self.content = {}
    
    def handleItem(self,region,rawdict):
        item = Item()
        item.handleCon(region,rawdict)
        self.content['事项信息'] = item.con
    
    def handleSubItem(self,guides):
        self.content['子事项信息'] = []
        for guide in guides:
            # print(guide)
            sitem = SubItem()
            sitem.handleCon(guide)
            self.content['子事项信息'].append(sitem.con)
        
        if self.content['事项信息'] and self.content['子事项信息']:
            if '基本信息' not in self.content['子事项信息'][0]:
                return
            self.content['事项信息']['基本编码'] = self.content['子事项信息'][0]['基本信息']['基本编码']
            self.content['事项信息']['行使层级'] = self.content['子事项信息'][0]['基本信息']['行使层级']

class Item:

    def __init__(self):
        self.con = {}
    
    def handleCon(self,region,rawdict):
        
        ## 基本编码 / 行使层级
        # print(rawdict)
        rawdict = rawdict.get('基本信息','')
        if rawdict == "":
            return 
        self.con['事项名称'] = rawdict.get('权责事项名称','')
        self.con['事项类别'] = rawdict.get('事项类型','')
        self.con['基本编码'] = ''
        self.con['实施主体'] = rawdict.get('实施主体','')
        ## 实施层级及权限
        tmp = rawdict.get('实施层级及权限','')
        tmp = tmp.split('|')
        if len(tmp) == 2:
            self.con['行使层级'] = tmp[0].strip()
        else:
            self.con['行使层级'] = '' 

        self.con['实施依据'] = rawdict.get('设定、行使依据及有关条款','')
        self.con['所属地区'] = region
        self.con['备注'] = ''
        # print(self.con)

class SubItem:
    def __init__(self):
        self.con = {}
    
    def handleCon(self,guide):
        #title,rawinfo,proinfo,sult_plaint,fee,legal
        if '标题信息' not in guide:
            print('No title')
            return
        title = guide["标题信息"]
        rawinfo = guide['基本信息']
        proinfo = guide['办理信息']
        evi = guide['设定依据']
        flow = guide['办理流程']
        legal = guide['法律救济']
        if not legal:
            legal = {}
        cond = guide['受理条件']
        material = guide['材料目录']
        sult_plaint = guide['咨询/投诉方式']
        if '收费信息' in guide:
            fee = guide["收费信息"]
        else:
            fee = {}

        self.handleBasicInfo(title,rawinfo,proinfo,sult_plaint,fee,legal)
        self.handleFlow(flow)
        self.handleMat(material)
        self.handleCond(cond)
        self.hanldeFee(fee)
        self.handleEvi(evi)


    
    def handleFlow(self,flow):
        items = {}
        items['办理流程图'] = flow['流程图url']
        lst = []
        idx = 0
        for step in flow['办理步骤']:
            newstep = {}
            newstep['序号'] = idx
            idx += 1
            newstep['办理流程环节名称'] = step['环节名称']
            newstep['办理流程环节办理时限'] = step['办理时限']
            newstep['办理流程环节审批标准'] = step['审批标准']
            lst.append(newstep)
        items['办理步骤'] = lst
        self.con['办理流程'] = items
    
    def handleMat(self,materials):
        
        idx = 0
        lst = []
        for material in materials:
            newmat = {}
            newmat['序号'] = idx
            idx += 1
            newmat['材料名称'] = material['材料名称']
            newmat['空白表格'] = material['空白表格']
            newmat['来源渠道'] = ''
            newmat['纸质材料份数'] = material['纸质材料份数']
            newmat['材料必要性'] = material['材料必要性']
            newmat['填表须知'] = ''
            newmat['是否已实现数据共享'] = ''
            lst.append(newmat)
        self.con['办理材料'] = lst
    
    def handleCond(self,cond):
        self.con['受理条件'] = cond
    
    def hanldeFee(self,fee):
        item = {}
        item['序号'] = 0
        item['费用名称'] = fee.get('收费项目名称:','')
        item['费用标准'] = fee.get('收费标准:','')
        item['费用说明'] = ""
        self.con['收费情况'] = [item]
    
    def handleEvi(self,evi):
        self.con['设定依据'] = evi

    def handleBasicInfo(self,title,rawinfo,proinfo,sult_plaint,fee,legal):
        sitem = BasicInfo()
        sitem.handleBinfo(title,rawinfo,proinfo,sult_plaint,fee,legal)
        self.con['基本信息'] = sitem.con
        
    


if __name__ == '__main__':
    from util import *
    import os
    details = getFromFile('../SDQZdata/pagedetail_sd.json')
    subpath = '../SDQZdata/sd/'
    subnames = os.listdir(subpath)
    # details = getFromFile('../SDQZdata/sd/58_0.json')
    flag = 0
    # for i in range(len(details)):
    # subindx = 0
    for detail in details:
        # detail = details[i]
        subidx = 0
        prename = detail['idx']
        print(prename)
        guides = []
        while True:
            name = str(prename)+'_'+str(subidx)+'.json'
            if name in subnames:
                flag = 1
                subidx += 1
                guide = getFromFile(subpath+name)
                guides.append(guide)
            else:
                break
        
        out = OutFormat()
        out.handleItem('山东省',detail)
        if flag == 1:
            out.handleSubItem(guides)
        
        saveToFile('../SDQZdata/excel_sd/'+str(prename)+'.json',out.content)



        # out = OutFormat()
        # out.handleSubItem([details])
        # # out.handleItem('山东省',detail)
        # print(out.content['子事项信息'])
        # saveToFile('1.json',out.content['子事项信息'])
        # break

