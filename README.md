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
1. Download the station list from http://www.bom.gov.au/climate/cdo/about/sitedata.shtml
(direct link: ftp://ftp.bom.gov.au/anon2/home/ncc/metadata/sitelists/stations.zip)

2. Unzip stations.zip, which contains stations.txt
