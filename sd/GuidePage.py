from util import *
from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
from tqdm import tqdm

class TitleInfo:
    def __init__(self):
        self.con = {}
    
    def handle_info(self,text):
        # print(text)

        pat = '<p class="bg-title fl qiehuan".*?>(.*?)</p>'
        btitle = S_search(pat,text)
        self.con['标题'] = btitle

        pat = '<div class="wz fl".*?>(.*?)</div>'
        pos = S_search(pat,text)
        self.con['位置'] = pos

        pat = '<p class="con1-p">.*?<span.*?>(.*?)</span>.*?</p>'
        con1 = re.findall(pat,text,re.S)
        # print(con1)
        if len(con1) == 3:
            self.con['基本编码'] = con1[0]
            self.con['实施编码'] = con1[1]
            self.con['服务部门'] = con1[2]
        # print(self.con)

class BasicInfo:

    def __init__(self):
        self.con = {}
    
    def handle_bi(self,text):
        td_l = re.findall('<td class="td-l">(.*?)</td>',text,re.S)
        td_r = re.findall('<td class="td-r".*?>(.*?)</td>',text,re.S)
        assert len(td_l) == len(td_r)
        for l,r in zip(td_l,td_r):
            ## '-' 表示无信息
            self.con[l] = r
        # print(self.con)

class ConductInfo:

    def __init__(self):
        self.con = {}
    
    def handle_ci(self,text):
        # print(text)
        td_l = re.findall('<td class="td-l">(.*?)</td>',text,re.S)
        td_r = re.findall('<td class="td-r.*?".*?>(.*?)</td>',text,re.S)
        # print(td_l)
        # print(td_r)
        assert len(td_l) == len(td_r)
        for l,r in zip(td_l,td_r):
            ## '-' 表示无信息
            self.con[l] = r
        # print(self.con)

class Accordance:
    
    def __init__(self):
        self.con = []
    
    def handle_acc(self,tag):
        # print(text)
        tbs = tag.find_all(class_='con-l-main')
        for tb in tbs:
            tcon = {}
            tb = str(tb)
            td_l = re.findall('<td class="td-l">(.*?)</td>',tb,re.S)
            td_r = re.findall('<td class="td-r.*?".*?>(.*?)</td>',tb,re.S)
            assert len(td_l) == len(td_r)
            for l,r in zip(td_l,td_r):
                ## '-' 表示无信息
                tcon[l] = extract_url(r)
            self.con.append(tcon)
        # print(self.con)

class Procedure:

    def __init__(self):
        self.con = {}
    
    def handle_pro(self,text):
        # print(text)
        tcon = []
        thead = ['环节名称','办理内容','办理时限','审批标准','办理结果']
        trs = re.findall('<tr>(.*?)</tr>',text,re.S)
        for tr in trs:
            tds = re.findall('<td>(.*?)</td>',tr,re.S)
            if len(tds) % 5 == 0 and len(tds) != 0:
                tcon.append(dict(zip(thead,tds)))
        self.con['办理步骤'] = tcon
        
        turl = S_search('<a href="(.*?)" id="more".*?>.*?</a>',text)
        self.con['流程图url'] = turl
        # print(self.con)

class Remedy:

    def __init__(self):
        self.con = {}
    
    def handle_title_con(self,tag):
        title = tag.find_all(class_='fljj-tit')
        if len(title) == 0:
            title = ""
        else:
            title = str(title[0])
            title = re.sub('<.*?>',"",title)
        
        cons = tag.find_all(class_='fljj-con')
        if len(cons) == 0:
            return title.strip(),{}
        else:
            cons = str(cons[0])
            ps = re.findall('<p>(.*?)</p>',cons,re.S)
            tmp = {}
            for p in ps:
                p = p.split('：',1)
                if len(p) == 2:
                    tmp[p[0]] = p[1]
                else:
                    print(p)
                    tmp[p[0]] = ""
            
            return title.strip(),tmp

    def handle_rem(self,tag):
        leg_tags = tag.find_all(class_="fljj fl")
        if len(leg_tags) == 0:
            self.con = None
            return
        title,discu = self.handle_title_con(leg_tags[0])
        self.con[title] = discu
        if len(leg_tags) > 1:
            title,discu = self.handle_title_con(leg_tags[1])
            self.con[title] = discu
        # print(self.con)

class Condition:
    def __init__(self):
        self.con = ""
    
    def handle_cond(self,text):
        txt1 = S_search('<div class="con2-p">(.*?)</div>',text)
        txt1 = re.sub('<.*?>','',txt1)
        self.con = txt1.strip()
        # return txt1.strip()
        # print(txt1.strip())


class Material:

    def __init__(self):

        self.con =[]
    
    def handle_table(self,text):
        ### 得到空白样表、示例样表的name与url
        ### if 存在url与名字 return 名字(url)
        ### else return ""
        text = text.strip()
        # print(text)
        pat = r'<a href="http://www.shandong.gov.cn/WebDiskServerDemo/doc\?doc_id=(.*?)".*?>'
        res = S_search(pat,text)
        # print(res)
        if res == "":
            return ""
        else:
            pat = r'<a href="(.*?)".*?>(.*?)</a>'
            url_name = re.search(pat,text,re.S)
            if url_name:
                url_name = url_name.groups()
                url = url_name[0].strip()
                name = url_name[1].strip()
                return name+'('+url+')'
            else:
                return ""

    def handleCon(self,text):
        thead = S_search('<thead>(.*?)</thead>',text)
        h_tds = re.findall('<td.*?>(.*?)</td>',thead,re.S)
        # print(h_tds)
        # print('*******')
        tbody = S_search('<tbody>(.*?)</tbody>',text)
        b_tds = re.findall('<td.*?>(.*?)</td>',tbody,re.S)
        # print(b_tds)
        if len(b_tds)%len(h_tds) != 0:
            # print(len(b_tds),len(h_tds))
            return
        else:
            # print("余数为0")
            for i in range(0,len(b_tds),len(h_tds)):
                tm = {}
                for j in range(len(h_tds)):
                    # tm[h_tds[j]] = b_tds[i+j]
                    
                    if S_search('<a.*?>(.*?)</a>',b_tds[i+j]) != "":
                        tm[h_tds[j]] = self.handle_table(b_tds[i+j])
                    else:
                        tm[h_tds[j]] = b_tds[i+j]
                self.con.append(tm)
    
    def handle_len(self):
        ### 处理示例样本与空白样本数量
        sample,blank = 0,0
        for con in self.con:
            tb = 1 if con['空白表格'] != "" else 0 
            blank += tb
            ts = 1 if con['示例样表'] != "" else 0 
            sample += ts
        
        return sample,blank

class QA:
    def __init__(self):
        self.con = []
    
    def handle_qa(self,text):
        text = S_search('<ul>(.*?)</ul>',text)
        lis = re.findall('<li>(.*?)</li>',text,re.S)
        for li in lis:
            ind = S_search('<i class="shuzu">(.*?)</i>',li)
            q = S_search('<p>(.*?)</p>',li)
            a = S_search('<span>(.*?)</span>',li)
            self.con.append((ind,q,a))
            # print(ind,q,a)

# http://www.shandong.gov.cn/api-gateway/jpaas-jiq-web-sdywtb/front/transition/ywTransToDetail?innerCode=1865
class CC:
    def __init__(self):
        self.con = {}
    
    def handle_cc(self,text):
        titles = re.findall('<p class="con2-l-tit">(.*?)</p>',text,re.S)
        con2 = re.findall('<div class="con2-r-main">(.*?)</div>',text,re.S)
        for i in range(len(con2)):
        # for con in con2:
            con = con2[i]
            tmp = {}
            ps = re.findall('<p>(.*?)</p>',con,re.S)
            for p in ps:
                # print(p)
                mets = re.search('<span class="f-bold">(.*?)</span>(.*)',p,re.S)
                if mets:
                    mets = mets.groups()
                    # print(mets)
                    tmp[mets[0]] = mets[1].strip()
            self.con[titles[i]] = tmp
        # print(self.con)

class Fee:

    def __init__(self):
        self.con = {}
    
    def handle_fee(self,text):
        con2 = S_search('<div class="con2-r-main">(.*?)</div>',text)
        ps = re.findall('<p>(.*?)</p>',con2,re.S)
        for p in ps:
            fs = re.search('<strong>(.*?)</strong>(.*)',p,re.S)
            if fs:
                fs = fs.groups()
                self.con[fs[0]] = fs[1].strip()
        # print(self.con)

            


class GuidePage:

    def __init__(self,pid,idx,url,browser,flag=0):

        self.url = url
        self.flag = flag
        self.browser = browser
        self.browser.get(url)
        time.sleep(1)

        self.content = {}
        self.content['pid'] = pid
        self.content['idx'] = idx
        self.content['url'] = url
        # print(url)

    def handle_con(self):
        text = self.browser.page_source
        soup = BeautifulSoup(text,'lxml')

        ## title信息
        text_ti = soup.find_all(class_='fixed-box')
        if len(text_ti) == 0:
            print('No Title Information')
        else:
            text_ti = str(text_ti[0])
            ti = TitleInfo()
            ti.handle_info(text_ti)
            self.content['标题信息'] = ti.con

        ## 基本信息
        text_bi = soup.find_all(id='md1')
        if len(text_bi) == 0:
            print("No Basic INfo")
        else:
            text_bi = str(text_bi[0])
            binfo = BasicInfo()
            binfo.handle_bi(text_bi)
            self.content['基本信息'] = binfo.con
        
        ## 办理信息
        text_ci = soup.find_all(id = 'md2')
        if len(text_ci) == 0:
            print("No Conduct INfo")
        else:
            text_ci = str(text_ci[0])
            cinfo = ConductInfo()
            cinfo.handle_ci(text_ci)
            self.content['办理信息'] = cinfo.con
        
        ## 设定依据
        text_ac = soup.find_all(id = 'md3')
        if len(text_ac) == 0:
            print("No accordance")
        else:
            text_ac = text_ac[0]
            acc = Accordance()
            acc.handle_acc(text_ac)
            self.content['设定依据'] = acc.con

        ## 办理流程
        textp = soup.find_all(id='md4')
        if len(textp) == 0:
            print("No Procedure")
        else:
            textp = str(textp[0])
            prod = Procedure()
            prod.handle_pro(textp)
            self.content['办理流程'] = prod.con
            
        ## 法律救济
        textl = soup.find_all(id="md5")
        if len(textl) == 0:
            print("No Legal Remedy")
        else:
            textl = textl[0]
            rem = Remedy()
            rem.handle_rem(textl)
            self.content['法律救济'] = rem.con
        
        ## 受理条件
        textc = soup.find_all(id="md6")
        if len(textc) == 0:
            print("No Condition")
        else:
            textc = str(textc[0])
            cond = Condition()
            cond.handle_cond(textc)
            self.content['受理条件'] = cond.con


        ## 材料目录
        text_mat = soup.find_all(id='md7')
        if len(text_mat) == 0:
            print('No Material!!')
            # return
        else:
            text_mat = str(text_mat[0])
            mat = Material()
            mat.handleCon(text_mat)
            self.content['材料目录'] = mat.con
            if self.flag == 1:
                return mat.handle_len()
            # print(mat.con)
                
        ## 常见问题
        textq = soup.find_all(class_='con-r-list2 pt2')
        if len(textq) == 0:
            print('No QA')
        else:
            textq = str(textq[0])
            qa = QA()
            qa.handle_qa(textq)
            self.content['常见问题'] = qa.con
        
        ## 咨询/投诉方式
        textc = soup.find_all(class_='con-r-list pt3')
        if len(textc) == 0:
            print("No Consult/Complaint")
        else:
            textc = str(textc[0])
            cc = CC()
            cc.handle_cc(textc)
            self.content['咨询/投诉方式'] = cc.con
        
        ## 收费信息
        textf = soup.find_all(class_='con-r-list pt4')
        if len(textf) == 0:
            print('No Fee')
        else:
            textf = str(textf[0])
            fee = Fee()
            fee.handle_fee(textf)
            self.content['收费信息'] = fee.con
    
    def saveToFile(self,path):
        self.handle_con()
        saveToFile(path+str(self.content['pid'])+'_'+str(self.content['idx'])+'.json',self.content)


    # def unfold(self):
    #     pat = '<div class="(tab-btn zk.*?)".*?>.*?</div>'
    #     text = self.browser.page_source
    #     saveToFile('1.txt',text)
    #     zk_lst = re.findall(pat,text,re.S)
    #     print(zk_lst)
    #     if len(zk_lst) == 0:
    #         return 
    #     else:
            
    #         for zk in zk_lst:
    #             # print(zk)
    #             # self.browser.find_element_by_class_name(zk).click()  
    #             self.browser.find_element_by_class_name("tab-btn zk").click()  
    #         return 



res = getFromFile('../SDQZdata/pagedetail_qd.json')
browser = webdriver.Firefox()
sample,blank = 0,0
for r in tqdm(res):
    if '实施清单' in r:
        nxp_lst = r['实施清单']
        # print(r)
        pid = r['idx']
        # if pid % 100 == 0:
        #     print(sample,blank)
        for i in range(len(nxp_lst)):
            nxp = nxp_lst[i]
            url = nxp['nxurl']
            # title = nxp['nxtitle']
            # dep = nxp['bm_dep']
            gp = GuidePage(pid,i,url,browser,0)
            # gp.handle_con()
            gp.saveToFile('../SDQZdata/qd/')

            # ts_tb = gp.handle_con()
            # if ts_tb:
            #     ts,tb = ts_tb
            #     sample += ts
            #     blank += tb
### 山东省
## 3800 1277 1180
## 3801: 918 844
## sum: 2195 2024
# print("示例样本：",sample)
# print("空白样本：",blank)
            
            
        
# # url = 'http://www.shandong.gov.cn/api-gateway/jpaas-jiq-web-sdywtb/front/transition/ywTransToDetail?innerCode=21686'
# url = 'http://www.shandong.gov.cn/api-gateway/jpaas-jiq-web-sdywtb/front/transition/ywTransToDetail?innerCode=603'
# browser = webdriver.Firefox()
# gp = GuidePage(1,1,url,browser)
# gp.saveToFile('../SDQZdata/sd/')
