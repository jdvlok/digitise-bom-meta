#!/usr/bin/python
#JD Vlok 2019-09-16
#interpret_classes.py: Class definitions to interpret text files as equipment entries 

import numpy as np

class meta_record:
 def __init__(self,date):
  self.date = date #'05/DEC/2012'
  self.action = None #'REPLACE'
  self.equipment = None #'Thermometer,', 'Mercury,'
#  self.function = None #'Max'
  self.make = None #'WIKA'
  self.serial = None #'32192'
  self.note = None #'Surface', 'Observations'?

class processed_record:
 def __init__(self,start_date):
  self.start_date = start_date
  self.end_date = None
  self.lats = -999
  self.longs = -999
  self.equipment = None #MiG, AiG
  self.type = None #'WIKA (SN)'
  self.shelter = 'X'
  self.CLcode = None #climatelab code

class siteloc:
 def __init__(self,date):
  self.date = date
  self.lats = None
  self.longs = None

#Large/Small Stevenson screen class (AUSdata/meta2019/ACORN/shelter_txt2npz.py)
class shelter_record: 
 def __init__(self,ID):
  self.ID = ID #station ID number
  self.name = None #station name
  self.L_start = None #Large Stevenson screen start date
  self.L_end = None #Large Stevenson screen end date
  self.S_start = None #Small Stevenson screen start date
  self.S_end = None #Small Stevenson screen end date

#postcode class (AUSdata/meta2019/postcodes/postcode_csv2npz.py):
class postloc: #pXvec
#See: https://www.matthewproctor.com/australian_postcodes
 def __init__(self,postcode):
  self.postcode = postcode #The postcode in numerical format - 0000 to 9999
  self.locality = None #The locality of the postcode - typically the city/suburb or postal distribution centre
  self.state = None #The Australian state in which the locality is situated
  self.lats = None #The latitude of the locality - defaults to 0 when not available
  self.longs = None #The longitude of the locality - defaults to 0 when not available
  self.id = None #primary key from source database
  self.dc = None #The Australia Post distribution Centre servicing this postcode
  self.type = None #type of locality, e.g. delivery area, post office or a "Large Volume Recipient" such as a GPO

class uniq_codes: #uXvec
 def __init__(self,postcode):
  self.postcode = postcode #The postcode in numerical format - 0000 to 9999
  self.state = None #The Australian state in which the locality is situated
  self.lats = None #The latitude of the locality - defaults to 0 when not available
  self.longs = None #The longitude of the locality - defaults to 0 when not available
  self.dc = None #The Australia Post distribution Centre servicing this postcode
