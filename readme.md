# Data Analyse Sterrenkunde Practicum
In de afgelopen paar maanden in er waargenomen als onderdeel van Sterrenkunde 1. Hier wordt de sterdichtheid in M81 onderzocht, 
en hiermee wordt een beeld gevormd van de sterrenhemel vanuit M81.

## Getting started
First, clone the repository (`git clone https://github.com/Vector04/Sterrenkunde-analyse.git`). Then, intall the required depecencies. (`pip install -r requirements.txt`) The dependencies include:
- numpy (Fast array processing)
- matplotlib (Imaging)
- pynrrd (nrrd array file processing)

The Images was first analysed using [SAOImageDS9](http://ds9.si.edu/site/Home.html), the image was exported to a nrrd format, which python can interpret with de the help of pynrrd. All the analysis was done in `analysis.py`. If you wish to export the results of the simultion, set `loggin = True`. All of the print statements will be captured and written to `log.txt`.
Have fun!
