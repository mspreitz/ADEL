#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import _adel_log


#-----------------GLOBALS-------------------
# fully qualified file name of the sqlite database file to parse
DB_FILE_NAME = None
# file object of the opened sqlite database file
DB_FO = None
# flag whether db is set or not (true = 0, false != 0)
DB_FO_SET = 1
# database file size in pages
DB_FILESIZE_IN_BYTES = None
# database page size as stated in the header
DB_PAGESIZE_IN_BYTES = None
# reserved space at the end of each database page in bytes
DB_RESERVED_SPACE = 0
#-----------------GLOBALS-------------------


# Tries to open a SQlite database file.
# @fileName:            fully qualified name of the sqlite3 database file to open
# @return:              database page size in bytes if database was opened correctly, zero (0) otherwise
def open_db(file_name):
    global DB_FILE_NAME        
    global DB_FO
    global DB_FO_SET
    global DB_FILESIZE_IN_BYTES
    global DB_PAGESIZE_IN_BYTES
    global DB_RESERVED_SPACE

    # Ensure that there is no file open yet
    if DB_FO_SET == 0:
        _adel_log.log("open_db:        ----> WARNING! database file " + str(file_name).split("/")[-1] + " could not be opened, because a file is already open", 2)
        return 1

    # Ensure that the database file exists
    if os.path.exists(file_name):
        DB_FILE_NAME = file_name
        DB_FO = open(DB_FILE_NAME, "rb")
        DB_FO_SET = 0
        DB_FILESIZE_IN_BYTES = os.path.getsize(file_name)
        _adel_log.log("open_db:        ----> database file " + str(file_name).split("/")[-1] + " successfully loaded", 3)
        _adel_log.log("open_db:        ----> database file size is " + str(DB_FILESIZE_IN_BYTES) + " bytes", 3)
        # quick and dirty hack: retrieve database page size
        # alternatively we could parse the database header and store its values here
        DB_FO.seek(16, 0)
        DB_PAGESIZE_IN_BYTES = int(DB_FO.read(2).encode("hex"), 16)
        # quick and dirty hack: retrieve database page reserved space
        # alternatively we could parse the database header and store its values here
        DB_FO.seek(20, 0)
        DB_RESERVED_SPACE = int(DB_FO.read(1).encode("hex"), 16)
        return DB_FILESIZE_IN_BYTES

    _adel_log.log("open_db:        ----> ERROR! could not open database file " + str(file_name).split("/")[-1], 1)
    return 0
# end of function


# Closes the file that might have been opened by _sqliteParser:open_db().
def close_db():
    global DB_FILE_NAME
    global DB_FO
    global DB_FO_SET
    global DB_FILESIZE_IN_BYTES
    global DB_PAGESIZE_IN_BYTES
    # ensure that the database file is opened
    if DB_FO_SET == 0:
        DB_FO.close()
        _adel_log.log("close_db:        ----> database file \"" + str(DB_FILE_NAME) + "\" closed", 3)
        DB_FILE_NAME = None
        DB_FO = None
        DB_FO_SET = 1
        DB_FILESIZE_IN_BYTES = None
        DB_PAGESIZE_IN_BYTES = None
    else:
        _adel_log.log("close_db:        ----> WARNING! database file could not be closed, because none is open", 2)


# Reads a page with the given number in an SQLite database file and returns it's
# content as hexadecimal string.
# @db                   file object of the sqlite3 database file to read the page from
# @pageNumber           number of the page to read
# @pageSize             size of the page in bytes
# @return               complete content of the page as hexadecimal string or 'None' if page could not be read
def read_page(page_number):
    global DB_FO
    global DB_FO_SET
    global DB_PAGESIZE_IN_BYTES

    if (page_number < 1):
        # database file not open
        _adel_log.log("read_page:        ----> ERROR! invalid page number received, cannot read database page: " + str(page_number), 1)
        return ""

    if (DB_FO_SET == 0):
        # database file open
        fileOffset = ((page_number - 1) * DB_PAGESIZE_IN_BYTES)
        DB_FO.seek(fileOffset, 0)
        # transform to hex string for log output
        fileOffset = hex(fileOffset)
        _adel_log.log("read_page:        ----> database page " + str(page_number) + " read, file offset: " + str(fileOffset), 3)
        return DB_FO.read(DB_PAGESIZE_IN_BYTES).encode("hex")
    else:
        # database file not open
        _adel_log.log("read_page:        ----> ERROR! page could not be read, because database file is not open, call open_db() first", 1)
        return ""