#! /usr/bin/env python
# -*- coding: utf-8 -*-

f1=open('/Users/ckl/2.in')
f2=open('/Users/ckl/1.in')
w=open('/Users/ckl/1.out','w')

d={}
for p in f2.readlines():
    if len(p)>5:
        h=p[:-1].split(',')
        if len(h)>1:
            d[h[1]]=int(h[0])
for p in f1.readlines():
    if len(p) >4:
        h=p[:-1].split('\t')
        print h,len(h)
        if h[1] in d.keys():
            w.write('\"%s\":%s,\n'%(d[h[1]],h[0]))
w.close()
f1.close()
f2.close()
