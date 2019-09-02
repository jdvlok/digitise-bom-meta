#!/usr/bin/python
# Python 2.7.16
# JD Vlok 2019-07-18 jdvlok@gmail.com
# 2019-04-16: get_all_ACORN2.py: Download all ACORN data, hq: csv
# 2019-07-18: scrape_meta.py: Download all weather station meta data (pdf files)
# 2019-08-30: download_bom_meta_files: Download (wget) all SAT-measuring weather station meta data (pdf files)

from __future__ import division
import numpy as np
#import pylab as pl
import os
import time
#import urllib2
#import csv
#from mat:lotlib import rc #to use greek letters in figure caption

BASE = 'Aug_2019_SAT'

t0 = time.time()

def readtxt(fn):
 f = open(fn)
 linelist = f.readlines()
 f.close()
# L = len(lines)
 return linelist
  

def getfile(siteID):
# logfile = './log.txt'
 IDstr = '%06d'%siteID
 WWWBASE = 'http://www.bom.gov.au/clim_data/cdio/metadata/pdf/siteinfo'
 filename = 'IDCJMD0040.%s.SiteInfo.pdf'%IDstr
 if os.path.isfile(filename) or os.path.isfile('./%s/%s'%(BASE,filename)):
  print 'File exists already'
  txtf = open('./%s_log/downloaded.txt'%BASE,'a') #w: write, a: append, r+: read/write, r: read
  txtf.write('%s\n'%(IDstr))
  txtf.close()
 else:
  url = '%s/%s'%(WWWBASE,filename)
#  myCmd = 'wget -a %s %s'%(logfile,url)
  myCmd = 'wget -q %s'%(url)
  os.system(myCmd)
  if not (os.path.isfile(filename) or os.path.isfile('./%s/'%BASE+filename)): #file still doesn't exist:
#   print 'Failed to download',IDstr  
   txtf = open('./%s_log/failed.txt'%BASE,'a') #w: write, a: append, r+: read/write, r: read
   txtf.write('%s\n'%(IDstr))
   txtf.close()

fn = './AUS_SATlist.txt' #gen_temp_list.py
filecontent = readtxt(fn)

IDlist = []
for IDstr in filecontent:
 IDlist.append(np.int(IDstr))

#erase data in logfiles:
#txtf = open('./%s_log/downloaded.txt'%BASE,'w') #w: write, a: append, r+: read/write, r: read
#txtf.close()
#txtf = open('./%s_log/failed.txt'%BASE,'w') #w: write, a: append, r+: read/write, r: read
#txtf.close()

count=1
for ID in IDlist: #[0:12]:
 tend = time.time()-t0
 print '%d. %d: t = %2.4f'%(count,ID,tend)
 #download meta file:
 getfile(ID)
 count+=1
# getfile(tstr,'min',remote)


tend = time.time()-t0
print 'Time elapsed = %2.4f seconds'%tend
