# digitise-bom-meta
Digitisation of BoM climatological metadata (temperature related)

The aim of this project is to digitise all temperature-related meta data published by the Australian Bureau of Meteorology (BoM).
Climatological station meta data containing weather station and temperature sensor meta data are published as .pdf files by the BoM, at e.g. http://www.bom.gov.au/clim_data/cdio/metadata/pdf/siteinfo/IDCJMD0040.076031.SiteInfo.pdf.


Parameters of interest include:

1. The temperature-measuring device used (e.g. Mercury thermometer, thermograph, Platinum probe)

2. The date range over which the device was used (including installation and removal dates)

3. The location (latitude and longitude coordinates) of the weather station, including any site moves


Other parameters of interest, which are currently not listed in the meta data include:

1. The screen type (Glaisher, large or small Stevenson screen, etc.) used at each weather station

2. Changes in the area surrounding each weather station (some information is given in the meta data)


The aim is to extract all relevant meta data and to create a dated list of equipment types used at each weather station.

The following procedure should be followed to extract and digitise the BoM metadata:
1. Obtain the list of stations of which the metadata should be extracted. If all weather stations are required, follow A below. If only surface air temperature (SAT) measuring stations are needed, follow B below.

A: Download the station list from http://www.bom.gov.au/climate/cdo/about/sitedata.shtml
(direct link: ftp://ftp.bom.gov.au/anon2/home/ncc/metadata/sitelists/stations.zip) and unzip stations.zip, which contains stations.txt


B. Run gen_temp_list.py to automatically 

i) download BoM station alpha files (Tmax/Tmin monthly/daily station meta data files), and 

ii) create AUS_SATlist.txt containing BoM station numbers of all surface air temperature (SAT) measuring stations


Using AUS_SATlist.txt as reference, the metadata can be extracted as follows:

1. Run download_bom_meta_files.py to download (wget) all (listed in AUS_SATlist.txt) metadata from the BoM website and copy all .pdf files to ./Aug_2019_SAT/
(Approximately 8 minutes to download 1979 .pdf files)


2. Create directory "Aug2019_SAT_meta" and run drive_extract_txt.py to extract metadata in each .pdf file.
For example IDCJMD0040.039059.SiteInfo.pdf --> meta_039059.txt
drive_extract_txt.py uses pdf2txt defined in extract_txt_onepdf.py


3. Run shelter_txt2npz.py to convert op_table5.txt (shelter data from http://www.bom.gov.au/climate/data/acorn-sat/documents/ACORN-SAT_Observation_practices_WEB.pdf) to stevenson_dates.npz


4. Run postcode_csv2npz.py to convert post code data from australian_postcodes.csv (obtained from https://www.matthewproctor.com/australian_postcodes) to postcodes.npz


5. Create directory "csvfiles" and link "stations_v9a.dat" (190 MB, containing all Australian SAT data - not available here due to size constraints) to current directory


6. Run interpret_onetxt.py to extract meta data in one .txt file into a .csv file
(i.e. process one station). This file has the following dependencies:

6.1. interpret_classes.py containing class definitions

6.2. stations_v9a.dat containing all SAT data (e.g. monthly Tmax of all Australian stations)

6.3. stationsdef5.py containing class definitions of stations_v9a.dat

6.4. stevenson_dates.npz

6.5. postcodes.npz
