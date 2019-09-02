#!/usr/bin/python
#Python 2.7.16
#JD Vlok 2019-08-23 jdvlok@gmail.com
# 1. 2019-08-23: postcode_csv2npz.py: read australian_postcodes.csv and save in .npz as object vector

#This .py program extracts Australian post code data from the post code CSV file obtained from
#https://www.matthewproctor.com/australian_postcodes, and saves the data as objects in a .npz file

from __future__ import division
import numpy as np
import time

t0 = time.time()

class postloc:
 def __init__(self,postcode):
  self.postcode = postcode #The postcode in numerical format - 0000 to 9999
  self.locality = None #The locality of the postcode - typically the city/suburb or postal distribution centre
  self.state = None #The Australian state in which the locality is situated
  self.lats = None #The latitude of the locality - defaults to 0 when not available
  self.longs = None #The longitude of the locality - defaults to 0 when not available
  self.id = None #primary key from source database
  self.dc = None #The Australia Post distribution Centre servicing this postcode
  self.type = None #type of locality, e.g. delivery area, post office or a "Large Volume Recipient" such as a GPO

class uniq_codes:
 def __init__(self,postcode):
  self.postcode = postcode #The postcode in numerical format - 0000 to 9999
  self.state = None #The Australian state in which the locality is situated
  self.lats = None #The latitude of the locality - defaults to 0 when not available
  self.longs = None #The longitude of the locality - defaults to 0 when not available
  self.dc = None #The Australia Post distribution Centre servicing this postcode
 
def readtxt(fn):
 f = open(fn)
 linelist = f.readlines()
 f.close()
# L = len(lines)
 return linelist

# 1. Read postcode CSV file:
fn = './australian_postcodes.csv' #https://www.matthewproctor.com/australian_postcodes
file_content = readtxt(fn)
file_content = np.delete(file_content,0) #remove first line
pXvec = []
for line in file_content:
 l = line.split(',')
 pX = postloc(np.int(l[0]))
 pX.locality = l[1]
 pX.state = l[2]
 pX.lats = l[4]
 pX.longs = l[3]
 pX.id = np.int(l[5])
 pX.dc = l[6]
 pX.type = l[7] 
 pXvec.append(pX)

#only retain unique postcodes:
ll_exist=[] #vector containing unique set of lats and longs
uXvec=[]
for pX in pXvec:
 llstring = pX.lats+pX.longs
 if llstring not in ll_exist:
  ll_exist.append(llstring)
  uX = uniq_codes(pX.postcode)
  uX.state = pX.state 
  uX.lats = pX.lats
  uX.longs = pX.longs
  uX.dc = pX.dc
  uXvec.append(uX)

npzfile = './postcodes.npz'
np.savez_compressed(npzfile,v1=pXvec,v2=uXvec)
print 'Wrote %d (total), %d (unique) postcodes to %s'%(len(pXvec),len(uXvec),npzfile)

tend = time.time()-t0
print 'Time elapsed = %2.4f seconds'%tend

