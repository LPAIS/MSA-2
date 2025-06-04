import os
import sys
import json
import pdb
import math
import torch
import treelib
import numpy as np
from treelib import Node, Tree
from math import log, floor, ceil
from tqdm import tqdm

structure_symbols = ['⿵', '⿹', '⿲', '⿴', '⿶', '⿷', '⿻', '⿰', '⿳', '⿱', '⿺', '⿸']
bi_son_symbols = ['⿵', '⿹', '⿴', '⿶', '⿷', '⿻', '⿰', '⿱', '⿺', '⿸']
tri_son_symbols = ['⿲', '⿳']

mth = open("./SLC_dep_7.txt", 'r', encoding='utf-8').readlines() # 这里存放整理好的ids，格式‘临:⿰ 〢 ⿱ ⿱  丶 𫩏’
radi_set = set()
for line in mth:
    line = line.split(':')[-1]
    line = line.replace('\n', '')
    radicals = line.split(' ')
    for i in radicals:
        if i not in structure_symbols:
            radi_set.add(i)
# pdb.set_trace()
char2num = {}
proto_binary = {}
radi_set = list(radi_set)
for idx in range(0, len(radi_set)):

    tmp = np.random.randint(0, 2, 60)
    tmp = list(tmp)
    while tmp in proto_binary.values():
        tmp = np.random.randint(0, 2, 60)
        tmp = list(tmp)
    radical = radi_set[idx]
    proto_binary[radical] = tmp
# pdb.set_trace()

f = open('./proto_book_dep_7_r60.txt', 'w', encoding='utf-8')
for radical in proto_binary:
    line = ''
    line += radical
    line += ':'
    code = proto_binary[radical]
    code_ = ''
    for i in code:
        code_ += str(i)
    line += code_
    line += '\n'
    f.write(line)
print('get_protobook')
f.close()


def print_tree_custom(tree):
    for node_id in tree.nodes:
        node = tree[node_id]
        print(f"{node.tag}{' ' if node.is_leaf() else ''}")


def parse_tree(tokens):
    radical_tree = Tree()
    parent_stack = []
    for tree_cursor in range(0, len(tokens)):
        # 从头建树
        if len(parent_stack) == 0:
            radical_tree.create_node(tokens[tree_cursor], tree_cursor)
            # radical_tree.create_node(tokens[tree_cursor], tree_cursor)
            parent_stack.append(tree_cursor)
            continue

        # 添加子节点
        radical_tree.create_node(tokens[tree_cursor], tree_cursor, parent=parent_stack[-1])

        # 父节点出栈
        if (len(radical_tree.children(parent_stack[-1])) == 3 and tokens[parent_stack[-1]] in tri_son_symbols) or\
           (len(radical_tree.children(parent_stack[-1])) == 2 and tokens[parent_stack[-1]] in bi_son_symbols):
            parent_stack.pop()

        if tokens[tree_cursor] in structure_symbols:
            parent_stack.append(tree_cursor)


    return radical_tree


def tri_symbols_replace(radical_tree):
    # radical_tree.show()
    replace_dict = {'⿲': '⿰', '⿳': '⿱'}
    tobe_replaced_identifiers = [_ for _ in radical_tree.nodes if radical_tree.nodes[_].tag in replace_dict]

    for identifier in tobe_replaced_identifiers:
        children_id = [i.identifier for i in radical_tree.children(identifier)]
        radical_tree[identifier].tag = replace_dict[radical_tree[identifier].tag]
        radical_tree.create_node(radical_tree[identifier].tag, 'new_son_of_{}'.format(identifier), parent=identifier)
        if len(children_id) < 3:
            pdb.set_trace()
        radical_tree.move_node(children_id[1], 'new_son_of_{}'.format(identifier))
        radical_tree.move_node(children_id[2], 'new_son_of_{}'.format(identifier))
    # radical_tree.show()
    return radical_tree


def parse_structure(radical_tree):
    # # #深度为5(指的是论文的深度),按照代码的话 深度是6
    # structure = [0 for i in range(15)]
    # IDC_id = [0 for i in range(15)]
    # id_dict = {0:(1, 2), 1:(3, 4), 2:(5, 6), 3:(5, 8), 4:(9, 10), 5:(11, 12), 6:(13, 14),
    #            7:(15, 16), 8:(17, 18), 9:(19, 20), 10:(21, 22), 11:(23, 24), 12:(25, 26),
    #            13:(27, 28), 14:(29, 30)}
    
    # # #深度为6(指的是论文的深度),按照代码的话 深度是7
    # structure = [0 for i in range(31)]
    # IDC_id = [0 for i in range(31)]
    # id_dict = {0:(1, 2), 1:(3, 4), 2:(5, 6), 3:(7, 8), 4:(9, 10), 5:(11, 12), 6:(13, 14),
    #            7:(15, 16), 8:(17, 18), 9:(19, 20), 10:(21, 22), 11:(23, 24), 12:(25, 26),
    #            13:(27, 28), 14:(29, 30), 15:(31, 32), 16:(33, 34), 17:(35, 36), 18:(37, 38),
    #            19:(39, 40), 20:(41, 42), 21:(43, 44), 22:(45, 46), 23:(47, 48), 24:(49, 50),
    #            25:(51, 52), 26:(53, 54), 27:(55, 56), 28:(57, 58), 29:(59, 60), 30:(61, 62)} 

    # # #深度为7(指的是论文的深度),按照代码的话 深度是8
    structure = [0 for i in range(63)]
    IDC_id = [0 for i in range(63)]
    id_dict = {0:(1, 2), 1:(3, 4), 2:(5, 6), 3:(7, 8), 4:(9, 10), 5:(11, 12), 6:(13, 14),
               7:(15, 16), 8:(17, 18), 9:(19, 20), 10:(21, 22), 11:(23, 24), 12:(25, 26),
               13:(27, 28), 14:(29, 30), 15:(31, 32), 16:(33, 34), 17:(35, 36), 18:(37, 38),
               19:(39, 40), 20:(41, 42), 21:(43, 44), 22:(45, 46), 23:(47, 48), 24:(49, 50),
               25:(51, 52), 26:(53, 54), 27:(55, 56), 28:(57, 58), 29:(59, 60), 30:(61, 62),
               31:(63, 64), 32:(65, 66), 33:(67, 68), 34:(69, 70), 35:(71, 72), 36:(73, 74),
               37:(75, 76), 38:(77, 78), 39:(79, 80), 40:(81, 82), 41:(83, 84), 42:(85, 86),
               43:(87, 88), 44:(89, 90), 45:(91, 92), 46:(93, 94), 47:(95, 96), 48:(97, 98),
               49:(99, 100), 50:(101, 102), 51:(103, 104), 52:(105, 106), 53:(107, 108), 54:(109, 110),
               55:(111, 112), 56:(113, 114), 57:(115, 116), 58:(117, 118), 59:(119, 120), 60:(121, 122),
               61:(123, 124), 62:(125, 126)} 
    
    # #深度为8(指的是论文的深度),按照代码的话 深度是9
    # structure = [0 for i in range(127)]
    # IDC_id = [0 for i in range(127)]
    # id_dict = {0:(1, 2), 1:(3, 4), 2:(5, 6), 3:(7, 8), 4:(9, 10), 5:(11, 12), 6:(13, 14),
    #            7:(15, 16), 8:(17, 18), 9:(19, 20), 10:(21, 22), 11:(23, 24), 12:(25, 26),
    #            13:(27, 28), 14:(29, 30), 15:(31, 32), 16:(33, 34), 17:(35, 36), 18:(37, 38),
    #            19:(39, 40), 20:(41, 42), 21:(43, 44), 22:(45, 46), 23:(47, 48), 24:(49, 50),
    #            25:(51, 52), 26:(53, 54), 27:(55, 56), 28:(57, 58), 29:(59, 60), 30:(61, 62),
    #            31:(63, 64), 32:(65, 66), 33:(67, 68), 34:(69, 70), 35:(71, 72), 36:(73, 74),
    #            37:(75, 76), 38:(77, 78), 39:(79, 80), 40:(81, 82), 41:(83, 84), 42:(85, 86),
    #            43:(87, 88), 44:(89, 90), 45:(91, 92), 46:(93, 94), 47:(95, 96), 48:(97, 98),
    #            49:(99, 100), 50:(101, 102), 51:(103, 104), 52:(105, 106), 53:(107, 108), 54:(109, 110),
    #            55:(111, 112), 56:(113, 114), 57:(115, 116), 58:(117, 118), 59:(119, 120), 60:(121, 122),
    #            61:(123, 124), 62:(125, 126),
    #            63:(127, 128), 64:(129, 130), 65:(131, 132), 66:(133, 134), 67:(135, 136), 68:(137, 138), 69:(139, 140),
    #            70:(141, 142), 71:(143, 144), 72:(145, 146), 73:(147, 148), 74:(149, 150), 75:(151, 152),
    #            76:(153, 154), 77:(155, 156), 78:(157, 158), 79:(159, 160), 80:(161, 162), 81:(163, 164),
    #            82:(165, 166), 83:(167, 168), 84:(169, 170), 85:(171, 172), 86:(173, 174), 87:(175, 176),
    #            88:(177, 178), 89:(179, 180), 90:(181, 182), 91:(183, 184), 92:(185, 186), 93:(187, 188),
    #            94:(189, 190), 95:(191, 192), 96:(193, 194), 97:(195, 196), 98:(197, 198), 99:(199, 200),
    #            100:(201, 202), 101:(203, 204), 102:(205, 206), 103:(207, 208), 104:(209, 210), 105:(211, 212),
    #            106:(213, 214), 107:(215, 216), 108:(217, 218), 109:(219, 220), 110:(221, 222), 111:(223, 224),
    #            112:(225, 226), 113:(227, 228), 114:(229, 230), 115:(231, 232), 116:(233, 234), 117:(235, 236),
    #            118:(237, 238), 119:(239, 240), 120:(241, 242), 121:(243, 244), 122:(245, 246), 123:(247, 248),
    #            124:(249, 250), 125:(251, 252), 126:(253, 254)} 
    
    # #深度为5的满二叉树，最多有15个双子节点
    # pdb.set_trace()

    def dfs(Node, id):
        if Node.tag not in bi_son_symbols:
            return
        elif Node.tag in bi_son_symbols: 
            structure[id] = 1 #如果是结构符号，记录为1
            IDC_id[id] = Node.identifier #将节点标识符储存
            children = radical_tree.children(Node.identifier)
            # pdb.set_trace()
            try:
                id1, id2 = id_dict[id]
                # pdb.set_trace()
            except KeyError:
                print('err1')
                # pdb.set_trace()
            # pdb.set_trace()
            dfs(children[0], id1)
            try:
                dfs(children[1], id2)
            except IndexError:
                # radical_tree.show()
                print('err2')
                # pdb.set_trace()

    dfs(radical_tree[0], 0)
    # pdb.set_trace()
    return structure, IDC_id


def binary_encoding(index):
    if index < 0 or index >= 16:
        raise ValueError("Index out of range for 4-bit binary encoding")
    # 将整数转换成二进制字符串，去掉前缀'0b'
    binary_str = bin(index)[2:] 
    # 在前面补零直到长度为4
    binary_str = binary_str.zfill(4)
    # 将二进制字符串转换为列表
    return [int(bit) for bit in binary_str]


def long_binary_encoding(indexes, n, c=2):
    # 创建一个空的结果列表
    encodings = []
    
    # 遍历每个索引
    for index in indexes:
        # 初始化编码向量
        encoding = np.zeros(n).astype('int')
        
        # 使用cosine函数生成编码，可以换成sine函数
        for i in range(n):
            # 通过调整频率和相位使每个位置的值不同
            value = math.cos(c * math.pi * (index + i) / n)
            
            # 将cosine值映射到0或1
            if value > 0.0:
                encoding[i] = 1
        
        # 将编码添加到结果列表中
        encodings.append(encoding)
    
    return encodings


def get_IDC_codebook(n, symbol_list):
    structural_list = symbol_list
    IDC_codebook_n  = {}
    indexes = []
    for i in range(len(symbol_list)):
        indexes.append(i) 
        
    if n>4:
        coff = (16/n)*2
        binary_encodings = long_binary_encoding(indexes, n, c=coff)
        for i, encoding in enumerate(binary_encodings):
            IDC_codebook_n[structural_list[i]] = encoding.tolist()

    elif n>2:
        for i in indexes:
            IDC_codebook_n[structural_list[i]] = binary_encoding(i+1)

    elif n>1:
        Enclose = {'⿵', '⿹', '⿴', '⿶', '⿷', '⿺', '⿸'}
        Compose = {'⿰', '⿱'}
        Special = {'⿻'}
        for ele in structural_list:
            if ele in Enclose:
                IDC_codebook_n[ele]=[1,0]
            elif ele in Compose:
                IDC_codebook_n[ele]=[0,1]
            elif ele in Special:
                IDC_codebook_n[ele]=[1,1]

    else:
        for ele in structural_list:
            IDC_codebook_n[ele]=[1]
        
    return IDC_codebook_n


def dynamic_SE(radical_tree):
    structure, IDC_id = parse_structure(radical_tree)
    IDC = [0 for i in range(112)]

    '''
     HierCode: D=5 4*1 + 4*2 + 4*4 + 4*8 + 4*16(all bl.) = 124
     Ours:     D=5 16*1+ 8*2 + 4*4 + 2*8 + 1*16(all bl.) = 80 

     HierCode: D=7 4*1 + 4*2 + 4*4 + 4*8 + 4*16 + 4*32 + (all bl.) = 252
     Ours:     D=7 16*1+ 8*2 + 4*4 + 2*8 + 1*16 + 1*32 + (all bl.) = 112 

     因此，论文中HierCode选D=5，我们的方法选D=6
    '''
    
    # 16*1 + 8*2 + 4*4 + 2*8 = 64 D=5
    # 16*1 + 8*2 + 4*4 + 2*8 + 1*16 + 1*32 = 112
    # 16*1 + 8*2 + 4*4 + 2*8 + 1*16 + 1*32 + 1*64 = 
    
    IDC_codebook = {'16': get_IDC_codebook(16, bi_son_symbols),
                    '8':  get_IDC_codebook(8, bi_son_symbols),
                    '4':  get_IDC_codebook(4, bi_son_symbols),
                    '2':  get_IDC_codebook(2, bi_son_symbols),
                    '1':  get_IDC_codebook(1, bi_son_symbols)}
  
    # structure encoding
    # 建立一个全0 list, 有tag的地方给其赋值1, 否则仍为0
    init_len = 16
    start  = 0
    for i in range(31): #15
        length = max(int(init_len/(2**floor(log((i+1), 2)))), 1) 
        # print(start)
        # structure即为flag,若为1则是结构信息
        # IDC_id则表示对应位置的结构信息在tree中的位置
        # 利用identifier可以来判断位于tree的第几层
        if structure[i] == 1:
            char = radical_tree[IDC_id[i]].tag
            code = IDC_codebook[str(length)][char]
            for num, j in enumerate(code):
                IDC[start+num] = j

        start += length

    # radical encoding
    encode_dimension = 60
    max_radicals = 16
    radical = [0 for i in range(encode_dimension*max_radicals)] #36*9 45*23
    counter = 0
    for node in radical_tree.nodes:  
        if radical_tree[node].tag not in bi_son_symbols:
            try:
                radi = radical_tree[node].tag
            except KeyError as err:
                print(err)
                # pdb.set_trace()
            # pdb.set_trace()
            code = proto_binary[radi]
            start = counter * encode_dimension
            for num, j in enumerate(code):
                try:
                    radical[start+num] = j
                except IndexError as err:
                    print(err)
                    # pdb.set_trace()
            counter += 1

    code = IDC + radical

    return  code


if __name__ == '__main__':
    codebook = {}
    txt_file = './SLC_dep_7_cur.txt' # 和第16行一样，这里存放整理好的ids，格式‘临:⿰ 〢 ⿱ ⿱  丶 𫩏’ 
    # txt_file = '/Users/wang/Desktop/Work/radical/decompose-radical-27533.txt'
    lines = open(txt_file, 'r', encoding='utf-8').readlines()
    f = open('./UniSA_dep7_r60-16.txt', 'w', encoding='utf-8') # 这里主要用于存放hiercode编码
    radical_trees = {}
    for i,line in tqdm(enumerate(lines)):
        i+=1
        try:
            tokens = line.split(':')[1].strip().split(' ')
            radical_tree = parse_tree(tokens)
            char = line.split(':')[0]
            # pdb.set_trace()
            # radical_tree.show()

            if any([(_ in tokens) for _ in tri_son_symbols]):
                radical_tree = tri_symbols_replace(radical_tree)

            # print(f'{char}:{str(i)}')
            code = dynamic_SE(radical_tree)
            codebook[char] = code
            radical_trees[char] = radical_tree
            # print(f'{char}:{str(i)}')
            
        except:
            print(char)
           

    for line in lines:
        try:
            line_code = ''
            char = line.split(':')[0]
            line_code += char
            line_code += ':'
            code = codebook[char]
            for i in code:
                # if i == 0:
                #     i = -1
                line_code += str(i)
            line_code += '\n'
            f.write(line_code)
            
        except:
            pass
    f.close()