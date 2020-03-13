# Data Analyse Sterrenkunde Practicum
In de afgelopen paar maanden in er waargenomen als onderdeel van Sterrenkunde 1. Hier wordt de sterdichtheid in M81 onderzocht, 
en hiermee wordt een beeld gevormd van de sterrenhemel vanuit M81.

## Installation
Clone the repository, and install the required depedencies. 
```cmd
git clone https://github.com/Vector04/Sterrenkunde-analyse.git
```
Make sure you are in the right directory:
```
pip install -r requirements.txt
``` 

The Images was first analysed using [SAOImageDS9](http://ds9.si.edu/site/Home.html), the image was exported to a `.nrrd` format, which python can interpret with de the help of `pynrrd`. All the analysis was done in `analysis.py`. If you wish to export the results of the simultion, set `logging = True`. All of the print statements will be captured and written to `log.txt`. Additionaly, I used an external libary to convert the temperature of a black body to a color. The libary used is called [Colorpy](http://markkness.net/colorpy/ColorPy.html).

Have fun!
