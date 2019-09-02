#!/usr/bin/python
#Python 2.7.16
#JD Vlok 2019-08-05 jdvlok@gmail.com
# 1. 2019-08-29: extract_pdf3.py: code written to execute as script within other code
# 2. 2019-08-30: drive_extraction.py: code calling extract_pdf3.py (~/Works2019/bowen/meta/drive_extraction.py)
# 3. 2019-08-30: drive_extract_txt.py: use station IDs in AUS_SATlist.txt (gen_temp_list.py) to extract meta PDF files

from __future__ import division
import numpy as np
import time
from extract_txt_onepdf import pdf2txt
import os

def readtxt(fn):
 f = open(fn)
 linelist = f.readlines()
 f.close()
# L = len(lines)
 return linelist

fn = './AUS_SATlist.txt'
IDstrings = readtxt(fn)

IDlist=[]
for IDstr in IDstrings:
 IDlist.append(np.int(IDstr))

Lx = len(IDlist)

tc,f3c = 0,0 #file exist counter
notexist = []
HOME = './Aug_2019_SAT'
for ID in IDlist:
 tc+=1
 idstr = '%06d'%ID
 fname = 'IDCJMD0040.%s.SiteInfo.pdf'%idstr
 pathfn = '%s/%s'%(HOME,fname)
 if os.path.isfile(pathfn):
  f3c+=1
  pdf2txt(ID,pathfn)
 else:
  notexist.append(ID)

print '%d files tested (%d), %d exist'%(tc,Lx,f3c)

# print
# print '*****************************************************************'
# print '*****************************************************************'
# print 'ID = %d'%ID
# print '*****************************************************************'
# print '*****************************************************************'
