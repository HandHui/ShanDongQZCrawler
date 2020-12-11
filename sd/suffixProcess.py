from util import *
import json

### 合并多次爬取的pagedetail
# res1 = getFromFile('sd/pagedetail.json')
# print(len(res1))

# res2 = getFromFile('sd/pagedetail200.json')
# print(len(res2))

# res3 = getFromFile('sd/pagedetail700.json')
# print(len(res3))

# res = res1 + res2 + res3
# saveToFile('sd/pagedetail.json',res)

res = getFromFile('sd/pagedetail_sd.json')
for r in res:
    if '实施清单' in r:
        if len(r['实施清单']) > 8:
            print(r)