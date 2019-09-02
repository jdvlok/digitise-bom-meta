#!/usr/bin/python
#Python 2.7.16
# JD Vlok 2019-07-18
# 2019-04-16: get_all_ACORN2.py: Download all ACORN data, hq: csv
# 2019-07-18: scrape_meta.py: Download all weather station meta data (pdf files)

# 2019-08-30: gen_temp_list.py: Download temperature alpha files (using wget) and generate unified list from:
#http://www.bom.gov.au/climate/data/lists_by_element/alphaAUS_36.txt #Tmax monthly
#http://www.bom.gov.au/climate/data/lists_by_element/alphaAUS_122.txt #Tmax daily
#http://www.bom.gov.au/climate/data/lists_by_element/alphaAUS_38.txt #Tmin monthly
#http://www.bom.gov.au/climate/data/lists_by_element/alphaAUS_123.txt #Tmin daily

from __future__ import division
import numpy as np
#import pylab as pl
import os
import time
#import urllib2
#import csv
#from mat:lotlib import rc #to use greek letters in figure caption

t0 = time.time()
WWWbase = 'http://www.bom.gov.au/climate/data/lists_by_element'

def getfile(typenr):
 filename = 'alphaAUS_%d.txt'%typenr
 if os.path.isfile(filename):
  os.remove(filename)
 url = '%s/%s'%(WWWbase,filename)
 myCmd = 'wget -q %s'%(url) #q: quiet
 os.system(myCmd)
 return filename

def readtxt(fn):
 f = open(fn)
 linelist = f.readlines()
 f.close()
# L = len(lines)
 return linelist

def extractIDs(filecontent):
#extract list of station IDs, stop at first "\r\n" - as this is the end of the list
 IDvec = []
 l=0
 found_n = False
 Lx = len(filecontent)
 while (l<Lx) and (not found_n):
  found_n = (filecontent[l] == '\r\n')
#  print found_n
  if not found_n:
   line = filecontent[l].split()
#   print line
   ID = line[0]
   if ID.isdigit():
    IDvec.append(np.int(ID))
   l+=1
 if found_n: #read "x stations" in alphafile after station listed
  L_reported = np.int(filecontent[l+1].split()[0])
  print 'Number of stations extracted = %d (%d reported in file)'%(len(IDvec),L_reported)
 return IDvec, L_reported

#download lists of SAT-measuring stations from BoM website:
fn1 = getfile(36)
fn2 = getfile(122)
fn3 = getfile(38)
fn4 = getfile(123)

A = readtxt(fn1)
B = readtxt(fn2)
C = readtxt(fn3)
D = readtxt(fn4)

listA,a = extractIDs(A)
listB,b = extractIDs(B)
listC,c = extractIDs(C)
listD,d = extractIDs(D)

concatlist = listA + listB + listC + listD
t = a+b+c+d #total number of stations extracted (including multiples)
sl = len(concatlist)
uniq_list = np.unique(concatlist)

print 'Concatenated list: %d elements (%d: sum of reported numbers)'%(sl,t)
print 'Unique elements = %d'%len(uniq_list)

#write uniq_list to file (to be used to drive .pdf extraction):
fn = './AUS_SATlist.txt'
txtf = open(fn,'w') #w: write, a: append, r+: read/write, r: read
for ID in uniq_list:
 txtf.write('%d\n'%(ID))
txtf.close()

tend = time.time()-t0
print 'Time elapsed = %2.4f seconds'%tend
