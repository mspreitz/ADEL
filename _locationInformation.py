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

import struct
import time

import _adel_log
import _sqliteParser


def get_location_information_browser(backup_dir, output_file):
    # insert try - except as soon as all errors are fixed
    try:
        browser_position_list = []
        db_file_browser = backup_dir + "/CachedGeoposition.db"
        #resultList = _sqliteParser.parseDB(db_file_browser)
        '''
        for i in range(1, len(resultList)):
            lat = resultList[1][i][0]
            long = resultList[1][i][1]
            acc = resultList[1][i][3]
            readtime = resultList[1][i][7]
            readtime = time.strftime("%x %X", time.localtime(readtime/1000))
            browser_position_list.append(["Browser", str(lat), str(long), acc, str(readtime)])
        '''
    except:
        browser_position_list = []
    return browser_position_list


def get_location_information_twitter(backup_dir, output_file):
    try:
        twitterPositionList = []
        db_file_twitter = backup_dir + "/global.db"
        resultList = _sqliteParser.parseDB(db_file_twitter)
        twitter_id = resultList[1][2][2]
        db_file_twitter = backup_dir + "/" + twitter_id + ".db"
        resultList = _sqliteParser.parseDB(db_file_twitter)
        for i in range(1, len(resultList[4])):
            if str(resultList[4][i][2]) == twitter_id:
                if str(resultList[4][i][10]) != "None":
                    lat = resultList[4][i][10]
                    long = resultList[4][i][11]
                    title = resultList[4][i][3]
                    readtime = resultList[4][i][6]
                    readtime = time.strftime("%x %X", time.localtime(readtime / 1000))
                    output_file.write('%25s %7d %5d %10s %10s %s \n' % ("twitter", 100, 0, lat, long, str(readtime)))
                    twitterPositionList.append([str(title), str(lat), str(long), "100", str(readtime)])
    except:
        twitterPositionList = []
    return twitterPositionList


def get_location_information_gmaps(backup_dir, outputFile):
    try:
        gMapsPositionList = []
        db_file_gmaps = backup_dir + "/da_destination_history.db"
        resultList = _sqliteParser.parseDB(db_file_gmaps)
        # [['time', 'INTEGER'], ['dest_lat', 'INTEGER'], ['dest_lng', 'INTEGER'], ['dest_title', 'STRING'], ['dest_address', 'STRING'], ['dest_token', 'STRING'], ['source_lat', 'INTEGER'], ['source_lng', 'INTEGER'], ['day_of_week', 'INTEGER'], ['hour_of_day', 'INTEGER']]
        i = 1
        while i <= len(resultList) + 1:
            if resultList[1][i][3] == None:
                title = resultList[1][i][4]
            else:
                title = resultList[1][i][3]
            title = title.replace("\xc3\xbc", "ue") # ue
            title = title.replace("\xc3\xa4", "ae") # ae
            title = title.replace("\xc3\xb6", "oe") # oe
            title = title.replace("\xc3\x9c", "Ue") # Ue
            title = title.replace("\xc3\x84", "Ae") # Ae
            title = title.replace("\xc3\x96", "Oe") # Oe
            title = title.replace("\xc3\x9f", "ss") # ss
            lat = resultList[1][i][6]
            if "-" in str(lat):
                lat = str(lat)[0:3] + "." + str(lat)[3:]
            else:
                lat = str(lat)[0:2] + "." + str(lat)[2:]
            long = resultList[1][i][7]
            if "-" in str(long):
                long = str(long)[0:3] + "." + str(long)[3:]
            else:
                long = str(long)[0:2] + "." + str(long)[2:]
            readtime = resultList[1][i][0]
            readtime = time.strftime("%x %X", time.localtime(readtime / 1000))
            outputFile.write('%25s %7d %5d %10s %10s %s \n' % ("GMaps", 500, 0, lat, long, str(readtime)))
            gMapsPositionList.append([str(title), str(lat), str(long), "500", str(readtime)])
            i = i + 1
    except:
        gMapsPositionList = []
    return gMapsPositionList


def get_location_information_cell(backup_dir, outputFile):
    cellPositionList = []
    try:
        _adel_log.log("LocationInfo:  ----> starting to parse location information data", 0)
        cf = open(backup_dir + "/cache.cell", 'rb')
        dbVersion, dbEntriesNumber = struct.unpack('>hh', cf.read(4))
        i = 0
        while i < dbEntriesNumber:
            key = cf.read(struct.unpack('>h', cf.read(2))[0])
            (accuracy, confidence, latitude, longitude, readtime) = struct.unpack('>iiddQ', cf.read(32))
            outputFile.write('%25s %7d %5d %10f %10f %s \n' % (key, accuracy, confidence, latitude, longitude, time.strftime("%x %X %z", time.localtime(readtime / 1000))))
            cellPositionList.append([key, str(latitude), str(longitude), str(accuracy), time.strftime("%x %X", time.localtime(readtime / 1000))])
            i = i + 1
        cf.close()
    except:
        _adel_log.log("LocationInfo:  ----> no Cell cache found", 2)
    return cellPositionList


def get_location_information_wifi(backup_dir, outputFile):
    wifiPositionList = []
    try:
        cf = open(backup_dir + "/cache.wifi", 'rb')
        dbVersion, dbEntriesNumber = struct.unpack('>hh', cf.read(4))
        i = 0
        while i < dbEntriesNumber:
            key = cf.read(struct.unpack('>h', cf.read(2))[0])
            (accuracy, confidence, latitude, longitude, readtime) = struct.unpack('>iiddQ', cf.read(32))
            outputFile.write('%25s %7d %5d %10f %10f %s \n' % (key, accuracy, confidence, latitude, longitude, time.strftime("%x %X %z", time.localtime(readtime / 1000))))
            wifiPositionList.append([key, str(latitude), str(longitude), str(accuracy), time.strftime("%x %X", time.localtime(readtime / 1000))])
            i = i + 1
        cf.close()
    except:
        _adel_log.log("LocationInfo:  ----> no Wifi cache found", 2)
    return wifiPositionList


def createMap(backup_dir, cellPositionList, wifiPositionList, picturePositionList, twitterPositionList, gMapsPositionList, browserPositionList):
    backup_dir = backup_dir.split("/")[0]
    mapFile = open(backup_dir + "/map.html", "a+")
    mapFile.write('''<!DOCTYPE html>
                    <html>
                    <head>
                    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
                    <style type="text/css">
                      html { height: 100% }
                      body { height: 100%; margin: 0px; padding: 0px }
                      #map_canvas { height: 100% }
                    </style>
                    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false">
                    </script>
                    <script type="text/javascript">
                        var cellList = {};\n''')
    i = 0
    while i < len(cellPositionList):
        if cellPositionList[0][1] == "0.000000":
            i = i + 1
        else:
            title = "'Cell-ID: " + cellPositionList[i][0] + "    -> Time: " + cellPositionList[i][4] + "'"
            mapFile.write("cellList['" + str(i) + "'] = {center: new google.maps.LatLng(" + cellPositionList[i][1] + ", " + cellPositionList[i][2] + "), accuracy: " + cellPositionList[i][3] + ", title: " + title + "};\n")
            i = i + 1
    mapFile.write('''var wifiList = {};\n''')
    for j in range(0, len(wifiPositionList)):
        if wifiPositionList[j][1] == "0.000000":
            j = j + 1
        else:
            title = "'Wifi-MAC: " + wifiPositionList[j][0] + "    -> Time: " + wifiPositionList[j][4] + "'"
            mapFile.write("wifiList['" + str(j) + "'] = {center: new google.maps.LatLng(" + wifiPositionList[j][1] + ", " + wifiPositionList[j][2] + "), accuracy: " + wifiPositionList[j][3] + ", title: " + title + "};\n")
            j = j + 1
    mapFile.write('''var exifList = {};\n''')
    for k in range(0, len(picturePositionList)):
        title = "'Picture: " + picturePositionList[k][0] + "    -> Time: " + picturePositionList[k][4] + "'"
        mapFile.write("exifList['" + str(k) + "'] = {center: new google.maps.LatLng(" + picturePositionList[k][1] + ", " + picturePositionList[k][2] + "), accuracy: " + picturePositionList[k][3] + ", title: " + title + "};\n")
        k = k + 1
    mapFile.write('''var twitterList = {};\n''')
    for l in range(0, len(twitterPositionList)):
        title = "'Message: " + twitterPositionList[l][0] + "    -> Time: " + twitterPositionList[l][4] + "'"
        mapFile.write("twitterList['" + str(l) + "'] = {center: new google.maps.LatLng(" + twitterPositionList[l][1] + ", " + twitterPositionList[l][2] + "), accuracy: " + twitterPositionList[l][3] + ", title: " + title + "};\n")
        l = l + 1
    mapFile.write('''var gMapsList = {};\n''')
    for m in range(0, len(gMapsPositionList)):
        title = "'Destination: " + gMapsPositionList[m][0] + "    -> Time: " + gMapsPositionList[m][4] + "'"
        mapFile.write("gMapsList['" + str(m) + "'] = {center: new google.maps.LatLng(" + gMapsPositionList[m][1] + ", " + gMapsPositionList[m][2] + "), accuracy: " + gMapsPositionList[m][3] + ", title: " + title + "};\n")
        m = m + 1
    mapFile.write('''var browserList = {};\n''')
    for n in range(0, len(browserPositionList)):
        title = "'" + browserPositionList[n][0] + "    -> Time: " + browserPositionList[n][4] + "'"
        mapFile.write("browserList['" + str(n) + "'] = {center: new google.maps.LatLng(" + browserPositionList[n][1] + ", " + browserPositionList[n][2] + "), accuracy: " + browserPositionList[n][3] + ", title: " + title + "};\n")
        n = n + 1
    mapFile.write('''function initialize() {
                            var mapOptions = {zoom: 7, center: new google.maps.LatLng(51.163375, 10.447683), mapTypeId: google.maps.MapTypeId.ROADMAP};
                            var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
                            for (var cell in cellList) {
                                var accuracy = {strokeColor: "#0000FF", strokeOpacity: 0.7, strokeWeight: 2, fillColor: "#0000FF", fillOpacity: 0.15, map: map, center: cellList[cell].center, radius: cellList[cell].accuracy};
                                var marker = new google.maps.Marker({position: cellList[cell].center, map: map, title: cellList[cell].title, icon: '../xml/cell.png'});
                                cityCircle = new google.maps.Circle(accuracy);
                            }
                            for (var wifi in wifiList) {
                                var accuracy = {strokeColor: "#9e7151", strokeOpacity: 0.7, strokeWeight: 2, fillColor: "#9e7151", fillOpacity: 0.15, map: map, center: wifiList[wifi].center, radius: wifiList[wifi].accuracy};
                                var marker = new google.maps.Marker({position: wifiList[wifi].center, map: map, title: wifiList[wifi].title, icon: '../xml/wifi.png'});
                                cityCircle = new google.maps.Circle(accuracy);
                            }
                            for (var exif in exifList) {
                                var accuracy = {strokeColor: "#076e33", strokeOpacity: 0.7, strokeWeight: 2, fillColor: "#09a133", fillOpacity: 0.15, map: map, center: exifList[exif].center, radius: exifList[exif].accuracy};
                                var marker = new google.maps.Marker({position: exifList[exif].center, map: map, title: exifList[exif].title, icon: '../xml/jpg.png'});
                                cityCircle = new google.maps.Circle(accuracy);
                            }
                            for (var twitter in twitterList) {
                                var accuracy = {strokeColor: "#383838", strokeOpacity: 0.7, strokeWeight: 2, fillColor: "#a8a8a8", fillOpacity: 0.15, map: map, center: twitterList[twitter].center, radius: twitterList[twitter].accuracy};
                                var marker = new google.maps.Marker({position: twitterList[twitter].center, map: map, title: twitterList[twitter].title, icon: '../xml/twitter.png'});
                                cityCircle = new google.maps.Circle(accuracy);
                            }
                            for (var gMap in gMapsList) {
                                var accuracy = {strokeColor: "#ffffff", strokeOpacity: 0.8, strokeWeight: 2, fillColor: "#ffffff", fillOpacity: 0.3, map: map, center: gMapsList[gMap].center, radius: gMapsList[gMap].accuracy};
                                var marker = new google.maps.Marker({position: gMapsList[gMap].center, map: map, title: gMapsList[gMap].title, icon: '../xml/g_maps.png'});
                                cityCircle = new google.maps.Circle(accuracy);
                            }
                            for (var browser in browsersList) {
                                var accuracy = {strokeColor: "#000000", strokeOpacity: 0.7, strokeWeight: 2, fillColor: "#000000", fillOpacity: 0.15, map: map, center: browsersList[browser].center, radius: browsersList[browser].accuracy};
                                var marker = new google.maps.Marker({position: browsersList[browser].center, map: map, title: browsersList[browser].title, icon: '../xml/g_maps.png'});
                                cityCircle = new google.maps.Circle(accuracy);
                            }
                        }
                    </script>
                    </head>
                    <body onload="initialize()">
                      <div id="map_canvas" style="width:100%; height:100%"></div>
                    </body>
                    </html>''')
    mapFile.close()
    _adel_log.log("LocationInfo:  ----> Location map \033[0;32m" + backup_dir + "/map.html\033[m created", 0)
