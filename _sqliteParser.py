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


if __name__ == "__main__":
    import _adel_log
    import _sqliteFileHandler
    import _sqlitePageParser
    import _helpersStringOperations
    import datetime
    import sys
else:
    import _adel_log
    import _sqliteFileHandler
    import _sqlitePageParser
    import _helpersStringOperations


#-----------------GLOBALS-------------------
DB_FILE_SIZE_IN_BYTES = 0
# Header bytes [0:15]: sqlite3 magic string "SQLite format 3"
HEADER_MAGIC_STRING = ""
# Header bytes [16:18]: database page size
HEADER_DATABASE_PAGESIZE = 0
# Header bytes [18:19]: file format write version (must be 1 or 2)
HEADER_FILE_FORMAT_WRITE_VERSION = 0
# Header bytes [19:20]: file format read version (must be 1 or 2)
HEADER_FILE_FORMAT_READ_VERSION = None
# Header bytes [20:21]: reserved space per page (usually 0)
HEADER_RESERVED_SPACE_PER_PAGE = None
# Header bytes [21:22]: maximum embedded payload fraction (must be 64)
HEADER_MAXIMUM_EMBEDDED_PAYLOAD_FRACTION = None
# Header bytes [22:23]: minimum embedded payload fraction (must be 32)
HEADER_MINIMUM_EMBEDDED_PAYLOAD_FRACTION = None
# Header bytes [23:24]: leaf payload fraction (must be 32)
HEADER_LEAF_PAYLOAD_FRACTION = None
# Header bytes [24:27]: file change counter
HEADER_FILE_CHANGE_COUNTER = None
# Header bytes [28:31]: database size in pages
HEADER_DATABASE_SIZE_IN_PAGES = None
# Header bytes [32:35]: first freelist trunk page
HEADER_FIRST_FREE_TRUNK_PAGE = None
# Header bytes [36:39]: total number of freelist pages
HEADER_TOTAL_NUMBER_OF_FREELIST_PAGES = None
# Header bytes [40:43]: schema cookie
HEADER_SCHEMA_COOKIE = None
# Header bytes [44:47]: schema format number (must be 1-4)
HEADER_SCHEMA_FORMAT_NUMBER = None
# Header bytes [48:51]: default page cache size
HEADER_DEFAULT_PAGE_CACHE_SIZE = None
# Header bytes [52:55]: largest root b-tree page number
HEADER_LARGEST_ROOT_BTREE_PAGE_NUMBER = None
# Header bytes [56:59]: database text encoding (must be 1-3)
HEADER_DATABASE_TEXT_ENCODING = None
# Header bytes [60:64]: user version
HEADER_USER_VERSION = None
# Header bytes [64:67]: incremental-vacuum mode (1, zero otherwise)
HEADER_INCREMENTAL_VACCUM_MODE = None
# Header bytes [68:91]: reservation for expansion (must be 0)
HEADER_RESERVED_FOR_EXPANSION = None
# Header bytes [92:95]: version valid for number
HEADER_VERSION_VALID_FOR_NUMBER = None
# Header bytes [96:99]: sqlite version number
HEADER_SQLITE_VERSION_NUMBER = None
# Flag indicates whether HEADER_FILE_CHANGE_COUNTER is valid or not
HEADER_FILE_CHANGE_COUNTER_VALID = None
# place holder for integer primary key (= row ID) columns (max 1 per table)
ROW_ID_COLUMN = 0
#-----------------GLOBALS-------------------


# Main function of the sqlite parser scripts. Opens the database, reads the file header,
# parses the database schema definitions and returns a list with exactly one element for
# each database table. Each element holds the complete content of a table, including the
# column definitions of the table in the form of [column name, column type] as first element.
# @file_name:           fully qualified name of the sqlite3 database file to parse
# @return:              list with all contents that were extractet from the database file or
#                       empty list, if an error occured
def parse_db(file_name):
    global DB_FILE_SIZE_IN_BYTES
    global ROW_ID_COLUMN

    _adel_log.log("\n############  SQLite PARSER -> " + file_name + "  ############ \n", 2)
    _adel_log.log("parse_db:                      ----> parsing sqlite3 database file....", 3)

    # Open the database
    DB_FILE_SIZE_IN_BYTES = _sqliteFileHandler.open_db(file_name)
    if DB_FILE_SIZE_IN_BYTES == 0:
        # file could not be opened correctly
        return []

    # Read first page of database file
    first_page_hex_string = _sqliteFileHandler.read_page(1)
    # ensure that read page could retrieve an existing page
    if (first_page_hex_string == ""):
        _adel_log.log("parse_db: ERROR - cannot read first page of database", 1)
        return []

    # Parse the database header on the first page (first 100 bytes in the database file)
    parse_db_header(first_page_hex_string)
    if HEADER_DATABASE_TEXT_ENCODING > 1:
        _adel_log.log("parse_db: ERROR - database text encoding " + str(HEADER_DATABASE_TEXT_ENCODING) + " not supported in this version of FSP", 1)
        return []

    # Parse database schema (first page of the database file is root b-tree page for the schema btree)
    # Database schema is stored in a well defined way (sqlite master table)
    # CREATE TABLE sqlite_master(
    # type text, # must be one of the following: ['table', 'index', 'view', 'trigger']
    # name text,
    # tbl_name text,
    # rootpage integer,
    # sql text
    # );
    _adel_log.log("\nparseDB:                      ----> parsing sqlite3 database SCHEMA....", 3)
    db_schemata = _sqlitePageParser.parse_table_btree_page(first_page_hex_string, 100) # 100 bytes database file header
    _adel_log.log("parse_db:                      ----> sqlite3 database SCHEMA parsed", 3)

    # Initialize the resulting content list
    result_list = []
    final_list = []

    # loop through all schemata of the database
    for db_schema in db_schemata:
        if len(db_schema) != 5 + 1: # +1 due to manually added leading rowID
            _adel_log.log("parse_db: WARNING! invalid length of database schema statement entry detected: ", 2)
            _adel_log.log(str(db_schema), 2)
            continue

        # Reset result list for new element
        result_list = []

        # Parse this database element (table, index, view or trigger)
        if (_helpersStringOperations.starts_with_string(str(db_schema[1]), "TABLE") == 0):
            # PARSE TABLE STATEMENT
            # Ensure that we treat a valid schema
            db_schemata_statement = db_schema[len(db_schema) - 1]
            if ((db_schemata_statement == None) or (db_schemata_statement == "")):
                _adel_log.log("parse_db: WARNING! missing database schema statement entry detected, printing schema statement:", 2)
                _adel_log.log(str(db_schema), 3)
                continue

            sql_statement = (db_schema[5]) # db_schema[5] is expected to be the "sql text" as defined in sqlite_master
            _adel_log.log("\nparseDB:                      ----> parsing new database structure with SQL statement:", 3)
            _adel_log.log(str(sql_statement), 3)

            # Extract and check command (expected to be CREATE)
            command_tuple = _helpersStringOperations.split_at_first_occurrence(sql_statement, " ")
            if (len(command_tuple) == 0):
                _adel_log.log("parse_db: WARNING! invalid sql COMMAND detected, continuing with next database element (e.g. next table)", 2)
                continue
            if (_helpersStringOperations.starts_with_string(str(command_tuple[0]), "CREATE") != 0):
                _adel_log.log("parse_db: WARNING! invalid sql COMMAND detected, expected \"CREATE\" but found: " + str(command_tuple[0]), 2)
                _adel_log.log("                  continuing with next database element (e.g. next table)", 2)
                continue
            # Extract and check first command operand (expected to be TEMP, TEMPORARY, TABLE or VIRTUAL TABLE)
            type_tuple = _helpersStringOperations.split_at_first_occurrence(command_tuple[1], " ")
            if len(type_tuple) == 0:
                _adel_log.log("parse_db: WARNING! invalid sql COMMAND TYPE detected, continuing with next database element (e.g. next table)", 2)
                continue
            # According to the syntax diagrams of the sqlite SQL create table statement there are TEMP or TEMPORARY key words allowed at this place
            if   (_helpersStringOperations.starts_with_string(str(type_tuple[0]), "TEMP") == 0
              or _helpersStringOperations.starts_with_string(str(type_tuple[0]), "TEMPORARY") == 0
              or _helpersStringOperations.starts_with_string(str(type_tuple[0]), "VIRTUAL") == 0):
                # Ignore and proceed with next fragement (must then be TABLE)
                type_tuple = _helpersStringOperations.split_at_first_occurrence(type_tuple[1], " ")
                if len(type_tuple) == 0:
                    _adel_log.log("parse_db: WARNING! invalid sql COMMAND TYPE after TEMP(ORARY) detected, continuing with next database element (e.g. next table)", 2)
                    continue
            # This fragment must be table
            if (_helpersStringOperations.starts_with_string(str(type_tuple[0]), "TABLE") != 0):
                _adel_log.log("parse_db: WARNING! invalid sql COMMAND TYPE detected, expected \"TABLE\" but found: " + str(type_tuple[0]), 2)
                _adel_log.log("                  continuing with next database element (e.g. next table)", 2)
                continue
            # Extract and check second command operand (expected to be table name)
            name_tuple = []
            next_space = _helpersStringOperations.split_at_first_occurrence(type_tuple[1], " ")
            next_parenthesis = _helpersStringOperations.split_at_first_occurrence(type_tuple[1], "(")
            if (next_space < next_parenthesis):
                # "IF NOT EXISTS" statement possible
                if (_helpersStringOperations.starts_with_string(str(_helpersStringOperations.crop_whitespace(type_tuple[1])), "IF") == 0):
                    type_tuple[1] = type_tuple[1][2:]
                if (_helpersStringOperations.starts_with_string(str(_helpersStringOperations.crop_whitespace(type_tuple[1])), "NOT") == 0):
                    type_tuple[1] = type_tuple[1][3:]
                if (_helpersStringOperations.starts_with_string(str(_helpersStringOperations.crop_whitespace(type_tuple[1])), "EXISTS") == 0):
                    type_tuple[1] = type_tuple[1][6:]
                type_tuple[1] = _helpersStringOperations.crop_whitespace(type_tuple[1])

                # Extract name tuple
                name_tuple = _helpersStringOperations.split_at_first_occurrence(type_tuple[1], " ")
                if len(name_tuple) == 0:
                    name_tuple = _helpersStringOperations.split_at_first_occurrence(type_tuple[1], "(")
                    if len(name_tuple) == 0:
                        _adel_log.log("parse_db: WARNING! invalid sql COMMAND TYPE NAME detected, continuing with next database element (e.g. next table)", 2)
                        continue
                    # Append leading opening parenthesis that we cut off before
                    name_tuple[1] = "(" + str(name_tuple[1])
                else:
                    # "AS ..." statement possible
                    tmp_string = _helpersStringOperations.crop_whitespace(name_tuple[1])
                    if (tmp_string.startswith("AS")):
                        _adel_log.log("parse_db:                            OK - \"AS\" statement detected: " + str(tmp_string), 3)
                        _adel_log.log("parse_db:                            OK - no data stored, thus continuing with next database element (e.g. next table)", 3)
                        continue
            else:
                name_tuple = _helpersStringOperations.split_at_first_occurrence(type_tuple[1], "(")
                if len(name_tuple) == 0:
                    _adel_log.log("parse_db: WARNING! invalid sql COMMAND TYPE NAME detected, continuing with next database element (e.g. next table)", 2)
                    continue
                # Append leading opening parenthesis that we cut off before
                name_tuple[1] = "(" + str(name_tuple[1])

            # Now ready to parse TABLE
            _adel_log.log("parse_db:                      ----> parsing database structure " + str(type_tuple[0]) + " \"" + str(name_tuple[0]) + "\"", 3)
            _adel_log.log("parse_db:                      ----> parsing SQL statement of " + str(type_tuple[0]) + "....", 3)
            _adel_log.log("parse_db:                            OK - SQL statement is of type: " + str(command_tuple[0]) + " " + str(type_tuple[0]), 3)

            # Parse and append sql statement
            name_tuple[1] = _helpersStringOperations.cut_first_last_exclude(name_tuple[1], "(", ")")
            result_list.append(parse_sql_statement_params(name_tuple[1]))

            # Ensure we deal with a real table, virtual tables have no b-tree and thus the b-tree root page pointer is 0
            if (db_schema[4] == 0):
                _adel_log.log("parse_db:                            OK - this table holds no content (e.g. virtual table), continuing with next database element (e.g. next table)", 3)
                _adel_log.log("parse_db:                      ----> database structure " + str(type_tuple[0]) + " \"" + str(name_tuple[0]) + "\" parsed", 3)
                # Append result from table, index, view or trigger to final list
                final_list.append(result_list)
                continue

            # Parse and append table contents
            btree_root_page_string = _sqliteFileHandler.read_page(db_schema[4])
            # Ensure that read page could retrieve an existing page
            if (btree_root_page_string == ""):
                _adel_log.log("parse_db: ERROR - could not refer to b-tree root page: " + str(db_schema[4]), 1)
                _adel_log.log("                 continuing with next database element (e.g. next table)", 1)
                continue
            _adel_log.log("parse_db:                      ----> parsing contents of " + str(type_tuple[0]) + "....", 3)
            table_contents = _sqlitePageParser.parse_table_btree_page(btree_root_page_string, 0)

            # Check whether the table contains a dedicated row ID column
            if (ROW_ID_COLUMN == 0):
                # Table has no dedicated row ID column, add "rowID" to the table statement (the rowID is already extractet)
                index_of_last_element_in_result_list = len(result_list) - 1
                temp_list = result_list[index_of_last_element_in_result_list]
                result_list[index_of_last_element_in_result_list] = [["rowID", "INTEGER"]]
                for element in range(len(temp_list)):
                    result_list[index_of_last_element_in_result_list].append(temp_list[element])
                # Append table contents to the result list
                for row in table_contents:
                    result_list.append(row)
            else:
                # Table has a dedicated row ID column (integer primary key column), link values stored as row ID in the b-tree to this column (at the place of this column)
                # Append table contents to the result list
                for row in table_contents:
                    # Replace "None" entries in integer primary key column of each row through the actual row ID
                    row[ROW_ID_COLUMN] = row[0]
                    # Delete manually appended row ID column (in parse_sql_statement_params)
                    temp_row = row
                    row = []
                    for index in range(len(temp_row) - 1):
                        row.append(temp_row[index + 1])
                    # Append corrected row
                    result_list.append(row)

            # Append result from table, index, view or trigger to final list
            final_list.append(result_list)
            _adel_log.log("parse_db:                      ----> database structure " + str(type_tuple[0]) + " \"" + str(name_tuple[0]) + "\" parsed", 3)

            # TODO: comment out the following print statements in productive environment
            #_adel_log.log("\n_sqliteParser.py:234, parse_db ----> printing database schema for " + str(type_tuple[0]) + " \"" + str(name_tuple[0]) + "\" for test purposes:", 4)
            #_adel_log.log(str(db_schema[len(db_schema) - 1]), 4)
            #_adel_log.log("\n_sqliteParser.py:236, parse_db ----> printing database contents for " + str(type_tuple[0]) + " \"" + str(name_tuple[0]) + "\" for test purposes:", 4)
            #for result in result_list:
            #    _adel_log.log(str(result), 4)
            # comment out the above print statements in productive environment

        # PARSE INDEX STATEMENT
        #if ((str(db_schema[1]) == "INDEX") or (str(db_schema[1]) == "Index") or (str(db_schema[1]) == "index")):
        # TODO: implement if necessary
        # IGNORED RIGHT NOW

        # PARSE VIEW STATEMENT
        #if ((str(db_schema[1]) == "VIEW") or (str(db_schema[1]) == "View") or (str(db_schema[1]) == "view")):
        # TODO: implement if necessary
        # IGNORED RIGHT NOW

        # PARSE TRIGGER STATEMENT
        #if ((str(db_schema[1]) == "TRIGGER") or (str(db_schema[1]) == "Trigger") or (str(db_schema[1]) == "trigger")):
        # TODO: implement if necessary
        # IGNORED RIGHT NOW

    _adel_log.log("\nparseDB:                      ----> returning contents of the database file", 3)
    # Close the database file
    _sqliteFileHandler.close_db()
    _adel_log.log("parse_db:                      ----> sqlite3 database file parsed", 3)

    return final_list



# Parses the parameter string of SQL statements and splits the string into it's elements.
# Returns a list containing single parameters of the SQL statement in the form of tuples:
# [column name, column type definition]
# @hex_string:           hexadecimal string of sql statement parameters
# @return:              list of tuples with splitted parameter information [column name, column type]
def parse_sql_statement_params(hex_string):
    global ROW_ID_COLUMN

    # Build params list
    param_list = _helpersStringOperations.split_parenthesis_sensitive(hex_string, ",")

    # Initialise result list and reset ROW_ID_COLUMN
    result_list = []
    ROW_ID_COLUMN = 0

    # Create correct sql statement parameter list
    index = 0
    max_index = len(param_list)
    _adel_log.log("parse_sql_statement_params:      ----> printing SQL statement parameters in the form [column name, column type]....", 3)
    while index < max_index:
        # Crop any white space
        param_list[index] = _helpersStringOperations.crop_whitespace(param_list[index])

        # Ensure that we have a column (starts with column name) and no table constraint
        if (_helpersStringOperations.starts_with_string(param_list[index], "CONSTRAINT") == 0
          or _helpersStringOperations.starts_with_string(param_list[index], "PRIMARY KEY") == 0
          or _helpersStringOperations.starts_with_string(param_list[index], "UNIQUE") == 0
          or _helpersStringOperations.starts_with_string(param_list[index], "CHECK") == 0
          or _helpersStringOperations.starts_with_string(param_list[index], "FOREIGN") == 0):
            _adel_log.log("parse_sql_statement_params:            OK - TABLE constraint detected at positon: " + str(index + 1) + ", constraint is: " + str(param_list[index]), 3)
            index += 1
            continue

        # Ok, we deal with a column
        column_tuple = _helpersStringOperations.split_at_first_occurrence(param_list[index], " ")
        if len(column_tuple) == 0:
            # Append as is
            param_tuple = [param_list[index], ""]
            result_list.append(param_list[index])
            _adel_log.log("parse_sql_statement_params:            OK - " + str(index + 1) + ". column is: " + str(param_tuple), 3)
            index += 1
            continue

        # Otherwise we have to parse the statement
        # at this position we can have a type-name or column constraints
        column_name = _helpersStringOperations.crop_whitespace(column_tuple[0]) 
        column_string = _helpersStringOperations.crop_whitespace(column_tuple[1])

        # Check if we deal with a column constraint
        if ((_helpersStringOperations.starts_with_string(column_string, "CONSTRAINT") == 0)
          or (_helpersStringOperations.starts_with_string(column_string, "PRIMARY KEY") == 0)
          or (_helpersStringOperations.starts_with_string(column_string, "NOT") == 0)
          or (_helpersStringOperations.starts_with_string(column_string, "UNIQUE") == 0)
          or (_helpersStringOperations.starts_with_string(column_string, "CHECK") == 0)
          or (_helpersStringOperations.starts_with_string(column_string, "DEFAULT") == 0)
          or (_helpersStringOperations.starts_with_string(column_string, "COLLATE") == 0)
          or (_helpersStringOperations.starts_with_string(column_string, "REFERENCES")) == 0):
            # Create and append param_tuple
            param_tuple = [column_name, ""]
            result_list.append(param_tuple)
            _adel_log.log("parse_sql_statement_params:            OK - " + str(index + 1) + ". column is: " + str(param_tuple) + ", constraint(s): " + column_string, 3)
            # Check whether this row functions as row ID (integer PRIMARY KEY)
            if (_helpersStringOperations.starts_with_string(column_string, "PRIMARY KEY") == 0):
                ROW_ID_COLUMN = index + 1
            index += 1
            continue

        # There is no column constraint, so there must be a type-name
        type_tuple = []
        next_space = _helpersStringOperations.fist_occurrence(column_string, " ")
        next_parenthesis = _helpersStringOperations.fist_occurrence(column_string, "(")
        if (next_space >= 0) and ((next_space < next_parenthesis) or (next_parenthesis < 0)):
            # Cut at the next space
            type_tuple = _helpersStringOperations.split_at_first_occurrence(column_string, " ")
        else:
            if (next_parenthesis >= 0) and ((next_parenthesis <= next_space) or (next_space < 0)):
                # Cut at the next parenthesis
                type_tuple = _helpersStringOperations.split_at_first_occurrence(column_string, "(")
                type_tuple[1] = "(" + str(type_tuple[1]) # append the opening paranthesis that was cut off

        if len(type_tuple) == 0:
            # Create and append param_tuple
            param_tuple = [column_name, column_string]
            result_list.append(param_tuple)
            _adel_log.log("parse_sql_statement_params:            OK - " + str(index + 1) + ". column is: " + str(param_tuple), 3)
            index += 1
            continue

        # The statement continues, so continue to parse
        # set type name and type string
        type_name = _helpersStringOperations.crop_whitespace(type_tuple[0]) 
        type_string = _helpersStringOperations.crop_whitespace(type_tuple[1])

        # The remaining string can contain further type name definitions (e.g. varchar(20) or column constraint statements
        # check if we deal with a column constraint
        if ((_helpersStringOperations.starts_with_string(type_string, "CONSTRAINT") == 0)
          or (_helpersStringOperations.starts_with_string(type_string, "PRIMARY KEY") == 0)
          or (_helpersStringOperations.starts_with_string(type_string, "NOT") == 0)
          or (_helpersStringOperations.starts_with_string(type_string, "UNIQUE") == 0)
          or (_helpersStringOperations.starts_with_string(type_string, "CHECK") == 0)
          or (_helpersStringOperations.starts_with_string(type_string, "DEFAULT") == 0)
          or (_helpersStringOperations.starts_with_string(type_string, "COLLATE") == 0)
          or (_helpersStringOperations.starts_with_string(type_string, "REFERENCES")) == 0):
            # Create and append param_tuple
            param_tuple = [column_name, type_name]
            result_list.append(param_tuple)
            _adel_log.log("parse_sql_statement_params:            OK - " + str(index + 1) + ". column is: " + str(param_tuple) + ", constraint(s): " + type_string, 3)
            # Check whether this row functions as row ID (integer PRIMARY KEY)
            if (_helpersStringOperations.starts_with_string(type_string, "PRIMARY KEY") == 0):
                ROW_ID_COLUMN = index + 1
            index += 1
            continue

        # Check for further type name definitions, they must be enclosed in parenthesis and belong to the type name
        restTuple = _helpersStringOperations.cut_first_last_include_into_tuple(type_string, "(", ")")
        if len(restTuple) == 0:
            # this case should not occur
            _adel_log.log("parse_sql_statement_params: WARNING! invalid column TYPE STRING in " + str(index + 1) + ". column: " + str(type_string), 2)
            _adel_log.log("                                  continuing with next column definition", 2)
            index += 1
            continue
        else:
            # The statement continues, so continue to parse
            # set rest name and rest string
            rest_name = _helpersStringOperations.crop_whitespace(restTuple[0]) 
            rest_string = _helpersStringOperations.crop_whitespace(restTuple[1])
            # Rest name belongs to the type name, append it
            type_name = type_name + " " + str(rest_name)

            # Create and append param_tuple
            param_tuple = [column_name, type_name]
            result_list.append(param_tuple)
            # We log the param_tuple later, so possible column constraints can be included

            # Rest string can be column constraint, check it
            if len(rest_string) > 0:
                if ((_helpersStringOperations.starts_with_string(rest_string, "CONSTRAINT") == 0)
                  or (_helpersStringOperations.starts_with_string(rest_string, "PRIMARY KEY") == 0)
                  or (_helpersStringOperations.starts_with_string(rest_string, "NOT") == 0)
                  or (_helpersStringOperations.starts_with_string(rest_string, "UNIQUE") == 0)
                  or (_helpersStringOperations.starts_with_string(rest_string, "CHECK") == 0)
                  or (_helpersStringOperations.starts_with_string(rest_string, "DEFAULT") == 0)
                  or (_helpersStringOperations.starts_with_string(rest_string, "COLLATE") == 0)
                  or (_helpersStringOperations.starts_with_string(rest_string, "REFERENCES")) == 0):
                    # Log column constraint
                    _adel_log.log("parse_sql_statement_params:            OK - " + str(index + 1) + ". column is: " + str(param_tuple) + ", constraint(s): " + rest_string, 3)
                    # Check whether this row functions as row ID (integer PRIMARY KEY)
                    if (_helpersStringOperations.starts_with_string(rest_string, "PRIMARY KEY") == 0):
                        ROW_ID_COLUMN = index + 1
                else:
                    # This case should not occur
                    _adel_log.log("parse_sql_statement_params: WARNING! invalid column REST STRING in " + str(index + 1) + ". column: " + str(rest_string), 2)
                    _adel_log.log("                                  continuing with next column definition", 2)
            else:
                # Log without column constraints
                _adel_log.log("parse_sql_statement_params:            OK - " + str(index + 1) + ". column is: " + str(param_tuple), 3)
            index += 1

    return result_list



# Parses the SQLite database header structure which is contained within the
# first 100 bytes of the database file (page 1) and set all corresponding global 
# variables.
# @first_page_hex_string:  first page of the database file as hexadecimal string
def parse_db_header(first_page_hex_string):
    global DB_FILE_SIZE_IN_BYTES
    global HEADER_MAGIC_STRING
    global HEADER_DATABASE_PAGESIZE
    global HEADER_FILE_FORMAT_WRITE_VERSION
    global HEADER_FILE_FORMAT_READ_VERSION
    global HEADER_RESERVED_SPACE_PER_PAGE
    global HEADER_MAXIMUM_EMBEDDED_PAYLOAD_FRACTION
    global HEADER_MINIMUM_EMBEDDED_PAYLOAD_FRACTION
    global HEADER_LEAF_PAYLOAD_FRACTION
    global HEADER_FILE_CHANGE_COUNTER
    global HEADER_DATABASE_SIZE_IN_PAGES
    global HEADER_FIRST_FREE_TRUNK_PAGE
    global HEADER_TOTAL_NUMBER_OF_FREELIST_PAGES
    global HEADER_SCHEMA_COOKIE
    global HEADER_SCHEMA_FORMAT_NUMBER
    global HEADER_DEFAULT_PAGE_CACHE_SIZE
    global HEADER_LARGEST_ROOT_BTREE_PAGE_NUMBER
    global HEADER_DATABASE_TEXT_ENCODING
    global HEADER_USER_VERSION
    global HEADER_INCREMENTAL_VACCUM_MODE
    global HEADER_RESERVED_FOR_EXPANSION
    global HEADER_VERSION_VALID_FOR_NUMBER
    global HEADER_SQLITE_VERSION_NUMBER
    global HEADER_FILE_CHANGE_COUNTER_VALID

    # Parse sqlite3 header structure
    _adel_log.log("\nparseDBHeader:                ----> parsing sqlite3 database file header", 3)

    # Header bytes [0:15]: sqlite3 magic string (without null terminator, thus 15 bytes only)
    HEADER_MAGIC_STRING = _helpersStringOperations.hexstring_to_ascii(first_page_hex_string[0 * 2:15 * 2])
    if HEADER_MAGIC_STRING != "SQLite format 3":
        _adel_log.log("parse_db_header: WARNING! unknown sqlite3 magic string found: \"" + str(HEADER_MAGIC_STRING) + "\"", 2)
    else:
        _adel_log.log("parse_db_header:                      OK - sqlite3 magic string: \"" + str(HEADER_MAGIC_STRING) + "\"", 3)
    # Header bytes [16:18]: database page size
    HEADER_DATABASE_PAGESIZE = int(first_page_hex_string[16 * 2:18 * 2], 16)
    _adel_log.log("parse_db_header:                      OK - database page size: " + str(HEADER_DATABASE_PAGESIZE), 3)
    # Header byte [18:19]: file format write version (must be 1 or 2)
    HEADER_FILE_FORMAT_WRITE_VERSION = int(first_page_hex_string[18 * 2:19 * 2], 16)
    if HEADER_FILE_FORMAT_WRITE_VERSION != 1 and HEADER_FILE_FORMAT_WRITE_VERSION != 2:
        _adel_log.log("parse_db_header: WARNING! invalid file format write version (must be 1 or 2): " + str(HEADER_FILE_FORMAT_WRITE_VERSION), 2)
    else:
        _adel_log.log("parse_db_header:                      OK - file format write version (must be 1 or 2): " + str(HEADER_FILE_FORMAT_WRITE_VERSION), 3)
    # Header byte [19:20]: file format read version (must be 1 or 2)
    HEADER_FILE_FORMAT_READ_VERSION = int(first_page_hex_string[19 * 2:20 * 2], 16)
    if HEADER_FILE_FORMAT_READ_VERSION != 1 and HEADER_FILE_FORMAT_READ_VERSION != 2:
        _adel_log.log("parse_db_header: WARNING! invalid file format read version (must be 1 or 2): " + str(HEADER_FILE_FORMAT_READ_VERSION), 2)
    else:
        _adel_log.log("parse_db_header:                      OK - file format read version (must be 1 or 2): " + str(HEADER_FILE_FORMAT_READ_VERSION), 3)
    # Header byte [20:21]: reserved space per page (usually 0)
    HEADER_RESERVED_SPACE_PER_PAGE = int(first_page_hex_string[20 * 2:21 * 2], 16)
    _adel_log.log("parse_db_header:                      OK - reserved space per page (usually 0): " + str(HEADER_RESERVED_SPACE_PER_PAGE), 3)
    # Header byte [21:22]: maximum embedded payload fraction (must be 64)
    HEADER_MAXIMUM_EMBEDDED_PAYLOAD_FRACTION = int(first_page_hex_string[21 * 2:22 * 2], 16)
    if HEADER_MAXIMUM_EMBEDDED_PAYLOAD_FRACTION != 64:
        _adel_log.log("parse_db_header: WARNING! invalid maximum embedded payload fraction (must be 64): " + str(HEADER_MAXIMUM_EMBEDDED_PAYLOAD_FRACTION), 2)
    else:
        _adel_log.log("parse_db_header:                      OK - maximum embedded payload fraction (must be 64): " + str(HEADER_MAXIMUM_EMBEDDED_PAYLOAD_FRACTION), 3)
    # Header byte [22:23]: minimum embedded payload fraction (must be 32)
    HEADER_MINIMUM_EMBEDDED_PAYLOAD_FRACTION = int(first_page_hex_string[22 * 2:23 * 2], 16)
    if HEADER_MINIMUM_EMBEDDED_PAYLOAD_FRACTION != 32:
        _adel_log.log("parse_db_header: WARNING! invalid minimum embedded payload fraction (must be 32): " + str(HEADER_MINIMUM_EMBEDDED_PAYLOAD_FRACTION), 2)
    else:
        _adel_log.log("parse_db_header:                      OK - minimum embedded payload fraction (must be 32): " + str(HEADER_MINIMUM_EMBEDDED_PAYLOAD_FRACTION), 3)
    # Header byte [23:24]: leaf payload fraction (must be 32)
    HEADER_LEAF_PAYLOAD_FRACTION = int(first_page_hex_string[23 * 2:24 * 2], 16)
    if HEADER_LEAF_PAYLOAD_FRACTION != 32:
        _adel_log.log("parse_db_header: WARNING! invalid leaf payload fraction (must be 32): " + str(HEADER_LEAF_PAYLOAD_FRACTION), 2)
    else:
        _adel_log.log("parse_db_header:                      OK - leaf payload fraction (must be 32): " + str(HEADER_LEAF_PAYLOAD_FRACTION), 3)
    # Header bytes [24:28]: file change counter
    HEADER_FILE_CHANGE_COUNTER = int(first_page_hex_string[24 * 2:28 * 2], 16)
    _adel_log.log("parse_db_header:                      OK - file change counter: " + str(HEADER_FILE_CHANGE_COUNTER), 3)
    # Header bytes [28:32]: database size in pages
    HEADER_DATABASE_SIZE_IN_PAGES = int(first_page_hex_string[28 * 2:32 * 2], 16)
    # Check if database file size in header is valid
    if ((DB_FILE_SIZE_IN_BYTES / HEADER_DATABASE_PAGESIZE) != HEADER_DATABASE_SIZE_IN_PAGES):
        if HEADER_DATABASE_SIZE_IN_PAGES == 0:
            # Header field is not set (e.g. through older versions of SQLite)
            _adel_log.log("parse_db_header:                      OK - database header field for size in pages is not set (e.g. by older SQLite versions): " + str(HEADER_DATABASE_SIZE_IN_PAGES) + " pages", 3)
            HEADER_DATABASE_SIZE_IN_PAGES = DB_FILE_SIZE_IN_BYTES / HEADER_DATABASE_PAGESIZE
            _adel_log.log("                                         determined database size in pages through calculation (file size / page size): " + str(HEADER_DATABASE_SIZE_IN_PAGES) + " pages", 3)
        else:
            # Raise warning with old size
            _adel_log.log("parse_db_header: WARNING! header field for database size in pages incorrect: " + str(HEADER_DATABASE_SIZE_IN_PAGES) + " pages", 2)
            # Calculate correct size
            HEADER_DATABASE_SIZE_IN_PAGES = DB_FILE_SIZE_IN_BYTES / HEADER_DATABASE_PAGESIZE
            # Raise new size
            _adel_log.log("                        determined database size in pages through calculation (file size / page size): " + str(HEADER_DATABASE_SIZE_IN_PAGES) + " pages", 3)
    else:
        _adel_log.log("parse_db_header:                      OK - database size in pages is: " + str(HEADER_DATABASE_SIZE_IN_PAGES) + " pages", 3)
    # Header bytes [32:36]: first freelist trunk page
    HEADER_FIRST_FREE_TRUNK_PAGE = int(first_page_hex_string[32 * 2:36 * 2], 16)
    _adel_log.log("parse_db_header:                      OK - first freelist trunk page: " + str(HEADER_FIRST_FREE_TRUNK_PAGE), 3)
    # header bytes [36:40]: total number of freelist pages
    HEADER_TOTAL_NUMBER_OF_FREELIST_PAGES = int(first_page_hex_string[36 * 2:40 * 2], 16)
    _adel_log.log("parse_db_header:                      OK - total number of freelist pages: " + str(HEADER_TOTAL_NUMBER_OF_FREELIST_PAGES), 3)
    # Header bytes [40:44]: schema cookie
    HEADER_SCHEMA_COOKIE = int(first_page_hex_string[40 * 2:44 * 2], 16)
    _adel_log.log("parse_db_header:                      OK - schema cookie: " + str(HEADER_SCHEMA_COOKIE), 3)
    # Header bytes [44:48]: schema format number (must be 1-4)
    HEADER_SCHEMA_FORMAT_NUMBER = int(first_page_hex_string[44 * 2:48 * 2], 16)
    if HEADER_SCHEMA_FORMAT_NUMBER < 1 and HEADER_SCHEMA_FORMAT_NUMBER > 4:
        _adel_log.log("parse_db_header: WARNING! invalid schema format number (must be 1-4): " + str(HEADER_SCHEMA_FORMAT_NUMBER), 2)
    else:
        _adel_log.log("parse_db_header:                      OK - schema format number (must be 1-4): " + str(HEADER_SCHEMA_FORMAT_NUMBER), 3)
    # Header bytes [48:52]: default page cache size
    HEADER_DEFAULT_PAGE_CACHE_SIZE = int(first_page_hex_string[48 * 2:52 * 2], 16)
    _adel_log.log("parse_db_header:                      OK - default page cache size: " + str(HEADER_DEFAULT_PAGE_CACHE_SIZE), 3)
    # Header bytes [52:56]: largest root b-tree page number
    HEADER_LARGEST_ROOT_BTREE_PAGE_NUMBER = int(first_page_hex_string[52 * 2:56 * 2], 16)
    _adel_log.log("parse_db_header:                      OK - largest root b-tree page number: " + str(HEADER_LARGEST_ROOT_BTREE_PAGE_NUMBER), 3)
    # Header bytes [56:60]: database text encoding (must be 1-3)
    HEADER_DATABASE_TEXT_ENCODING = int(first_page_hex_string[56 * 2:60 * 2], 16)
    if HEADER_DATABASE_TEXT_ENCODING < 1 and HEADER_SCHEMA_FORMAT_NUMBER > 3:
        _adel_log.log("parse_db_header: WARNING! invalid database text encoding (must be 1-3): " + str(HEADER_DATABASE_TEXT_ENCODING), 2)
    else:
        _adel_log.log("parse_db_header:                      OK - database text encoding (must be 1-3): " + str(HEADER_DATABASE_TEXT_ENCODING), 3)
    # Header bytes [60:64]: user version
    HEADER_USER_VERSION = int(first_page_hex_string[60 * 2:64 * 2], 16)
    _adel_log.log("parse_db_header:                      OK - user version: " + str(HEADER_USER_VERSION), 3)
    # header bytes [64:68]: incremental-vacuum mode (1, zero otherwise)
    HEADER_INCREMENTAL_VACCUM_MODE = int(first_page_hex_string[64 * 2:68 * 2], 16)
    if HEADER_INCREMENTAL_VACCUM_MODE != 0 and HEADER_INCREMENTAL_VACCUM_MODE != 1:
        _adel_log.log("parse_db_header: WARNING! invalid incremental-vacuum mode (1, zero otherwise): " + str(HEADER_INCREMENTAL_VACCUM_MODE), 2)
    else:
        _adel_log.log("parse_db_header:                      OK - incremental-vacuum mode (1, zero otherwise): " + str(HEADER_INCREMENTAL_VACCUM_MODE), 3)
    # Header bytes [68:92]: reservation for expansion (must be 0)
    HEADER_RESERVED_FOR_EXPANSION = int(first_page_hex_string[68 * 2:92 * 2], 16)
    if HEADER_RESERVED_FOR_EXPANSION != 0:
        _adel_log.log("parse_db_header: WARNING! invalid reservation for expansion (must be 0): " + str(HEADER_RESERVED_FOR_EXPANSION), 2)
    else:
        _adel_log.log("parse_db_header:                      OK - reservation for expansion (must be 0): " + str(HEADER_RESERVED_FOR_EXPANSION), 3)
    # Header bytes [92:96]: version valid for number
    HEADER_VERSION_VALID_FOR_NUMBER = int(first_page_hex_string[92 * 2:96 * 2], 16)
    _adel_log.log("parse_db_header:                      OK - version valid for number: " + str(HEADER_VERSION_VALID_FOR_NUMBER), 3)
    # Header bytes [96:100]: sqlite version number
    HEADER_SQLITE_VERSION_NUMBER = int(first_page_hex_string[96 * 2:100 * 2], 16)
    _adel_log.log("parse_db_header:                      OK - sqlite version number: " + str(HEADER_SQLITE_VERSION_NUMBER), 3)

    # Check whether the file change counter is valid
    if (HEADER_FILE_CHANGE_COUNTER == HEADER_VERSION_VALID_FOR_NUMBER):
        # field valid
        HEADER_FILE_CHANGE_COUNTER_VALID = 0
    else:
        # Field not valid
        HEADER_FILE_CHANGE_COUNTER_VALID = 1

    _adel_log.log("parse_db_header:                ----> sqlite3 database file header parsed", 3)


#-----------------Example-------------------
#if __name__ == "__main__":
#    # Set date and time
#    DATE     = str(datetime.datetime.today()).split(' ')[0]
#    TIME     = str(datetime.datetime.today()).split(' ')[1].split('.')[0].split(':')
#    log_file  = DATE + "__" + TIME[0] + "-" + TIME[1] + "-" + TIME[2] + "__sqliteParser.log"
#    _adel_log.FILE_HANDLE = open(log_file, "a+")
#
#    # Check database file name
#    number_of_args = len(sys.argv[1:])
#    if number_of_args > 0:
#        file_name = sys.argv[1]
#    else:
#        _adel_log.log("_sqliteParser: WARNING! no database file given --> using test database \"sql3_test.db\"", 2)
#        # initialize the db file for testing purposes if not given as command line argument
#        file_name = "sql3_test.db"
#    if number_of_args > 1:
#        _adel_log.LOG_LEVEL_GLOBAL = sys.argv[2]
#    else:
#        _adel_log.LOG_LEVEL_GLOBAL = 4
#
#    parse_db(file_name)
#
#    # Test databases
#    file_names = []
#    file_names.append(file_name)
#    #file_names.append("sql3_test.db")
#    #file_names.append("contacts.db")
#
#    file_names.append("testDBs/T1_cal.sqlite")
#    file_names.append("testDBs/T2_cookies.sqlite")
#    file_names.append("testDBs/T3_dl.sqlite")
#    file_names.append("testDBs/T4_global-messages.sqlite")
#    file_names.append("testDBs/T5_urls.sqlite")
#
#    file_names.append("testDBs/SE_01_account.db")
#    file_names.append("testDBs/SE_02_user_dict.db")
#    file_names.append("testDBs/SE_03_calendar.db")
#    file_names.append("testDBs/SE_04_contacts.db")
#    file_names.append("testDBs/SE_05_downloads.db")
#    file_names.append("testDBs/SE_06_settings.db")
#    file_names.append("testDBs/SE_07_mmssms.db")
#    file_names.append("testDBs/SE_08_telephony.db")
#
#    file_names.append("testDBs/1_accounts.db")
#    file_names.append("testDBs/2_alarms.db")
#    file_names.append("testDBs/3_auto_dict.db")
#    file_names.append("testDBs/4_calender.db")
#    file_names.append("testDBs/5_colornote.db")
#    file_names.append("testDBs/6_contacts2.db")
#    file_names.append("testDBs/7_downloads.db")
#    file_names.append("testDBs/8_EmailProvider.db")
#    file_names.append("testDBs/9_gmail.db")
#    file_names.append("testDBs/11_mailstore.spreitzenbarth-at-googlemail.com.db")
#    file_names.append("testDBs/22_mmssms.db")
#    file_names.append("testDBs/33_talk.db")
#    file_names.append("testDBs/44_telephony.db")
#    file_names.append("testDBs/55_twitter.db")
#    file_names.append("testDBs/66_user_dict.db")
#    file_names.append("testDBs/77_weather.db")
#
#    for file_name in file_names:
#        _adel_log.log("parseDBs:      ----> starting to parse " + str(file_name), 0)
#        result_list = parse_db(file_name)
#        # output to log for test purposes only
#        if result_list != 1:
#            i = 1
#            for result in result_list:
#                _adel_log.log("\nparseDBs:      ----> printing DATABASE ELEMENT " + str(i) + " for test purposes....", 0)
#                _adel_log.log(str(result), 0)
#                i += 1
#        else:
#            _adel_log.log("parseDBs: ERROR! could not parse database file \"" + str(file_name) + "\"", 1)
#    _adel_log.log("\nparseDBs:      ----> all SQLite databases parsed", 0)
#    _adel_log.log("", 3)
#-----------------Example-------------------