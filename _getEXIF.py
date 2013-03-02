#!/usr/bin/python
#

# Copyright (C) 2012 Michael Spreitzenbarth, Sven Schmitt
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import subprocess
import datetime
import sys
import hashlib

import _adel_log
import _exif

def get_exif_information(backup_dir, outputFile):
    picture_position_list = []
    picture_dir = backup_dir + "/pictures/"
    listing = os.listdir(picture_dir)
    for file in listing:
        latitude = ""
        longitude = ""
        readtime = ""
        try:
            f = open(picture_dir + file, 'rb')
            tags = _exif.process_file(f)
            for tag in tags.keys():
                if tag in ('GPS GPSLatitude'):
                    lat = str(tags[tag])
                    lat1 = lat.split(",")[2].split("]")[0].split(" ")[-1]
                    if "/" in lat1:
                        lat1_1 = float(lat1.split("/")[0])
                        lat1_2 = float(lat1.split("/")[1])
                        lat1 = lat1_1 / lat1_2
                    else:
                        lat1 = float(lat1)
                    lat2 = float(lat.split(",")[1].split(" ")[-1])
                    lat3 = float(lat.split(",")[0].split("[")[1])
                    latitude = ((((lat1 / 60) + lat2) / 60) + lat3)
                    
                if tag in ('GPS GPSLongitude'):
                    long = str(tags[tag])
                    long1 = long.split(",")[2].split("]")[0].split(" ")[-1]
                    if "/" in long1:
                        long1_1 = float(long1.split("/")[0])
                        long1_2 = float(long1.split("/")[1])
                        long1 = long1_1 / long1_2
                    else:
                        long1 = float(long1)
                    long2 = float(long.split(",")[1].split(" ")[-1])
                    long3 = float(long.split(",")[0].split("[")[1])
                    longitude = ((((long1 / 60) + long2) / 60) + long3)
                if tag in ('EXIF DateTimeOriginal'):
                    readtime = str(tags[tag])
                    readtime = readtime.split(":")[1] + "/" + readtime.split(":")[2].split(" ")[0] + "/" + readtime.split(":")[0].split("0")[1] + " " + readtime.split(" ")[1]
        except:
            continue
        
        if ((latitude != "") & (longitude != "")):
            picture_position_list.append([file, str(latitude), str(longitude), "500", readtime])
            outputFile.write('%25s %7d %5d %10s %10s %s \n' % ("JPEG", 500, 0, latitude, longitude, str(readtime)))
    return picture_position_list
