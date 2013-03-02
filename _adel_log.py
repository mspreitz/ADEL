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


# Global variable definitions (must be set through the __main__ program).
# This is a work around due to import problems (__main__ is importing
# _adel_log and vice versa) and we do not want to pass this two variables
# at each call of the log()  method.

LOG_LEVEL_GLOBAL = 4
FILE_HANDLE = None


# Write the given message to a specific log file if appropriate
# loglevel is set.
# A seperate log file is created for each execution of ADEL.
# @message:             message to write to the log file
# @log_level:            desired log level of message
def log(message, log_level):
    global LOG_LEVEL_GLOBAL
    global LOG_DIR

    if (int(log_level) <= int(LOG_LEVEL_GLOBAL)) and (int(log_level) > 0):
        # Write message to log file
        if FILE_HANDLE is None:
            print "\033[0;31m" + "log: ERROR! file handle not set\
                   (is \'None\')" + "\033[m"
        else:
            FILE_HANDLE.write(message + "\n")
    if log_level == 1:
        print "\033[0;31m" + message + "\033[m"
    if ((log_level == 2) and (not (message.startswith("#"))) and
       (not (message.startswith("\n#")))):
            print "\033[0;31m" + message + "\033[m"
    if log_level == 0:
        print message