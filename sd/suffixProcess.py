from util import *
from tqdm import tqdm
import json
import os

### 合并多次爬取的pagedetail
# res1 = getFromFile('sd/pagedetail.json')
# print(len(res1))

# res2 = getFromFile('sd/pagedetail200.json')
# print(len(res2))

# res3 = getFromFile('sd/pagedetail700.json')
# print(len(res3))

# res = res1 + res2 + res3
# saveToFile('sd/pagedetail.json',res)

# res = getFromFile('sd/pagedetail_sd.json')
# for r in res:
#     if '实施清单' in r:
#         if len(r['实施清单']) > 8:
#             print(r)

# path = '../SDQZdata/qd/'
# sample_url,blank_url = 0,0
# fnames = os.listdir(path)
# for fname in tqdm(fnames):
#     npath = path+fname
#     con = getFromFile(npath)

#     if '材料目录' in con:
#         mats = con['材料目录']
#         for mat in mats:
#             if '空白表格' in mat:
#                 blank_url += (0 if mat['空白表格'] == '' else 1)
#             if '示例样表' in mat:
#                 sample_url += (0 if mat['示例样表'] == '' else 1)

# print('空白表格数: ',blank_url)   ## 1507
# print('示例样表数: ',sample_url)  ## 1537



