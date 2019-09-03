#!/usr/bin/python
#Python 2.7.16
#JD Vlok 2019-09-03 jdvlok@gmail.com
# 1. 2019-09-03: shelter_txt2npz.py: read shelter data extracted from BoM Observation Practices
#(http://www.bom.gov.au/climate/data/acorn-sat/documents/ACORN-SAT_Observation_practices_WEB.pdf)
#and store as array of objects. (Shelter data extracted using: pdftotext -f 17 -l 19 (p. 11 - 13).)

from __future__ import division
import numpy as np
import time

t0 = time.time()

class shelter_record:
 def __init__(self,ID):
  self.ID = ID #station ID number
  self.name = None #station name
  self.L_start = None #Large Stevenson screen start date
  self.L_end = None #Large Stevenson screen end date
  self.S_start = None #Small Stevenson screen start date
  self.S_end = None #Small Stevenson screen end date

def readtxt(fn):
 f = open(fn)
 linelist = f.readlines()
 f.close()
# L = len(lines)
 return linelist

# 1. Read txt file containing installation dates of large/small Stevenson screens:
fn = './op_table5.txt' #http://www.bom.gov.au/climate/data/acorn-sat/documents/ACORN-SAT_Observation_practices_WEB.pdf 
file_content = readtxt(fn)
file_content = np.delete(file_content,[0,1]) #remove first two lines
rXvec = []
for line in file_content:
 l = line.split()
 rX = shelter_record(np.int(l[-5]))
 rX.name = ' '.join([str(x) for x in l[0:-5]]).title()
 rX.L_start = l[-4]
 rX.L_end = l[-3]
 rX.S_start = l[-2]
 rX.S_end = l[-1]
 rXvec.append(rX)

npzfile = './stevenson_dates.npz'
np.savez_compressed(npzfile,v1=rXvec)
print 'Wrote %d records to %s'%(len(rXvec),npzfile)

#write objects out again in text file:
txtf = open('./stevenson_dates.txt','w') #w: write, a: append, r+: read/write, r: read
for rX in rXvec:
 name = rX.name
 ID = '%06d'%rX.ID
 L_start = '%11s'%(rX.L_start)
 L_end = '%11s'%(rX.L_end)
 S_start = '%11s'%(rX.S_start)
 S_end = '%11s'%(rX.S_end)
 txtf.write('%-30s %s %s %s %s %s\n'%(name,ID,L_start,L_end,S_start,S_end))

txtf.write(__file__) #write name of python script to file
txtf.close()

tend = time.time()-t0
print 'Time elapsed = %2.4f seconds'%tend

