#2017-03-15: stationsdef2.py: Addition to class structure:
# self.alt: altitude value
# self.dateseq_MA: date sequence (monthly) for moving average (MA)
# self.valseq_MA: MA temperature sequence (for last 12 months)
# self.yearseq: date sequece containing year numbers for annual mean temperature sequence
# self.annualmeanT: annual mean temperature sequence

#2017-05-05: stationsdef3.py
#self.state added which indicates the state in which the station lies

#2018-01-15: stationsdef4.py
#expand to include Tmin and Tmax in one datafile

#2019-08-26: stationsdef5.py
#self.postcode added to associate closest postcode location with weather station using Haversine distance

# year range (self.yearseq), and annual averages (self.Tyear)
import numpy as np
import calendar
 
def datestring(yearval):
 yearint = int(yearval)
 yearfl = yearval - yearint
 monthnr = round((12*yearfl)+0.5)
 monthname = calendar.month_abbr[int(monthnr)]
# rstr = '%s %d'%(monthname,yearint)
 return (yearint,monthname) #rstr


class station_data:
 def __init__(self):
  self.dateseq = [] #
  self.valseq = [] #
#  self.nanthreshold = None
  self.valseq_interp = [] 
  self.index_interp = []
  self.dateseq_MA = [] #
  self.valseq_MA = [] #
  self.yearseq = [] #
  self.annualmeanT = [] #
  self.startM = None ##
  self.startY = None ##
  self.endM = None ##
  self.endY = None ##
  self.duration = None
  self.percentage = None

 def true_period(self): #calculate non-NaN start/end dates
  idx = np.isfinite(self.valseq)
  if len(idx) > 0:
   finite_datevec = self.dateseq
#   ylo_str, yhi_str = datestring(finite_datevec[0]), datestring(finite_datevec[-1])
   ylo_Y, ylo_M = datestring(finite_datevec[0])
   yhi_Y, yhi_M = datestring(finite_datevec[-1])
  else:
   ylo_Y, ylo_M = '-999','NA' 
   yhi_Y, yhi_M = '-999','NA'
  return (ylo_Y, ylo_M, yhi_Y, yhi_M)
#  return (ylo_str, yhi_str)
 
 def valid_samples(self): #calculate number of samples present
  N=np.count_nonzero(np.isfinite(self.valseq))
  return N
 
 def start_end_dates(self): #sX.max.start_end_dates
  if np.isnan(self.valseq[0]):
   print 'Warning: Index value 0 is NaN'
  if np.isnan(self.valseq[-1]):
   print 'Warning: Index value -1 is NaN'
  ylo_str, yhi_str = datestring(self.dateseq[0]), datestring(self.dateseq[-1])
  return (ylo_str, yhi_str)

class station:
 def __init__(self,stationID):
  self.ID = stationID
  self.name = None
  self.state = None
  self.lats = None
  self.longs = None
  self.gis_alt = None #Google ALT data
  self.bom_alt = None #BOM data given on each station webpage
  self.aws = None
  self.nearest_neighbours = []
  self.max = station_data()
  self.min = station_data()
  self.postcode = None

#functions must be updated to deal with min and max subclasses:
 def datemax(self):
#  rval = -999
#  if tseq != []:
  max1 = np.max(self.max.dateseq)
  max2 = np.max(self.min.dateseq)
  rval = np.max([max1,max2])
  return rval

 def datemin(self):
  return np.min(self.max.dateseq)
 
 def valmin(self):
  return np.nanmin(self.valseq)
 
 def valmax(self):
  return np.nanmax(self.valseq)

 def validcount(self):
  v = np.count_nonzero(np.isfinite(self.max.valseq))
#  v = 0
#  for sampnr in np.arange(0,len(self.max.dateseq),1):
#   if not np.isnan(self.max.valseq[sampnr]):
#    v+=1
  return v  
 
 def nancount(self):
  v = np.count_nonzero(np.isnan(self.max.valseq))
#  v = 0
#  for sampnr in np.arange(0,len(self.max.dateseq),1):
#   if np.isnan(self.max.valseq[sampnr]):
#    v+=1
  return v  

 def truepercentage(self):
  return 100.0*self.validcount()/float(len(self.max.dateseq))
  #return 100.0 #*self.validcount()/float(len(self.dateseq))
 
 def maxnanrun(self):
  Lx = len(self.max.dateseq)
#  idx = [] #array containing index values of interpolated samples
  nanbinvec = np.zeros(Lx) #"binary" vector: 1 if index is NaN, else: 0
  for l in np.arange(0,Lx,1):
   if np.isnan(self.max.valseq[l]): #if y[l] is a valid number
#    idx.append(l)
    nanbinvec[l] = 1

  sumbinvec = np.copy(nanbinvec)
  #run through binvec and sum:
  for n in np.arange(0,Lx,1):
   if nanbinvec[n]==1:
    sumbinvec[n] += sumbinvec[n-1] #cummulative sum, which restarts if 0 is encountered
  
  return np.max(sumbinvec) #longest run of NaNs


