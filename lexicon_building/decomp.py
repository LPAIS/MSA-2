import os
import sys
import json
import pdb
import treelib
from treelib import Node, Tree
import time
import re
from tqdm import tqdm

structure_symbols = ['⿵', '⿹', '⿲', '⿴', '⿶', '⿷', '⿻', '⿰', '⿳', '⿱', '⿺', '⿸']

bi_son_symbols = ['⿵', '⿹', '⿴', '⿶', '⿷', '⿻', '⿰', '⿱', '⿺', '⿸']

tri_son_symbols = ['⿲', '⿳']

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

    # pdb.set_trace()

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


def get_tree(tokens):
    radical_tree = parse_tree(tokens)
    if any([(_ in tokens) for _ in tri_son_symbols]):
        radical_tree = tri_symbols_replace(radical_tree)
    return radical_tree

def ids_Sort(ids):
    ids = re.sub(r"([^&;])", r"\1 ", ids)
    ids = re.sub(r"&[^&;]+;", lambda m: m.group().replace(" ", ""), ids)
    ids = ids.replace(';','; ')
    ids = ids.strip()
    return ids



def decomp(tokens, dep, depth_ori):
    # pdb.set_trace()
    radical_tree = get_tree(tokens)
    depth = radical_tree.depth()
    # pdb.set_trace()
    if depth >= 7-dep-depth_ori+1:
        return tokens
    else:
        new_ids = []
        for token in tokens:
            if token in char_list and len(char_ini[token]) > 1:  # 判断是否可拆
                tmp = decomp(char_ini[token], dep+1, depth_ori)
                # pdb.set_trace()
                for i in tmp:
                    new_ids.append(i)
            else:
                new_ids.append(token)
        radical_tree = get_tree(new_ids)
        depth = radical_tree.depth()
        if depth >= 7-dep-depth_ori+1:
            return tokens
        else:
            return new_ids


if __name__ == '__main__':
    t_start = time.time()
    txt_file = './ids_SLC_1.txt' # 这里放未拆解的ids
    lines = open(txt_file, 'r', encoding='utf-8').readlines()
    f = open('./SLC_dep_7.txt','w',encoding='utf-8')
    
    char_list = []
    char_ini = {}
    for line in lines:
        char = line.split(':')[0]
        ids = line.split(':')[1].strip().split(' ')
        char_list.append(char)
        char_ini[char] = ids
    radical_trees = dict()
    counter = 0
    i = 0
    for line in tqdm(lines):
        i += 1
        tokens = line.split(':')[1].strip().split(' ')
        char = line.split(':')[0]
        radical_tree = get_tree(tokens)
        radical_trees[char] = radical_tree
        depth = radical_tree.depth()
        flag = True #判断是否被拆
        num = 0
        new_ids = decomp(tokens, 0, depth)
        ids = ' '.join(new_ids)
        radical_tree = get_tree(new_ids)
        depth = radical_tree.depth()
        f.write(f'{char}:{ids}\n')
        if depth > 7:
            counter += 1
            print(char)
            print(ids)
            print(depth)
            radical_tree.show()
            dep_supper_9 = open('./dep_supper_9.txt','a',encoding='utf-8')
            dep_supper_9.write(f'{char}:{ids}:{depth}\n')
            dep_supper_9.close()
            # import pdb;pdb.set_trace()
        if i % 1000 == 0:
            t_end = time.time()
            print(f'{i}::{char}:::{str(t_end-t_start)}')
            t_start = t_end
    print(counter)