import os
import pdb
from tqdm import tqdm

ori_ids = open('./SLC_task/dep7/ids_SLC_1.txt', 'r').readlines()
proto = open('./SLC_task/dep7/proto_book_dep_7.txt', 'r').readlines()

cur_ids = open('./SLC_task/dep7/ids_SLC_cur.txt', 'w', encoding='utf-8')

proto_list = []
for pro in proto:
    pro = pro.strip()
    char = pro.split(':')[0]
    proto_list.append(char)

# print(proto_list)
for idss in tqdm(ori_ids):
    idss = idss.strip()
    char, ids = idss.split(':')
    if char in proto_list:
        cur_ids.write(f'{char}:{char}\n')
    else:
        cur_ids.write(f'{char}:{ids}\n')
    