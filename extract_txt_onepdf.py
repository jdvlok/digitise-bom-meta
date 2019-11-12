#!/usr/bin/python
#JD Vlok 2019-08-05 jdvlok@gmail.com
#Python 2.7.16
# 1. 2019-08-29: extract_pdf3.py: code written to execute as script within other code
# 2. 2019-08-30: extract_txt_onepdf.py: extract text (meta data) using pdftotext from one pdf file and save as .txt file

from __future__ import division
import pylab as pl
import numpy as np
import time
import PyPDF2
import os
from datetime import datetime as dt
import sys

def readtxt(fn_):
 f = open(fn_)
 linelist = f.readlines()
 f.close()
# L = len(lines)
 return linelist

def identify_line_nr(search_txt_, file_content_):
#find index (line number) of "search_txt_" in "file_content_"
 Lx = len(file_content_) #number of lines in file
 l = 0 #line nr
 found_txt = False
 while (not found_txt) and (l<Lx):
  found_txt = (search_txt_ in file_content_[l])
  l+=1

 if found_txt:
#  print 'Found max on line %d:'%l #number from 1
  lmark_ = l-1 #line on which search_txt_ was found, numbered from 0
#  print file_content_[lmark_]
  #find next newline character ("\n") in file:
 else:
#  print 'Could not find \'%s\''%(search_txt_)
  lmark_ = np.nan
 return lmark_

def meta_extract(search_txt, file_content_):
 nr_words = len(search_txt.split()) #number of words in search string
 ln_ = identify_line_nr(search_txt, file_content_)
# print '%s found on line %d'%(search_txt, ln)
 line = file_content_[ln_]
# print line
 datastr = line.split()[nr_words::]
 rtxt = ' '.join([str(x) for x in datastr])
 return rtxt

def load_page(page_nr_,fn_,txtout_,opt):
 cmd = 'pdftotext %s -f %d -l %d -x 0 -y 0 -W 592 -H 778 %s %s'%(opt, page_nr_,page_nr_,fn_,txtout_)
 #extract first page of basic climatological station metadata:
 #within frame topleft: (0,0) --> (592,778) #width, height
 #man pdftotext:
 #-f number: Specifies the first page to convert.
 #-l number: Specifies the last page to convert.
 #-r number: Specifies the resolution, in DPI.  The default is 72 DPI.
 #-x number: Specifies the x-coordinate of the crop area top left corner
 #-y number: Specifies the y-coordinate of the crop area top left corner
 #-W number: Specifies the width of crop area in pixels (default is 0)
 #-H number: Specifies the height of crop area in pixels (default is 0)
 os.system(cmd) #extract one page from file fn and save in txtout_
 file_content_ = readtxt(txtout_) #read station data from temp.txt
 return file_content_ 

def date_format(line_): #check if line_ possibly contains a date
 if (line_ == '\n') or (line_ == '\f'): #new line or form feed (aka \x0c) --> check new page
  rval = False
 else:
#  print line_
  str1 = line_.split()[0] #'21/AUG/1987'
  if len(str1) < 11: #date must be 11 characters long
   rval = False
  else:
   rval = (str1[2] == '/') and (str1[6] == '/') #if line contains date --/---/----
 return rval

def extract_text_block(search_string_, search_string2_, page_nr_vec_, fn_, txtout_):
 txt_block = []
 title_found = False
 unwanted_string = 'No Electronic History'
 pc=0
 print 'Extracting:', search_string_
 while not title_found:
  page_nr = page_nr_vec_[pc]
  file_content = load_page(page_nr, fn_, txtout_,'-layout') #changed from '' to '-layout'
  Lx = len(file_content) #number of lines in file
  line_nr = identify_line_nr(search_string_, file_content)
  if np.isnan(line_nr): #i.e. search_string_ not in file
   print 'String %s not found on p. %d'%(search_string_, page_nr)
   pc+=1 #step to next page
  else:
   title_found = True
   line = file_content[line_nr]
   if unwanted_string in line:
    print unwanted_string
    txt_block.append(unwanted_string) #no metadata available
   else:
    record_ended = False
    ln=line_nr
    while (not record_ended) and (ln<Lx):
     ln+=1
     line = file_content[ln]
     if (line == '\n') or (line == '\f'): #new line or form feed (aka \x0c) --> check new page
      pc+=1
      page_nr = page_nr_vec_[pc]
      file_content = load_page(page_nr, fn_, txtout_, '-layout') #changed from '' to '-layout'
      Lx = len(file_content) #number of lines in file
      ln = identify_line_nr(search_string2_, file_content)
      if np.isnan(ln):
       record_ended = True #if next page does not contain "...(Continued)" end the record
#     elif not date_format(file_content[ln+1]): #page contains "Continued" but first line thereafter is not a date
#      record_ended = True #if next page does not contain "...(Continued)" end the record
     elif date_format(line):
      txt_block.append(line)
     else: #line does not contain a date, and is not a new line, i.e. start of new weather element
      record_ended = True
# for txtl in txt_block:
#  print txtl
# print  
 return txt_block

#print '%03d/%03d: %s'%(ln,Lx,line)

def find_pages(search_string_,nr_pages_,fn_,txtout_):
#Find pages containing e.g. "Station Equipment History":
 page_nr_vec_ = []
 page_nr = 2 #start searching on p.2 (p.1 already processed)
 while (page_nr <= nr_pages_):
  file_content = load_page(page_nr,fn_,txtout_,'-layout') #changed from '' to '-layout'
  nr_lines = len(file_content)
  line_nr = 0
  found_string = False
  while (not found_string) and (line_nr < nr_lines):
   found_string = (search_string_ in file_content[line_nr])
   line_nr+=1
  if found_string:
   page_nr_vec_.append(page_nr)
  page_nr += 1
 return page_nr_vec_

def write_block_to_file(txtf_, txt_block):
 unwanted_string = 'No Electronic History'
 if txt_block[0] == unwanted_string:
  txtf_.write(' (%s)\n'%unwanted_string)
 else:
  txtf_.write('\n')
  for line in txt_block:
   txtf_.write(line)


def pdf2txt(siteID,fn):
 print 'Reading', fn

 pdfFileObj = open(fn, 'rb')
 print 'Reading:', fn
 pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
 nr_pages = pdfReader.numPages #19
 print 'Number of pages:',nr_pages

 txtout = './temp.txt'
 #cmd = 'pdftotext -f 1 -l 1 -x 0 -y 0 -W 592 -H 778 %s %s'%(fn,txtout)
 file_content = load_page(1,fn,txtout,'')

 comp_date = meta_extract('Metadata compiled:', file_content)
 sXname = meta_extract('Station:', file_content)
 sX_ID = meta_extract('Bureau of Meteorology station number:', file_content)
 state = meta_extract('State:', file_content)
 startY = meta_extract('Year opened:', file_content)
 cstat = meta_extract('Status:', file_content)

 #extract lat and lon:
 ln = identify_line_nr('Latitude', file_content)
 if np.isfinite(ln):
  lat = file_content[ln+1].split()[-1] #latitude should be last word of line following 'Latitude'
 else:
  print 'Latitude not specified'

 ln = identify_line_nr('Longitude', file_content)
 if np.isfinite(ln):
  lon = file_content[ln+1].split()[-1] #longitude should be last word of line following 'Longitude'
 else:
  print 'Longitude not specified'

 if siteID != np.int(sX_ID):
  print 'Station number mismatch!'

 search_string = 'Station Equipment History'
 page_nr_vec = find_pages(search_string,nr_pages,fn,txtout)
 print page_nr_vec

 search_string2 = 'Equipment Install/Remove(Continued)'
 text_identifier1 = 'Minimum Temperature'
 block1 = extract_text_block(text_identifier1, search_string2, page_nr_vec, fn, txtout)

 text_identifier2 = 'Maximum Temperature'
 block2 = extract_text_block(text_identifier2, search_string2, page_nr_vec, fn, txtout)

 text_identifier3 = 'Air Temperature'
 block3 = extract_text_block(text_identifier3, search_string2, page_nr_vec, fn, txtout)

 search_string4 = 'Station Detail Changes'
 print 'Extracting:', search_string4
 page_nr_vec = find_pages(search_string4,nr_pages,fn,txtout)
 search_string4_2 = 'Station Detail Changes(Continued)'

 block4 = []
 for page_nr in page_nr_vec:
  file_content = load_page(page_nr, fn, txtout, '-layout')
  Lx = len(file_content) #number of lines in file
  line_nr = identify_line_nr(search_string4, file_content) #will identify both "Station Detail Changes" and "...(Continued)"
  if np.isnan(line_nr): #this should not happen, as only pages containing search_string4 have already been identified
   print 'Error: %s not found on p. %d of %s'%(search_string4,page_nr,fn)
  else:
   line = file_content[line_nr]
   record_ended = False
   ln = line_nr
   while (not record_ended) and (ln<Lx):
    ln+=1
    line = file_content[ln]
#    print line
    if date_format(line):
#     linesplit=line.split() #date and description separated by 3 whitespaces; for QA tests
#     s0 = linesplit[0]
     s0 = ' '.join([str(x) for x in line.split()]) #remaining description
     block4.append(s0+'\n')
   #  block4.append(line) #re-activate this line after QA, and comment out QA code above
    elif line[0:12]=='            ': #i.e. no date, but description flowing from previous line
     surv_str = ' '.join([str(x) for x in line.split()]) #remaining description
     r_str = block4[-1].strip('\n')+' '+surv_str+'\n' #add overflow text to last entry in block4
     block4[-1] = r_str #replace last entry in block4
    else: #line does not contain a date, is not a new line, and does not contain overflow text, i.e. start of new weather element
     record_ended = True

 clock_str = dt.now().strftime("%Y-%m-%d %H:%M:%S")

 meta_out_txt = './Aug2019_SAT_meta/meta_%06d.txt'%siteID
 txtf = open(meta_out_txt,'w') #w: write, a: append, r+: read/write, r: read
 txtf.write('%s ~ %s\n'%(__file__,clock_str)) #write name of python script to file
 txtf.write('Compiled: %s\n'%(comp_date))
 txtf.write('Station:  %s\n'%(sXname))
 txtf.write('ID:       %s\n'%(sX_ID))
 txtf.write('State:    %s\n'%(state))
 txtf.write('Lat:      %s\n'%(lat))
 txtf.write('Lon:      %s\n'%(lon))
 txtf.write('Opened:   %s\n'%(startY))
 txtf.write('Status:   %s\n'%(cstat))

 txtf.write('\n%s'%text_identifier1)
 write_block_to_file(txtf, block1)
 
 txtf.write('\n%s'%text_identifier2)
 write_block_to_file(txtf, block2)
 
 txtf.write('\n%s'%text_identifier3)
 write_block_to_file(txtf, block3)

 txtf.write('\n%s'%search_string4)
 write_block_to_file(txtf, block4)

 txtf.write('\n')
 
 txtf.close()
 print 'Wrote filtered metadata to', meta_out_txt


if __name__ == '__main__':
##command line arguments:
 total = len(sys.argv)
 if total != 2:
  print 'Usage: extract_txt_onepdf.py siteID'
  sys.exit()

## Get the arguments list
 cmdargs = str(sys.argv)
 #print 'args =', cmdargs
#print 'args =', cmdargs
 stationID = int(sys.argv[1])
 HOME = './Aug_2019_SAT'
 pdf_fn = '%s/IDCJMD0040.%06d.SiteInfo.pdf'%(HOME,stationID)
 pdf2txt(stationID,pdf_fn)
 
