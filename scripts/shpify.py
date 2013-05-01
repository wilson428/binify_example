#!/usr/bin/env python

import shapefile
import csv

w = shapefile.Writer(shapefile.POINT)
w.field('ADDRESS')
w.field('TYPE','C','40')

# make .shp, .dbf, and .shx files
with open('data/coordinates.csv', 'rU') as csvfile:
    reader = csv.reader(csvfile)
    point = 0
    for row in reader:
        w.point(float(row[0]), float(row[1]))
        w.record("p%d" % point, "Point")
        point += 1

w.save("shapefiles/original")

# add .prj fiile

prj = open("shapefiles/original.prj", "w")
epsg = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
prj.write(epsg)
prj.close()
