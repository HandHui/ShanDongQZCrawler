import requests
from bs4 import BeautifulSoup
from util import *
import re
import os
import time
from tqdm import tqdm
from selenium import webdriver
import random


class PageDetail:

    def __init__(self,idx,url_code=None,url=None,region_code=None):
        self.idx = idx
        if url_code:
            self.url = 'http://www.shandong.gov.cn/api-gateway/jpaas-jiq-web-sdywtb/front/item/qzqdej_index?itemCode=' + \
                                        url_code + '&orgCode=&regionCode='+region_code
        else:
            self.url = url
        self.text = ""
        self.content = {}
        self.content['idx'] = idx
        self.content['url'] = self.url
        self.parse()
        print(self.url)
    
    def parse(self):
        headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        
        user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    ]
        headers['User-Agent'] = random.choice(user_agent_list).encode("utf-8").decode("latin1")
        # headers = headers.encode("utf-8").decode("latin1")
        req = requests.get(self.url,headers = headers)
        self.text = req.text
        # print(self.text)

    def handle_info(self):
        # self.parse()
        # print(self.url)
        soup = BeautifulSoup(self.text,'lxml')
        con1 = soup.find_all(class_='qd-con1')
        if len(con1) == 0:
            print("info con1 length = 0")
            return
        con = str(con1[0])
        tds = re.findall('<td.*?>(.*?)</td>',con)

        self.content['基本信息'] = {}
        binfo = self.content['基本信息']

        for i in range(0,len(tds),2):
            binfo[tds[i]] = tds[i+1]
    
    def handle_tab(self,browser):
        # self.parse()
        soup = BeautifulSoup(self.text,'lxml')
        tab2 = soup.find_all(class_='qd-tab2')
        if len(tab2) == 0:
            print("tab length == 0")
            return 
        tab = str(tab2[0])
        pat = '<div class="fwmc mingcheng fwmc.*?" title=".*?"><a href="(.*?)".*?target="_blank">(.*?)</a></div>'
        href_tname = re.findall(pat,tab)

        pat1 = '<div class="bm mingcheng">(.*?)</div>'
        bm_dep = re.findall(pat1,tab)
        bm_dep = bm_dep[1:]
        #  print(bm_dep)
        assert len(href_tname) == len(bm_dep)
        
        if len(href_tname) > 0:
            self.content['实施清单'] = []
            for i in range(len(href_tname)):
            # for ht in href_tname:
                ht = href_tname[i]
                imp = {}
                imp['nxurl'] = ht[0]
                imp['nxtitle'] = ht[1]
                imp['bm_dep'] = bm_dep[i]
                self.content['实施清单'].append(imp)
        
        # while self.nextPage(browser):
        #     soup = BeautifulSoup(self.text,'lxml')
        #     tab2 = soup.find_all(class_='qd-tab2')
        #     if len(tab2) == 0:
        #         print("tab length == 0")
        #         return 
        #     tab = str(tab2[0])
        #     pat = '<div class="fwmc mingcheng fwmc.*?" title=".*?"><a href="(.*?)".*?target="_blank">(.*?)</a></div>'
        #     href_tname = re.findall(pat,tab)

        #     pat1 = '<div class="bm mingcheng">(.*?)</div>'
        #     bm_dep = re.findall(pat1,tab)
        #     bm_dep = bm_dep[1:]
        #     assert len(href_tname) == len(bm_dep)
            
        #     if len(href_tname) > 0:
        #         for i in range(len(href_tname)):
        #         # for ht in href_tname:
        #             ht = href_tname[i]
        #             imp = {}
        #             imp['nxurl'] = ht[0]
        #             imp['nxtitle'] = ht[1]
        #             imp['bm_dep'] = bm_dep[i]
        #             self.content['实施清单'].append(imp)

    
    def nextPage(self,browser):
        text = browser.page_source
        # print(text)
        ## <a href="javascript:;" class="laypage_next" data-page="2">下一页</a>
        pat = '<a href="javascript:;" class="laypage_next" data-page=".*?">下一页</a>'
        if re.search(pat,text) == None:
            print("final page")
            return 0
        else:
            browser.find_element_by_class_name('laypage_next').click()  ## brower变成了下一页
            time.sleep(1)
            self.text = browser.page_source
            return 1



### 第一阶段
# res = getFromFile('sd/pagelist.json')

# ans = []

# for r in tqdm(res):
#     idx = r['idx']
#     if idx <= 700:
#         continue
#     url_code = r['url_code']
#     if url_code:
#         try:
#             pd = PageDetail(idx,url_code)
#             pd.handle_info()
#             pd.handle_tab()
#             ans.append(pd.content)
#         except Exception as e:
#             print(e)
#             time.sleep(10)
        
#         if idx % 100 == 0:
#             saveToFile('sd/pagedetail700.json',ans)  ### 200表示200及以后的内容
#                                                      ### 700同理
#     time.sleep(0.5)
#         # print(pd.content)
# saveToFile('sd/pagedetail700.json',ans)

## 第二阶段
## 找到所有的nxurl，但是因为没有regioncode限制 拿到的都是全省的数据
# res = getFromFile('sd/pagedetail.json')
# # idx = 123
# # url_code = None
# # url = 'http://www.shandong.gov.cn/api-gateway/jpaas-jiq-web-sdywtb/front/item/qzqdej_index?itemCode=E33CF7C910D04B80A01D1BE484878972'
# ans = []
# browser = webdriver.Firefox()
# for r in tqdm(res):
#     idx = r['idx']
#     if '实施清单' not in r:
#         ans.append(r)
#         continue
#     elif len(r['实施清单']) < 10:
#         ans.append(r)
#         continue
#     else:
#         # imp = {}
        
#         url = r['url']
#         url_code = None

#         try:
            
#             browser.get(url)
#             pd = PageDetail(idx,url_code=None,url=url)
#             pd.handle_info()
#             pd.handle_tab(browser)
#             ans.append(pd.content)
#         except Exception as e:
#             print(e)
#             print("wait 10 sec!!!")
#             time.sleep(10)
        
#         if idx % 100 == 0:
#             saveToFile('sd/pagedetail2.json',ans)

# saveToFile('sd/pagedetail2.json',ans)


# 第三阶段
# print(os.listdir('../SDQZdata/'))
# 添加region_code对内容进行限制，只爬取省级信息
res = getFromFile('../SDQZdata/pagedetail_all.json')
# pagedetail2中 包含着 山东省的全部信息，本阶段是进行简化，只爬取省级/青岛市级别的数据
# idx = 123
# url_code = None
# url = 'http://www.shandong.gov.cn/api-gateway/jpaas-jiq-web-sdywtb/front/item/qzqdej_index?itemCode=E33CF7C910D04B80A01D1BE484878972'
ans = []
browser = webdriver.Firefox()
region_code = '370200000000'

for r in tqdm(res):
    idx = r['idx']
    if '实施清单' not in r:
        ans.append(r)
        continue
    else:
        # imp = {}
        
        url = r['url']
        url = url + '&orgCode=&regionCode=' + region_code
        url_code = None

        try:
            
            browser.get(url)
            pd = PageDetail(idx,url_code=None,url=url,region_code = region_code)
            pd.handle_info()
            pd.handle_tab(browser)
            ans.append(pd.content)
        except Exception as e:
            print(e)
            print("wait 10 sec!!!")
            time.sleep(10)
        
    if idx % 100 == 0:
        saveToFile('sd/pagedetail_qd.json',ans)

saveToFile('sd/pagedetail_qd.json',ans)
        

        



