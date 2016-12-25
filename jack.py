#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/12/19 19:03
# @Author  : r00t
# @Site    : 
# @File    : jack.py
# @Software: PyCharm

import urllib2
import re
from pyquery import PyQuery
from lxml import etree

for i in range(1,2):
    url = 'http://www.baidu.com.cn/member/view.php?userid=%d' % (i)
    page = urllib2.urlopen(url)
    html = page.read()
    #查找<td></td>的内容
    #因为要匹配的数据都在<td></td>里面，只要匹配出所有的<td></td>,匹配出来的数据是个list,然后取下标就可以了
    rex = re.compile(r'<td>(.*?)</td>')
    email = re.findall(rex,html)[0]
    phone = re.findall(rex,html)[6]
    tel = re.findall(rex,html)[7]
    print email,phone,tel

