from util import *
from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
from tqdm import tqdm

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
    
    def handle_con(self):
        text = self.browser.page_source
        soup = BeautifulSoup(text,'lxml')

        ## 
        text_mat = soup.find_all(id='md7')
        if len(text_mat) == 0:
            print('No Material!!')
            # return
        else:
            text_mat = str(text_mat[0])
            mat = Material()
            mat.handleCon(text_mat)
            if self.flag == 1:
                return mat.handle_len()
            # print(mat.con)



res = getFromFile('../SDQZdata/pagedetail_sd.json')
browser = webdriver.Firefox()
sample,blank = 0,0
for r in tqdm(res):
    if '实施清单' in r:
        nxp_lst = r['实施清单']
        # print(r)
        pid = r['idx']
        for i in range(len(nxp_lst)):
            nxp = nxp_lst[i]
            url = nxp['nxurl']
            # title = nxp['nxtitle']
            # dep = nxp['bm_dep']
            gp = GuidePage(pid,i,url,browser,1)
            ts,tb = gp.handle_con()
            sample += ts
            blank += tb

print("示例样本：",sample)
print("空白样本：",blank)
            
            
        

# url = 'http://www.shandong.gov.cn/api-gateway/jpaas-jiq-web-sdywtb/front/transition/ywTransToDetail?innerCode=21686'
# browser = webdriver.Firefox()
# gp = GuidePage(1,1,url,browser)
# gp.handle_con()
