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


"""\033[0;32mADEL - Android Data Extractor Lite.             \033[m

This Python script dumps all important SQLite Databases from a connected Android smartphone to the local
disk and analyzes these files in a forensically accurate workflow. If no smartphone is connected you can
specify a local directory which contains the databases you want to analyze. Afterwards this script creates
a clearly structured XML report.

If you connect a smartphone you need a rooted and insecure kernel/recovery installed on the smartphone.

Example for connected smartphone:
        \033[0;32m adel.py -d device -l 4\033[m

Example for database backups:
        \033[0;32m adel.py -d /home/user/backup -l 4\033[m

"""

__authors__ = '"Michael Spreitzenbarth & Sven Schmitt" <firstname.lastname@cs.fau.de>'

# Exit codes
# 0 => everything worked fine
# 3 => no smartphone connected

# Log level
# 0 = important status messages
# 1 = log error messages only
# 2 = log level 1 + warning messages
# 3 = log level 2 + normal messages
# 4 = log level 3 + debug messages

import os
import subprocess
import datetime
import sys
import shutil
import argparse


import _adel_log
import  _analyzeDB
import _dumpFiles
import _createReport
import _compareHashValues
import _locationInformation
import _getEXIF
import _getGestureLock
from _processXmlConfig import PhoneConfig


# DATE & TIME
DATE = str(datetime.datetime.today()).split(' ')[0]
TIME = str(datetime.datetime.today()).split(' ')[1].split('.')[0].split(':')


# Dumps sqlite databases from a connected android phone
def dumpDBs(file_dir, os_version, device_name):
    # Backup the SQLite files
    _adel_log.log("dumpDBs:       ----> dumping all SQLite databases....", 0)
    _dumpFiles.get_SQLite_files(file_dir, os_version, device_name)
    _adel_log.log("dumpDBs:       ----> all SQLite databases dumped", 0)
    _adel_log.log("", 3)


# analyzes the dumped databases
def analyzeDBs(file_dir, os_version, xml_dir, device_name, os_version2):
    config = PhoneConfig("xml/phone_configs.xml", device_name, os_version2) #TODO os_version2?
    # Call the analysis module
    _adel_log.log("analyzeDBs:    ----> starting to parse and analyze the databases....", 0)
    _analyzeDB.phone_info(file_dir, os_version, xml_dir, device_name, config)
    twitter_dbname_list = _dumpFiles.get_twitter_sqlite_files(file_dir, os_version)
    _analyzeDB.analyze(file_dir, os_version2, xml_dir, twitter_dbname_list, config)
    _adel_log.log("analyzeDBs:    ----> all databases parsed and analyzed....", 0)

    # Create report
    _adel_log.log("createReport:  ----> creating report....", 0)
    _createReport.report(xml_dir)
    _adel_log.log("ADEL MAIN:     ----> report \033[0;32m" + xml_dir + "/report.xml\033[m created", 0)


# Gets GPS-Location out of files
def get_location_information(backup_dir, device_name):
    _adel_log.log("\n############  LOCATION INFORMATION  ############\n", 2)
    output_file = open(backup_dir + "/LocationInformation.log", 'a+')
    output_file.write(('%25s %6s %11s %11s %11s %5s \n' % ('key', 'accuracy', 'confidence', 'latitude', 'longitude', 'time')))
    if device_name != "local":
        picture_position_list = _getEXIF.get_exif_information(backup_dir, output_file)
        backup_dir = backup_dir + "/databases"
    else:
        picture_position_list = ""
    twitter_position_list = _locationInformation.get_location_information_twitter(backup_dir, output_file)
    gmaps_position_list = _locationInformation.get_location_information_gmaps(backup_dir, output_file)
    cell_position_list = _locationInformation.get_location_information_cell(backup_dir, output_file)
    wifi_position_list = _locationInformation.get_location_information_wifi(backup_dir, output_file)
    browser_position_list = _locationInformation.get_location_information_browser(backup_dir, output_file)
    _locationInformation.createMap(backup_dir, cell_position_list, wifi_position_list, picture_position_list, twitter_position_list, gmaps_position_list, browser_position_list)
    output_file.close()


# The main function
def run(argv):
    # Manual
    usage = "\033[0;32m adel.py <device/backup_folder> <loglevel>\033[m The loglevel is an optional value."
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-l', '--loglevel', default=4, const='4', nargs='?', help='The loglevel is an optional value between 0 (no logging) and 4 (full debug logging).')
    parser.add_argument('-d', '--device', default=False, nargs='?', help='Use the device name of the smartphone to load the correct config.')
    parser.add_argument('-db', '--database', default=False, nargs='?', help='Absolute path for already dumped databases')
    options = parser.parse_args(argv[1:])
    print sys.argv
    print options.device
    if not options.device:
        print "Illegal number of arguments"
        print usage
        sys.exit(1)
    else:
        mode = options.device
    if (int(options.loglevel) >= 0) and (int(options.loglevel) <= 4):
            _adel_log.LOG_LEVEL_GLOBAL = int(options.loglevel)
    else:
        _adel_log.LOG_LEVEL_GLOBAL = 4

    # Programm header
    os.system("clear")
    
    print """\033[0;32m
              _____  ________  ___________.____
             /  _  \ \______ \ \_   _____/|    |
            /  /_\  \ |    |  \ |    __)_ |    |
           /    |    \|    `   \|        \|    |___
           \____|__  /_______  /_______  /|_______ \  
                   \/        \/        \/         \/
               Android Data Extractor Lite v2.0
    \033[m"""

    print "\n"
    print "ADEL MAIN:     ----> starting script...."
    if not options.database:

        # Opening the connection to the smartphone or emulator
        print "ADEL MAIN:     ----> Trying to connect to smartphone or emulator...."

        # Check if there is a smartphone or emulator connected
        if len(subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE).communicate(0)[0].split()) > 4:

            # Create backup directory
            try:
                device_name = subprocess.Popen(['adb', 'devices'], stdout=subprocess.PIPE).communicate(0)[0].split()[4]
            except:
                print "\033[0;31mADEL MAIN:     ----> ERROR! No Android smartphone connected !!\033[m"
                sys.exit(3) # indicates that no smartphone or emulator was connected to the PC
            print "dumpDBs:       ----> opening connection to device: \033[0;32m" + device_name + "\033[m"

            # Starting the deamon with root privileges
            subprocess.Popen(['adb', 'root'], stdout=subprocess.PIPE).communicate(0)[0]
            backup_dir = DATE + "__" + TIME[0] + "-" + TIME[1] + "-" + TIME[2] + "__" + device_name
            os.mkdir(backup_dir)

            # Create log file and log directory if LOGLEVEL is > 0
            if _adel_log.LOG_LEVEL_GLOBAL > 0:
                log_file = backup_dir + "/log/adel.log"
                os.mkdir(backup_dir + "/log")
                _adel_log.FILE_HANDLE = open(log_file, "a+")
                _adel_log.log("\n# (c) mspreitzenbarth & sschmitt 2012 \n\n\n         _____  ________  ___________.____            \n         /  _  \ \______ \ \_   _____/|    |           \n        /  /_\  \ |    |  \ |    __)_ |    |           \n       /    |    \|    `   \|        \|    |___        \n       \____|__  /_______  /_______  /|_______ \       \n               \/        \/        \/         \/       \n           Android Data Extractor Lite v2.0", 2)
                _adel_log.log("dumpDBs:       ----> evidence directory \033[0;32m" + backup_dir + "\033[m created", 0)
                _adel_log.log("ADEL MAIN:     ----> log file \033[0;32m" + log_file + "\033[m created", 0)
                _adel_log.log("ADEL MAIN:     ----> log level: \033[0;32m" + str(_adel_log.LOG_LEVEL_GLOBAL) + "\033[m", 0)

            # Get Android OS version which is running on the connected device
            try:
                os_version = subprocess.Popen(['adb', 'shell', 'getprop', 'ro.build.version.release'], stdout=subprocess.PIPE).communicate(0)[0].split()[0]
            except:
                os_version = subprocess.Popen(['adb', 'shell', 'getprop', 'ro.build.version.release'], stdout=subprocess.PIPE).communicate(0)[0]
            os_version2 = os_version.replace(".", "")
            if len(os_version2) < 3:
                os_version2 = os_version2.join("0")
            _adel_log.log("dumpDBs:       ----> device is running\033[0;32m Android OS " + os_version + "\033[m", 0)

            # Do the main logging action
            _adel_log.log("\n############  SMARTPHONE & GLOBAL INFO  ############\n", 2)
            _adel_log.log("dumpDBs:             Date: " + DATE + "  " + TIME[0] + ":" + TIME[1] + ":" + TIME[2], 3)
            _adel_log.log("dumpDBs:             Device Name: " + device_name, 3)
            _adel_log.log("dumpDBs:             Device is running: Android v" + os_version, 3)
            _adel_log.log("dumpDBs:             Log Level: " + str(_adel_log.LOG_LEVEL_GLOBAL), 3)

            # Call the dumping and analysing methods and create output directory
            xml_dir = backup_dir + "/xml" 
            os.mkdir(xml_dir)

            # Copy the xml stylesheet to the evidence directory
            shutil.copy("xml/report.xsl", xml_dir + "/report.xsl")
            file_dir = backup_dir + "/databases"
            os.mkdir(file_dir)
            dumpDBs(file_dir, os_version, device_name)
            _getGestureLock.crack(backup_dir)
            get_location_information(backup_dir, device_name)
            analyzeDBs(file_dir, os_version, xml_dir, options.device, os_version2)
            _compareHashValues.compare(backup_dir)

            # Killing deamon and closing the logfile
            _adel_log.log("ADEL MAIN:     ----> stopping script....", 0)
            print "\n"
            print "\033[0;32m         (c) m.spreitzenbarth & s.schmitt 2012\033[m"
            print "\n\n"

            # Close log file if any was created (log level must be > 0)
            if _adel_log.LOG_LEVEL_GLOBAL > 0:
                _adel_log.FILE_HANDLE.close()
        else:
            print "\033[0;31mADEL MAIN:     ----> ERROR! No Android smartphone connected !!\033[m"
            print "ADEL MAIN:     ----> stopping script...."
            subprocess.Popen(['adb', 'kill-server'], stdout=subprocess.PIPE).communicate(0)[0]
            print "\n"
            print "\033[0;32m         (c) m.spreitzenbarth & s.schmitt 2012\033[m"
            print "\n\n"
            sys.exit(3) # indicates that no smartphone or emulator was connected to the PC
    else:
        # Define global variables
        backup_dir = options.database
        file_dir = backup_dir
        device_name = "local"
        os_version = "2.3.3"
        os_version2 = "233"

        # Create log file and log directory if LOGLEVEL is > 0
        if _adel_log.LOG_LEVEL_GLOBAL > 0:
            log_file = backup_dir + "/log/adel.log"
            os.mkdir(backup_dir + "/log")
            _adel_log.FILE_HANDLE = open(log_file, "a+")
            _adel_log.log("\n# (c) mspreitzenbarth & sschmitt 2011 \n\n\n         _____  ________  ___________.____            \n         /  _  \ \______ \ \_   _____/|    |           \n        /  /_\  \ |    |  \ |    __)_ |    |           \n       /    |    \|    `   \|        \|    |___        \n       \____|__  /_______  /_______  /|_______ \       \n               \/        \/        \/         \/       \n           Android Data Extractor Lite v2.0", 2)
            _adel_log.log("dumpDBs:       ----> evidence directory \033[0;32m" + backup_dir + "\033[m created", 0)
            _adel_log.log("ADEL MAIN:     ----> log file \033[0;32m" + log_file + "\033[m created", 0)
            _adel_log.log("ADEL MAIN:     ----> log level: \033[0;32m" + str(_adel_log.LOG_LEVEL_GLOBAL) + "\033[m", 0)
        _adel_log.log("dumpDBs:       ----> using configuration for\033[0;32m Android 2.3.3\033[m", 0)

        # Do the main logging action
        _adel_log.log("\n############  SMARTPHONE & GLOBAL INFO  ############\n", 2)
        _adel_log.log("dumpDBs:             Date: " + DATE + "  " + TIME[0] + ":" + TIME[1] + ":" + TIME[2], 3)
        _adel_log.log("dumpDBs:             Log Level: " + str(_adel_log.LOG_LEVEL_GLOBAL), 3)

        # Call the dumping and analysing methods and create output directory
        xml_dir = backup_dir + "/xml" 
        os.mkdir(xml_dir)

        # Copy the xml stylesheet to the evidence directory
        shutil.copy("xml/report.xsl", xml_dir + "/report.xsl")
        dumpDBs(file_dir, os_version, device_name)
        get_location_information(backup_dir, device_name)
        analyzeDBs(file_dir, os_version, xml_dir, options.device, os_version2)

        # Killing deamon and closing the logfile
        _adel_log.log("ADEL MAIN:     ----> stopping script....", 0)
        print "\n"
        print "\033[0;32m         (c) m.spreitzenbarth & s.schmitt 2012\033[m"
        print "\n\n"

        # Close log file if any was created (log level must be > 0)
        if _adel_log.LOG_LEVEL_GLOBAL > 0:
            _adel_log.FILE_HANDLE.close()


if __name__ == '__main__':
    run(sys.argv)
