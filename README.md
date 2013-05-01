Binify D3 Example
==============

A demo of using binify to create a hexagon-bin map in d3

# Objective
Kevin Schaul has released an exciting new command-line tool called [binify](https://github.com/kevinschaul/binify) that clusters
("bins") points on a map into hexagonal tiles. See the [introductory blog post](http://www.kevinschaul.com/2013/04/18/introducing-binify/).

Binify operates on .shp files, which can be a bit difficult to work with for those of us who aren't GIS pros. The goal
of this demo is to take a simple csv file of about 2,000 coordinates and output a dynamic map using
[d3js](http://d3js.org/) and [topojson](https://github.com/mbostock/topojson), both courtesy of the
beautiful mind of Mike Bostock.

# Sample data
I downloaded about 2,000 addresses from a Craigslist-like website and converted them to coordinates with [geopy](https://code.google.com/p/geopy/).

# Setup

It's recommended you first create and activate a virtualenv with:

    virtualenv virt
    source virt/bin/activate

Whether or not you use virtualenv:

    pip install -r requirements.txt

You also need to install [ogr2ogr](http://www.gdal.org/ogr2ogr.html) and [topojson](https://github.com/mbostock/topojson) 
for working with the shapefiles.

# Conversions
## CSV -> SHP

Binify takes as input a .shp file, a [format developed by ESRI](http://en.wikipedia.org/wiki/Shapefile) for geospatial data.
Specifically, it needs a "point shapefile" that contains a layer of individual coordinates. (Most .shp files you're 
likely to encounter consist of a lot of polygons marking territorial boundaries and so forth.) We can make a .shp file
from a list of raw coordinates with the [pyshp](https://code.google.com/p/pyshp/) library. The ```shpify.py``` script 
will take care of this:

	./script/shpify.py
	
If you look at the source, you'll see this is a very simple process of loading the coordinates from ```coordinates.csv```
and writing them to a shapefile, same as you might to when creating a new .csv file in Python. 

This script should place a file called ```output.shp``` in the shapefiles directory. Pyshp also creates
the companion files ```output.dbf``` and ```output.shx```. We also need a projection file, ```output.prj```,
so this script manually creates one.

Load these files into an ArcGIS program such as [Quantum GIS](http://www.qgis.org/) and you'll see a nice collection of points:

![Alt text](/screenshots/dots.png)

## SHP -> Binned SHP

Here is where binify comes in. Per the documentation, we simply feed it our point shapefile with a few arguments.

First, we want to give it enough hexagons to achieve the granularity we want. 120 hexagons across sounds like a good starting target.

Because these sample coordinates span the United States, we will expect many of the hexagons to encompass
0 points. We can greatly reduce the filesize by including the -e argument, which prevents binify from 
writing empty polygons.

	binify -n=120 -e shapefiles/original.shp shapefiles/binned.shp

This may take a few minutes to run. When finished, you'll have a new set of files named ```binary.shp```
and so forth.

Load those files into QGIS and, like magic, we've got hexagons:

![Alt text](/screenshots/hexagons.png)

## Binned SHP -> GeoJSON -> topoJSON

The mechanics of how to build GeoJSON and topoJSON files are well-documented--see this [Stack Overflow
Question and the answer from Bostock](http://stackoverflow.com/questions/14565963/topojson-for-congressional-districts),
 for example--so we'll skip to the CLI commands:
 
	ogr2ogr -f GeoJSON binned.json shapefiles/binned.shp
	
Make sure to use the ```-p``` flag with the next line to preserve the ```COUNT``` property:
	
	topojson -s 7e-9 -p -o coordinates.json -- binned.json
	
This reduces the 1.9MB .shp file to an 88KB .json file.

## Mapping
We can reuse 90 percent of the code in the d3 [choropleth map example](http://bl.ocks.org/mbostock/4060606),
which serves as a nice introduction to topoJSON mapping. 

As Schaul notes in his introductory blog post, how you divide your data into color bins is critically important to how
viewers interpret the information. In this case, I was lazy and simply colored all the hexagons red and then dimmed them
according to the COUNT value (specifically, the square root of the ratio of the value to the maximum value on the map).

And there you have it. If the hexagons look a little too big, just rerun the ```binify``` command with a 
larger value for ```n```. You can see a [live example here](http://bl.ocks.org/wilson428/5493576). 