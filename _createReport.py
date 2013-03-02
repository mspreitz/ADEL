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


def report(xml_dir):
    report_file = open(xml_dir + "/report.xml", "a+")
    report_file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    report_file.write('<?xml-stylesheet type="text/xsl" href="report.xsl"?>\n')
    report_file.write('<report>\n')
    for root, dirs, files in os.walk(xml_dir):
        files.sort(reverse=False)
    for xml_file in files:
        if xml_file != "report.xml":
            data = open(xml_dir + "/" + xml_file, "r")
            for line in data:
                if line.startswith("<?"):
                    continue;
                else:
                    report_file.write(line)
        else:
            continue;
    report_file.write('</report>')
    report_file.close()