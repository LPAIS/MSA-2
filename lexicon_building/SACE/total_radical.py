# 该文件用来统计，ids中最大的部首数量
import os
from tqdm import tqdm
import pdb

f = open('./SLC_task/dep7/SLC_dep_7_cur.txt', 'r').readlines()

bi_son_symbols = ['⿵', '⿹', '⿴', '⿶', '⿷', '⿻', '⿰', '⿱', '⿺', '⿸']
num_list = []
for cids in tqdm(f):
    cids = cids.strip()
    char, ids = cids.split(':')
    ids = ids.split(' ')
    tmp = []
    for radical in ids:
        if radical not in bi_son_symbols:
            tmp.append(radical)
    num_list.append(len(tmp))
    # if len(tmp) == 16:
    #     pdb.set_trace()
print(max(num_list))

