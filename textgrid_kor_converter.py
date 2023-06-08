#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import os
from jamo import h2j, j2hcj
from glob import glob


# In[2]:


text_dict = {
    '"aa"':'"ᅡ"',
    '"c0"':'"ᄌ"',
    '"cc"':'"ᄍ"',
    '"ch"':'"ᄎ"',
    '"ee"':'"ᅦ"',
    '"h0"':'"ᄒ"',
    '"ii"':'"ᅵ"',
    '"k0"':'"ᄀ"',
    '"kf"':'"ᆨ"',
    '"kh"':'"ᄏ"',
    '"kk"':'"ᄁ"',
    '"ll"':'"ᆯ"',
    '"mf"':'"ᆷ"',
    '"mm"':'"ᄆ"',
    '"nf"':'"ᆫ"',
    '"ng"':'"ᆼ"',
    '"nn"':'"ᄂ"',
    '"oo"':'"ᅩ"',
    '"p0"':'"ᄇ"',
    '"pf"':'"ᆸ"',
    '"ph"':'"ᄑ"',
    '"pp"':'"ᄈ"',
    '"qq"':'"ᅢ"',
    '"rr"':'"ᄅ"',
    '"s0"':'"ᄉ"',
    '"<SIL>"':'"sil"',
    '"ss"':'"ᄊ"',
    '"t0"':'"ᄃ"',
    '"tf"':'"ᆮ"',
    '"th"':'"ᄐ"',
    '"tt"':'"ᄄ"',
    '"uu"':'"ᅮ"',
    '"vv"':'"ᅥ"',
    '"wa"':'"ᅪ"',
    '"we"':'ㅞ',
    '"wi"':'"ᅱ"',
    '"wo"':'"ᅬ"',
    '"wq"':'"ᅫ"',
    '"wv"':'"ᅯ"',
    '"xi"':'"ᅴ"',
    '"xx"':'"ᅳ"',
    '"ya"':'"ᅣ"',
    '"ye"':'"ᅨ"',
    '"yo"':'"ᅭ"',
    '"yq"':'"ᅤ"',
    '"yu"':'"ᅲ"',
    '"yv"':'"ᅧ"',
}


# In[3]:


def getPhones(lines, name):
    res = ''
    if name == 'phone':
        res += '\titem [2]:\n'
    elif name == 'word':
        res += '\titem [1]:\n'
    res += '\t\tclass = {}\n'.format(lines[0])
    res += '\t\tname = {}\n'.format(lines[1][:-1]+'s'+lines[1][-1])
    res += '\t\txmin = {}\n'.format(float(lines[2]))
    res += '\t\txmax = {}\n'.format(float(lines[3]))
    res += '\t\tintervals: size = {}\n'.format(lines[4])
    
    if name == 'phone':
        for i in range(int(lines[4])):
            res += '\t\t\tintervals[{}]\n'.format(i+1)
            res += '\t\t\t\txmin = {}\n'.format(float(lines[5 + i * 3 ]))
            res += '\t\t\t\txmax = {}\n'.format(float(lines[5 + i * 3 + 1]))
            text = text_dict[lines[5 + i * 3 + 2]]
            res += '\t\t\t\ttext = {}\n'.format(text)
    elif name == 'word':
        for i in range(int(lines[4])):
            res += '\t\t\tintervals[{}]\n'.format(i+1)
            res += '\t\t\t\txmin = {}\n'.format(float(lines[5 + i * 3 ]))
            res += '\t\t\t\txmax = {}\n'.format(float(lines[5 + i * 3 + 1]))
            text = h2j(lines[5 + i * 3 + 2])
            res += '\t\t\t\ttext = {}\n'.format(text)
            
    length = 5 + int(lines[4]) * 3
    return res, length


# In[12]:


def getGrid(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = list(map(lambda s: s.strip(), lines))
    
    res = ''
    res += 'File type = "ooTextFile"' + '\n'
    res +='Object class = {}\n'.format(lines[1])
    res += lines[2] + '\n'
    res +='xmin = {}\n'.format(float(lines[3]))
    res +='xmax = {}\n'.format(float(lines[4]))
    res +='tiers? {}\n'.format(lines[5])
    res +='size = {}\n'.format(lines[6])
    res +='item []:\n'

    if lines[7] == '"IntervalTier"' and lines[8] == '"phone"':
        phones, eod = getPhones(lines[7:], 'phone')
    if lines[7 + eod] == '"IntervalTier"' and lines[8+ eod] == '"word"':
        words, eod = getPhones(lines[7 + eod:], 'word')
    
    res += words + phones
    return res


# In[13]:


filenames = glob('{}/*'.format(sys.argv[1]))

grids = []
for x in filenames:
    grid = getGrid(x)
    with open(x,'w',encoding='utf-8') as f:
        f.write(grid)
    grids.append(grid)


# In[ ]:




