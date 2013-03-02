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

import _adel_log
import _sqliteFileHandler
import _sqliteVarInt
import _helpersBinaryOperations
import _helpersStringOperations

# Parses a b-tree page and returns any content that is contained in this b-tree page
# or in child b-tree pages of this page (if it is an interior btree page). This function
# parses a complete b-tree if the b-tree root page is passed in as pageHexString.
# @page_hex_stng:       complete page as hexadecimal string
# @page_offset          header offset in pageHexString (decimal, in bytes)
# @return:              list of contents contained in this page or child b-tree pages
#                       or an empty list if the page has an invalid page type
def parse_table_btree_page(page_hex_string, page_offset):
    # Parse the page header
    page_type = int(page_hex_string[(page_offset * 2):((page_offset + 1) * 2)], 16)
    #if (page_type == 2):
        # index b-tree interior page
        # TODO: define and implement parseIndexBTreeInteriorCell() (do the methods for TABLES also work for INDICES?)
        # IGNORED RIGHT NOW
    if (page_type == 5):
        # table b-tree interior page
        return parse_table_btree_interior_page(page_hex_string, page_offset)
    #if (page_type == 10):
        # index b-tree leaf page
        # TODO: define and implement parseIndexBTreeLeafCell() (do the methods for TABLES also work for INDICES?)
        # IGNORED RIGHT NOW
    if (page_type == 13):
        # Table b-tree leaf page
        return parse_table_btree_leaf_page(page_hex_string, page_offset)

    _adel_log.log("parse_table_btree_page: ERROR - invalid page type in table b-tree page header", 1)
    _adel_log.log("                     Page header was said to start at page offset: " + str(page_offset), 1)
    _adel_log.log("                     Printing page content....", 1)
    _adel_log.log(page_hex_string, 1)
    return []


# Parses a table b-tree interior page and returns any content that is contained
# in this b-tree page or in child b-tree pages of this page.
# @page_hex_string:       complete page as hexadecimal string
# @page_offset:          header offset in page_hex_string (decimal, in bytes)
# @return:              list of contents contained in this page or child b-tree pages
#                       or an empty list if the page has an invalid page type
def parse_table_btree_interior_page(page_hex_string, page_offset):
    # Parse the page header
    header = parse_btree_page_header(page_hex_string, page_offset)

    # Ensure that we deal with a correct page
    header_length = len(header)
    if (header_length != 7 or header[0] != 5):
        # No valid header_length
        _adel_log.log("parse_table_btree_interior_page: ERROR - invalid page type in table b-tree interior page header", 1)
        _adel_log.log("                             Page header was said to start at page offset: " + str(page_offset), 1)
        _adel_log.log("                             Printing page content....", 1)
        _adel_log.log(page_hex_string, 1)
        return []

    # initialize resulting list
    content_list = []
    # Initialize node list
    node_pointers = []
    # Initialize page content list
    page_contents = []
    # Parse cell pointer array
    cell_pointers = parse_cell_pointer_array(page_hex_string, (page_offset + header[header_length - 1]), header[2])
    # Parse cells
    for cell_pointer in cell_pointers:
        node_pointers.append(parse_table_btree_interior_cell(page_hex_string, cell_pointer))
    # This is an interior page, thus we append the right-most pointer as well
    node_pointers.append([header[5], 0])

    # Iterate through every node
    for node_tuple in node_pointers:
        _adel_log.log("parse_table_btree_interior_page:  ----> fetching child page to parse, page number: " + str(node_tuple[0]) + "....", 3)
        child_page = _sqliteFileHandler.read_page(node_tuple[0])

        # Ensure we fetched a valid page
        if (child_page == ""):
            _adel_log.log("parse_table_btree_interior_page: ERROR - invalid node tuple detected, cannot reference child page pointer: " + str(node_tuple), 1)
            continue
        # Parse child pages
        page_contents = parse_table_btree_page(child_page, 0)
        for page_content in page_contents:
            content_list.append(page_content)
        _adel_log.log("parse_table_btree_interior_page:  ----> child page parsed, page number: " + str(node_tuple[0]) + "....", 4)

    return content_list



# Parses a table b-tree leaf page and returns any content that is contained
# in this page and possible cell payload overflow pages.
# @page_hex_string:       complete page as hexadecimal string
# @page_offset:           header offset in page_hex_string (decimal, in bytes)
# @return:                list of content lists
def parse_table_btree_leaf_page(page_hex_string, page_offset):
    # Parse the page header
    header = parse_btree_page_header(page_hex_string, page_offset)

    # Ensure that we deal with a correct page
    headerLength = len(header)
    if (headerLength != 6 or header[0] != 13):
        # no valid headerLength
        _adel_log.log("parse_table_btree_leaf_page: ERROR - invalid page type in table b-tree leaf page header", 1)
        _adel_log.log("                         Page header was said to start at page offset: " + str(page_offset), 1)
        _adel_log.log("                         Printing page content....", 1)
        _adel_log.log(page_hex_string, 1)
        return []

    # Initialize resulting list
    content_list = []

    # Parse cell pointer array
    cell_pointers = parse_cell_pointer_array(page_hex_string, (page_offset + header[headerLength - 1]), header[2])

    # parse cells
    for cell_pointer in cell_pointers:
        content_list.append(parse_table_btree_leaf_cell(page_hex_string, cell_pointer, cell_pointers, header[1]))

    return content_list



# Parses the b-tree page header structure of the given b-tree page and returns the header
# fields as seperated elements in a list. A b-tree header is defined to have the
# following format:
# 1st element:          flag that defines the b-tree page type
# 2nd element:          byte offset into the page of the first freeblock
# 3rd element:          number of cells on this page
# 4th element:          offset to the first byte of the cell content area
# 5th element:          number of fragmented freebytes within the cell content area
# [6th element:]        right-most pointer (interior b-tree pages only)
# last (6/7th) element: length of the header structure in bytes (determines where the cell pointer array starts)
#
# @page_hex_string:     complete page as hexadecimal string
# @page_offset:         header offset in page_hex_string (decimal, in bytes)
# @return:              list of strings that contains the header elements as defined above
def parse_btree_page_header(page_hex_string, page_offset):
    # 1 byte is represented by two characters in the hexString, so internally we need to calculate the offset in nibbles
    page_offset = page_offset * 2

    # Parse sqlite b-tree header structure
    _adel_log.log("parse_btree_page_header:         ----> parsing b-tree page header structure....", 4)
    # B-tree header byte 0: b-tree page type
    btree_page_type = int(page_hex_string[(page_offset + 0):(page_offset + 2)], 16)
    if btree_page_type in (2, 5, 10, 13):
        _adel_log.log("parse_btree_page_header:               OK - sqlite b-tree page type (must be 2,5,10 or 13): %(btree_page_type)s" % vars(), 4)
    else:
        _adel_log.log("parse_btree_page_header: WARNING! - invalid sqlite b-tree page type (must be 2,5,10 or 13): %(btree_page_type)s" % vars(), 2)
    # B-tree header bytes 1-2: bytes offset into the page of the first freeblock
    btree_number_of_bytes_offset_in_first_free_block = int(page_hex_string[(page_offset + 2):(page_offset + 6)], 16)
    _adel_log.log("parse_btree_page_header:               OK - bytes offset into the page of the first freeblock: %(btree_number_of_bytes_offset_in_first_free_block)s" % vars(), 4)
    # B-tree header bytes 3-4: number of cells on this page
    btree_number_of_cells = int(page_hex_string[(page_offset + 6):(page_offset + 10)], 16)
    _adel_log.log("parse_btree_page_header:               OK - number of cells on this page: %(btree_number_of_cells)s" % vars(), 4)
    # B-tree header bytes 5-6: offset of the first byte of cell content area
    btree_offset_of_first_byte_content = int(page_hex_string[(page_offset + 10):(page_offset + 14)], 16)
    _adel_log.log("parse_btree_page_header:               OK - offset of the first byte of cell content area: %(btree_offset_of_first_byte_content)s" % vars(), 4)
    # B-tree header byte 7: number of fragmented free bytes
    btree_number_of_fragmented_free_bytes = int(page_hex_string[(page_offset + 14):(page_offset + 16)], 16)
    _adel_log.log("parse_btree_page_header:               OK - number of fragmented free bytes: %(btree_number_of_fragmented_free_bytes)s" % vars(), 4)

    # Build list of well defined header elements
    header_elements = [btree_page_type, btree_number_of_bytes_offset_in_first_free_block, btree_number_of_cells, btree_offset_of_first_byte_content, btree_number_of_fragmented_free_bytes]

    # check for optional header element 6: right-most pointer
    # b-tree header bytes 8-11: right-most pointer if page is an interior b-tree page
    if btree_page_type == 2 or btree_page_type == 5:
        btree_right_most_pointer = int(page_hex_string[(page_offset + 16):(page_offset + 24)], 16)
        header_elements.append(btree_right_most_pointer)
        length = 12
        _adel_log.log("parse_btree_page_header:               OK - right-most pointer: %(btree_right_most_pointer)s" % vars(), 4)
    else:
        length = 8
        _adel_log.log("parse_btree_page_header:               OK - page is a b-tree leaf page and thus does not include a right-most pointer", 4)

    # Return list of header elements
    header_elements.append(length)
    _adel_log.log("parse_btree_page_header:               OK - returning list of header elements: %(header_elements)s" % vars(), 3)
    _adel_log.log("parse_btree_page_header:         ----> b-tree page header structure parsed", 4)
    return header_elements


# Parses the cell pointer array of a b-tree page returns it's elements in a list.
# @page_hex_string:       complete page as hexadecimal string
# @page_offset:          cell pointer array offset in page_hex_string (decimal, in bytes)
# @elements:            number of cell pointer array elements
# @return:              list of cell pointer array elements (order corresponds to the order in the database file)
def parse_cell_pointer_array(pageHexString, pageOffset, elements):
    # 1 byte is represented by two characters in the hexString, so internally we need to calculate the offset in nibbles
    pageOffset = pageOffset * 2

    _adel_log.log("parse_cell_pointer_array:        ----> parsing b-tree page cell pointer array....", 4)
    cell_pointers = []
    i = 4
    while i <= (elements * 4): # times 4, because a cell pointer element is a 2-byte integer (= 4 nibbles and 4 characters in pageHexString)
        current_pointer = int(pageHexString[pageOffset + (i - 4):(pageOffset + i)], 16)
        _adel_log.log("parse_cell_pointer_array:              OK - append cell pointer to list: %(current_pointer)s" % vars(), 4)
        cell_pointers.append(current_pointer)
        i += 4
    _adel_log.log("parse_cell_pointer_array:              OK - returning list of cell pointers: %(cell_pointers)s" % vars(), 3)
    _adel_log.log("parse_cell_pointer_array:        ----> b-tree page cell pointer array parsed", 4)
    return cell_pointers



# Parses the free blocks of a b-tree page and returns the
# offsets and lengths of free blocks in a list of tuples.
# @page_hex_string:             complete page as hexadecimal string
# @next_free_block_pointer      pointer to the first free block in pageHexString (decimal, in bytes)
# @return:                      list of free block tuples in the format: [free block offsets, free block length]
def parse_free_blocks(page_hex_strings, next_free_block_pointer):
    # Check whether there are any free blocks on this page
    if (next_free_block_pointer == 0):
        # No free blocks on this page
        return []

    # Parse the free block list
    _adel_log.log("parse_free_blocks:              ----> parsing b-tree page free block chain....", 4)
    free_blocks = []
    while (next_free_block_pointer != 0):
        # We have a free block in the chain
        free_blocks.append([next_free_block_pointer, int(page_hex_strings[((next_free_block_pointer + 2) * 2):((next_free_block_pointer + 4) * 2)], 16)])
        _adel_log.log("parse_free_blocks:                    OK - append free block tuple to list [offset, length]: %(next_free_block_pointer)s" % vars(), 4)
        next_free_block_pointer = int(page_hex_strings[(next_free_block_pointer * 2):((next_free_block_pointer + 2) * 2)], 16)

    # Return results
    _adel_log.log("parse_free_blocks:                    OK - returning list of free block pointers: %(free_blocks)s" % vars(), 3)
    _adel_log.log("parse_free_blocks:              ----> b-tree page free block chain parsed", 4)
    return free_blocks


# Parses a complete table b-tree interior cell that is supposed to start at the given
# offset (relativ to the beginning of the page). The cell content is returned in a list.
# Any table b-tree interior cell is defined to have the following structure:
# 1. 4-byte big-endian integer for the page number of the left child
# 2. varint for row-id (integer key)
#
# @page_hex_strings:       complete page as hexadecimal string
# @page_offse  t:          cell offset in page_hex_strings (decimal, in bytes)
# @return:                 tuple (list with exactly two elements) containing the node contents (pointer to left child, row ID)
def parse_table_btree_interior_cell(page_hex_string, page_offset):
    # 1 byte is represented by two characters in the hexString, so internally we need to calculate the offset in nibbles
    page_offset_in_bytes = page_offset # store for log reasons only
    page_offset = page_offset * 2 # now dealing with nibbles because we treat a string (1 character = 1 nibble)

    _adel_log.log("parse_table_btree_interior_cell:  ----> parsing b-tree interior cell at offset %(page_offset_in_bytes)s...." % vars(), 4)

    # Get total number of bytes of payload
    left_child_pointer = int(page_hex_string[page_offset:(page_offset + (4 * 2))], 16)
    _adel_log.log("parse_table_btree_interior_cell:        OK - left child pointer is: %(left_child_pointer)s" % vars(), 4)
    # Get row_id
    row_id_string = page_hex_string[(page_offset + (4 * 2)):(page_offset + ((4 + 9) * 2))]
    row_id_tuple = _sqliteVarInt.parse_next_var_int(row_id_string)
    row_id = row_id_tuple[0]
    _adel_log.log("parse_table_btree_interior_cell:  ----> row_id (index) is: %(row_id)s...." % vars(), 4)

    # Build tuple of node contents
    node_tuple = [left_child_pointer, row_id]
    _adel_log.log("parse_table_btree_interior_cell:        OK - returning tuple of node content: %(node_tuple)s" % vars(), 4)
    _adel_log.log("parse_table_btree_interior_cell:  ----> b-tree interior cell at offset %(page_offset_in_bytes)s parsed" % vars(), 4)
    return node_tuple


# Parses a complete table b-tree leaf cell that is supposed to start at the given
# offset (relativ to the beginning of the page). The cell content is returned in a list.
# Any table b-tree leaf cell is defined to have the following structure:
# 1. varint for total number of bytes of payload
# 2. varint for row-id (integer key)
# 3. sqlite record (payload) that does not spill to overflow pages
# 4. [optional 4-byte big-endian integer page number for the first page of the overflow page list]
#
# @page_hex_string:       complete page as hexadecimal string
# @page_offset:          cell offset in page_hex_string (decimal, in bytes)
# @cell_pointers:        cell pointer array corresponding to this cell pointer
# @free_block_pointer:    pointer to the first free block in the page
# @return:              list of extracted contents or empty list if no contents could be retrieved
def parse_table_btree_leaf_cell(page_hex_string, page_offset, cell_pointers, free_block_pointer):
    # 1 byte is represented by two characters in the hexString, so internally we need to calculate the offset in nibbles
    page_offset_in_bytes = page_offset # store for log reasons only
    page_offset = page_offset * 2 # now dealing with nibbles because we treat a string (1 character = 1 nibble)
    db_page_size_in_bytes = _sqliteFileHandler.DB_PAGESIZE_IN_BYTES
    usable_page_space = db_page_size_in_bytes - _sqliteFileHandler.DB_RESERVED_SPACE

    _adel_log.log("parse_table_btree_leaf_cell:      ----> parsing b-tree leaf cell at offset %(page_offset_in_bytes)s...." % vars(), 4)

    # Get total number of bytes of payload
    bytes_of_payload_tuple = _sqliteVarInt.parse_next_var_int(page_hex_string[page_offset:(page_offset + 18)]) # a variable integer can be maximum 9 byte (= 18 nibbles) long
    bytes_of_payload = bytes_of_payload_tuple[0]
    _adel_log.log("parse_table_btree_leaf_cell:            OK - payload is %(bytes_of_payload)s bytes long" % vars(), 4)
    # Get row_id
    row_id_string = page_hex_string[(page_offset + (bytes_of_payload_tuple[1] * 2)):(page_offset + (bytes_of_payload_tuple[1] + 9) * 2)]
    row_id_tuple = _sqliteVarInt.parse_next_var_int(row_id_string)
    row_id = row_id_tuple[0]
    _adel_log.log("parse_table_btree_leaf_cell:      ----> extracting contents for row_id %(row_id)s...." % vars(), 4)

    # Check for overflow pages and append content of those pages, if any
    # Calculate the overflow limits for table b-tree leaf cell
    remaining_page_space = db_page_size_in_bytes - page_offset_in_bytes
    if (bytes_of_payload > (remaining_page_space)):
        # We expext content to overflow, because there is not enough space left on this page
        _adel_log.log("parse_table_btree_leaf_cell:            OK - payload is too large for this page, there are overflow pages" % vars(), 4)

        # Check at which position the next cell starts
        next_cell = usable_page_space
        for cell_pointer in cell_pointers:
            if (cell_pointer > page_offset_in_bytes) and (cell_pointer < next_cell):
                next_cell = cell_pointer

        # Check at which position the next freeblock starts (we ignore theoretically possible freebytes in this case,
        # Because we expect no freebyte at the end of a cell that overflows to another page
        next_free_block = usable_page_space
        free_blocks = parse_free_blocks(page_hex_string, free_block_pointer)
        for free_block in free_blocks:
            if (free_block[0] > page_offset_in_bytes) and (free_block[0] < next_free_block):
                next_free_block = free_block[0]

        # Get the end of this record: either closest following cell or closest following freeblock or end of page
        end_of_record = usable_page_space
        # Check of the end of this record is given through a following cell
        if (next_cell != usable_page_space) and ((next_cell <= next_free_block) or (next_free_block == usable_page_space)):
            # next element is not end of page but a cell
            end_of_record = next_cell
        # Check of the end of this record is given through a following free block
        if (next_free_block != usable_page_space) and ((next_free_block < next_cell) or (next_cell == usable_page_space)):
            # Next element is not end of page but a free block
            end_of_record = next_free_block

        # Cut record hex string from the beginning to the offset of the next following element
        record_hex_string = page_hex_string[(page_offset + ((bytes_of_payload_tuple[1] + row_id_tuple[1]) * 2)):(end_of_record * 2)]
        record_hex_string_length = len(record_hex_string) / 2 # string length is count in nibbles, we need bytes here

        # Save overflow page pointer at the end of record hex string
        first_overflow_page_number = int(record_hex_string[((record_hex_string_length - 4) * 2):(record_hex_string_length * 2)], 16)
        _adel_log.log("parse_table_btree_leaf_cell:      ----> parsing overflow page chain beginning at page %(first_overflow_page_number)s...." % vars(), 4)
        # Cut off overflow page number from record_hex_string
        record_hex_string = record_hex_string[(0):((record_hex_string_length - 4) * 2)]

        first_overflow_page_string = _sqliteFileHandler.read_page(first_overflow_page_number)
        # Ensure that read page could retrieve an existing page
        if (first_overflow_page_string == ""):
            _adel_log.log("parse_table_btree_leaf_cell: ERROR - invalid overflow page pointer, cannot reference first overflow page: " + str(first_overflow_page_number), 1)
            return []
        # Append content from overflow pages
        record_hex_string += parse_overflow_page_chain(first_overflow_page_string)

        # Ensure correct length of string (maybe not all bytes of the last overflow page in the chain contain content)
        record_hex_string_length = len(record_hex_string) / 2 # string length is count in nibbles, we need bytes here
        if (bytes_of_payload < record_hex_string_length):
            # Cut record hex string again
            record_hex_string = record_hex_string[:bytes_of_payload * 2]
    else:
        # The entire payload is stored on this page
        record_hex_string = page_hex_string[(page_offset + ((bytes_of_payload_tuple[1] + row_id_tuple[1]) * 2)):(page_offset + ((bytes_of_payload_tuple[1] + row_id_tuple[1] + bytes_of_payload_tuple[0]) * 2))]

    # Parse the record
    read_content_list = parse_record(record_hex_string)
    # Build the resulting list (including the row_id used sqlite internally)
    cell_content_list = []
    cell_content_list.append(row_id)
    for element in range(len(read_content_list)):
        cell_content_list.append(read_content_list[element])
    # Return results
    _adel_log.log("parse_table_btree_leaf_cell:            OK - returning list of cell contents", 4)
    _adel_log.log("parse_table_btree_leaf_cell:      ----> b-tree leaf cell at offset %(page_offset_in_bytes)s parsed" % vars(), 4)
    return cell_content_list


# Parses the complete overflow page chain (occures only in table b-trees) including possible further overflow
# paged and returns the compete content of the record that is sotred on the overflow page chain.
# @page_hex_string:       content of the overflow page as hexadecimal string
# @return:		content contained in this and child overflow pages as hexadecimal string
def parse_overflow_page_chain(page_hex_string):
    if (len(page_hex_string) == 0):
        _adel_log.log("parse_overflow_page_chain: WARNING! empty hexadecimal page string received", 2)
        return ""
    if (len(page_hex_string) < 8):
        _adel_log.log("parse_overflow_page_chain: WARNING! hexadecimal page string is too short: " + str(page_hex_string), 2)
        return ""

    # Check whether there is another overflow page: first 8 nibbles is 4-byte integer pointer to next overflow page or 00 00 00 00 if no further overflow page exists
    next_overflow_page_number = int(page_hex_string[0:8], 16) # will be zero if we reached the last overflow page in the chain

    # Build content string: append all content of this page
    overflow_page_content = page_hex_string[8:]
    _adel_log.log("parse_overflow_page_chain:             OK - overflow page parsed" % vars(), 4)

    if next_overflow_page_number != 0:
        # There is at least one more overflow page: append further content
        _adel_log.log("parse_overflow_page_chain:             ----> parsing next overflow page in chain, page number is: %(next_overflow_page_number)s...." % vars(), 4)
        overflow_page_content += parse_overflow_page_chain(_sqliteFileHandler.read_page(next_overflow_page_number))

    return overflow_page_content


# Parses a complete sqlite3 record structure and returns the extracted contents in a list.
# If the given record corresponds to a complete row in the sqlite table, then each element
# in the returned list corresponds to an entry in a column of that row.
# @record_hex_string:     complete record as hexadecimal string
# @return:		ordered list of record contents (first column first, last column last)
def parse_record(record_hex_string):
    # parse the record header
    _adel_log.log("parse_record:                  ----> parsing record header....", 4)
    header_length_tuple = _sqliteVarInt.parse_next_var_int(record_hex_string[0:18])
    header_string = record_hex_string[(header_length_tuple[1] * 2):(header_length_tuple[0] * 2)]
    record_header_field_list = _sqliteVarInt.parse_all_var_ints(header_string)
    _adel_log.log("parse_record:                        OK - record header field list is %(record_header_field_list)s" % vars(), 4)

    # Get the record content
    content_offset = header_length_tuple[0] * 2
    content_list = []
    element = 0
    for var_int in record_header_field_list:
        entry_content = parse_content_entry(record_header_field_list[element], record_hex_string, content_offset)
        content_list.append(entry_content[0])
        content_offset += entry_content[1] * 2
        element += 1

    # Return the record content list
    _adel_log.log("parse_record:                        OK - returning list of record contents", 4)#: %(content_list)s" %vars(), 4)
    _adel_log.log("parse_record:                  ----> record header parsed", 4)
    return content_list

# Extracts the content of the given serial type and returns a tuple (list with
# exactly two elements) with the entry content as first element and the length
# of the entry as second element.
# @serialType:		corresponding integer value in the record header
# @record_hex_string:     hexadecimal string of the sqlite3 record
# @content_offset:       offset of the content in record_hex_string
# @return:		tuple containing the content and the it's lenght in bytes
def parse_content_entry(serial_type, record_hex_string, content_offset):
    # initial checks
    if serial_type < 0:
    	_adel_log.log("getEntryContent: WARNING! invalid serial type (must be >= 0): %(serial_type)s" % vars(), 2)
	return None

    _adel_log.log("getEntryContent:              ----> retrieving serial type content at relative offset: %(content_offset)s...." % vars(), 4)

    # Initialise result list
    entry_content_list = []

    if (serial_type == 0):
        # Defined as NULL, zero bytes in length
        entry_content_list.append(None)
        entry_content_list.append(0)
        _adel_log.log("getEntryContent:                    OK - serial type is: NULL, zero bytes in length", 4)
        return entry_content_list
    if (serial_type == 1):
        entryContent = _helpersBinaryOperations.twos_complement_to_int(int(record_hex_string[(content_offset):(content_offset + 2)], 16), 1 * 8)
        entry_content_list.append(entryContent)
        entry_content_list.append(1)
        _adel_log.log("getEntryContent:                    OK - serial type is: 8-bit twos-complement integer: %(entryContent)s" % vars(), 4)
        return entry_content_list
    if (serial_type == 2):
        entryContent = _helpersBinaryOperations.twos_complement_to_int(int(record_hex_string[(content_offset):(content_offset + 4)], 16), 2 * 8)
        entry_content_list.append(entryContent)
        entry_content_list.append(2)
        _adel_log.log("getEntryContent:                    OK - serial type is: Big-endian 16-bit twos-complement integer: %(entryContent)s" % vars(), 4)
        return entry_content_list
    if (serial_type == 3):
        entryContent = _helpersBinaryOperations.twos_complement_to_int(int(record_hex_string[(content_offset):(content_offset + 6)], 16), 3 * 8)
        entry_content_list.append(entryContent)
        entry_content_list.append(3)
        _adel_log.log("getEntryContent:                    OK - serial type is: Big-endian 24-bit twos-complement integer: %(entryContent)s" % vars(), 4)
        return entry_content_list
    if (serial_type == 4):
        entryContent = _helpersBinaryOperations.twos_complement_to_int(int(record_hex_string[(content_offset):(content_offset + 8)], 16), 4 * 8)
        entry_content_list.append(entryContent)
        entry_content_list.append(4)
        _adel_log.log("getEntryContent:                    OK - serial type is: Big-endian 32-bit twos-complement integer: %(entryContent)s" % vars(), 4)
        return entry_content_list
    if (serial_type == 5):
        entryContent = _helpersBinaryOperations.twos_complement_to_int(int(record_hex_string[(content_offset):(content_offset + 12)], 16), 6 * 8)
        entry_content_list.append(entryContent)
        entry_content_list.append(6)
        _adel_log.log("getEntryContent:                    OK - serial type is: Big-endian 48-bit twos-complement integer: %(entryContent)s" % vars(), 4)
        return entry_content_list
    if (serial_type == 6):
        entryContent = _helpersBinaryOperations.twos_complement_to_int(int(record_hex_string[(content_offset):(content_offset + 16)], 16), 8 * 8)
        entry_content_list.append(entryContent)
        entry_content_list.append(8)
        _adel_log.log("getEntryContent:                    OK - serial type is: Big-endian 64-bit twos-complement integer: %(entryContent)s" % vars(), 4)
        return entry_content_list
    if (serial_type == 7):
        entryContent = struct.unpack('d', struct.pack('Q', int(record_hex_string[(content_offset):(content_offset + 16)], 16)))[0]
        entry_content_list.append(entryContent)
        entry_content_list.append(8)
        _adel_log.log("getEntryContent:                    OK - serial type is: Big-endian IEEE 754-2008 64-bit floating point number: %(entryContent)s" % vars(), 4)
        return entry_content_list
    if (serial_type == 8):
        # Integer constant 0 (only schema format > 4), zero bytes in length
        entry_content_list.append(0)
        entry_content_list.append(0)
        _adel_log.log("getEntryContent:                    OK - serial type is an integer constant: 0, zero bytes in length", 4)
        return entry_content_list
    if (serial_type == 9):
        # Integer constant 1 (only schema format > 4), zero bytes in length
        entry_content_list.append(1)
        entry_content_list.append(0)
        _adel_log.log("getEntryContent:                    OK - serial type is an integer constant: 1, zero bytes in length", 4)
        return entry_content_list
    if (serial_type == 10):
        # Not used, reserved for expansion
    	_adel_log.log("getEntryContent: WARNING! invalid serial type (not used, reserved for expansion): %(serial_type)s" % vars(), 2)
        entry_content_list.append(None)
        entry_content_list.append(0)
        return entry_content_list
    if (serial_type == 11):
        # Not used, reserved for expansion
    	_adel_log.log("getEntryContent: WARNING! invalid serial type (not used, reserved for expansion): %(serial_type)s" % vars(), 2)
        entry_content_list.append(None)
        entry_content_list.append(0)
        return entry_content_list
    if (serial_type >= 12):
        # either a STRING or a BLOB
        entrySize = determine_serial_type_content_size(serial_type)
        entryContent = record_hex_string[(content_offset):(content_offset + (entrySize * 2))]
        # build return list
        entry_content_list.append(_helpersStringOperations.hexstring_to_ascii(entryContent))
        entry_content_list.append(entrySize)
        return entry_content_list



# Returns the size of the content for sqlite3 record serial types greater than 12
# @serial_type:		integer value that represents the serial type
# @return:		length of serialType in bytes
def determine_serial_type_content_size(serial_type):
    if serial_type < 12:
        _adel_log.log("determine_serial_type_content_size: WARNING! invalid serial type (must be >= 12): %(serial_type)s" % vars(), 2)
        return 1 # at least one byte has an invalid serial type, thus return 1 so the program has a chance to continue with the next byte
    else:
        if serial_type % 2 == 0:
            # serial_type is an even number = String in the database
            serialTypeLength = (serial_type - 12) / 2
            _adel_log.log("determine_serial_type_content_size:     OK - serial type is a STRING of length: %(serialTypeLength)s" % vars(), 4)
            return serialTypeLength
        else:
            # serial_type is an odd number = BLOB in the database
            serialTypeLength = (serial_type - 13) / 2
            _adel_log.log("determine_serial_type_content_size:     OK - serial type is a BLOB of length: %(serialTypeLength)s" % vars(), 4)
            return serialTypeLength


#-----------------Example-------------------
#if __name__ == "__main__":
#    db = open("sql3_test.db", "rb")
#    db.seek(0, 0)
#    print parseBTreeHeader(db.read(1024), 100)
#    db.close()
#-----------------Example-------------------