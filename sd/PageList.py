from selenium import webdriver
from bs4 import BeautifulSoup
from util import *
import time
import re

class PageList:

    def __init__(self,browser):

        # self.url = url
        self.browser = browser
        self.idx = 0

        self.items = []
    
    def handle_con(self):
        browser = self.browser
        text = browser.page_source
        soup = BeautifulSoup(text,'lxml')
        centen_list = soup.find_all(class_='centen_list')
        item_list = centen_list[0].find_all(class_='s-secondItem2')
        for item in item_list:
            item_dict = {}
            item = str(item)

            item_dict['idx'] = self.idx
            self.idx += 1

            item_code = S_search('<a title=.*?>(.*?)</a>',item)
            item_dict['item_code'] = item_code  ##事项编码

            t = re.search('<a href=".*?" onclick="toSub\((.*?)\)" title=.*?>(.*?)</a>',item)
            if t:
                url_code,item_name = t.groups()
                url_code = eval(url_code)
                item_dict['url_code'] = url_code
                item_dict['item_name'] = item_name ##url_code and 事项名称
            else:
                print('url code Fail!!')
                item_dict['url_code'] = ""
                item_dict['item_name'] = ""

            item_dept = S_search('<div class="xzqh1" title=".*?">(.*?)</div>',item)
            item_dict['item_dept'] = item_dept ##事项部门

            item_subj = S_search('<div class="subject">(.*?)</div>',item)
            item_dict['item_subj'] = item_subj ##事项类别

            item_zx = S_search('<div class="zixiang1">(.*?)</div>',item)
            item_dict['item_zx'] = item_zx

            self.items.append(item_dict)
    
    def nextPage(self):
        text = self.browser.page_source
        pat = '<a href="javascript:;" class="laypage_next" data-page=".*?">下一页</a>'
        if re.search(pat,text) == None:
            return 0
        else:
            self.browser.find_element_by_class_name('laypage_next').click()  ## brower变成了下一页
            time.sleep(1)
            return 1
    
    def handle_all_page(self):
        
        while True:
            
            self.handle_con()
            if not self.nextPage():
                print(1)
                break
            # print(self.idx)
            if self.idx % 100 == 0:
                saveToFile('sd/pagelist.json',self.items)
        self.handle_con()
        saveToFile('sd/pagelist.json',self.items)


path1 = '../../sfdrive/geckodriver.exe'
url = 'http://www.shandong.gov.cn/api-gateway/jpaas-jiq-web-sdywtb/front/item/qzqd_index'
browser = webdriver.Firefox()
browser.get(url)
time.sleep(1)

plst = PageList(browser)
plst.handle_all_page()
# for p in plst.items:
#     print(p)
# <a href="javascript:;" class="laypage_next" data-page="626">下一页</a>



