import requests
import re
from util import *

url = 'http://www.shandong.gov.cn/api-gateway/jpaas-jiq-web-sdywtb/front/item/qzqd_index'
req = requests.get(url)
text = req.text

pat = '<li style="cursor:pointer;"  onclick="ssqdItems\(\'(.*?)\', .*?\)">(.*?)</li>'
dep_code = re.findall(pat,text)
print(dep_code)
saveToFile('sd/department_code.json',dep_code)


pat = '<a href=".*?" onclick="getRegions\(\'(.*?)\'.*?>(.*?)</a></li>'
region_code = re.findall(pat,text)
region_code.insert(0,('370000000000','山东省'))
print(region_code)
saveToFile('sd/region_code.json',region_code)
# print(req.text)