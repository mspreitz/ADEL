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

import _helpersBinaryOperations

# Returns a list of all variable integers found in the given hexadecimal string.
# The order of the variable integers in the resutling list corresponds to their
# order in the string.
# @hex_string:           hexadecimal string containing one or more variable integers
# @return:		list of all variable integers found in hexString
def parse_all_var_ints(hex_string):
    length = len(hex_string)
    list_of_var_ints = []

    # Iterate through hex_string
    position = 0
    var_int_tuple = []
    while position < length:
        var_int_tuple = parse_next_var_int(hex_string[position:])
        if var_int_tuple != None:
            list_of_var_ints.append(var_int_tuple[0])
            position += (var_int_tuple[1] * 2)
        else:
            position += 1
    return list_of_var_ints


# Determines the next variable integer structure (up to 9 bytes) in the given
# hexadecimal string and returns a tuple (list with exactly 2 elements) containing
# the value of the varInt as first element and the length of the varInt as second
# element.
# @hex_string:           hexadecimal string of up to 9 bytes
# @return:		tuple containing value and length in bytes (in that order) of the next varInt structure in hex_string
def parse_next_var_int(hex_string):
    # Determine next varInt length
    hex_string_length = len(hex_string)
    if hex_string_length < 2:
        return None

    var_int_length = 2
    # Length cannot be longer than 18 and cannot not be longer than the string itself
    # take the next byte if the current byte starts with 1, e.g. like "10000000" (this is how sqlite3 variable integers are defined)
    while (((int(hex_string[(var_int_length - 2):var_int_length], 16) & 10000000) >> 7) == 1) and (var_int_length < 18) and (var_int_length < (hex_string_length - 1)): # -1 due to strings with odd length
        var_int_length += 2

    # Determine next varInt value
    bit_string = ""
    position = 1
    while position <= var_int_length:
        nibbleValue = int(hex_string[(position - 1):position], 16)
        if (position % 2) == 0 or position == 17:
            # This is the second nibble of a byte, so take all bits
            bit_string += _helpersBinaryOperations.get_bitstring(nibbleValue, 4)
        else:
            # This is not the first nibble of the ninth byte of the variable integer, so take only 3 bits
            bit_string += _helpersBinaryOperations.get_bitstring((nibbleValue & 7), 3)
        position += 1
        var_int_value = _helpersBinaryOperations.bin_to_int(bit_string)   

    # Return tuple of value and length
    return [var_int_value, (var_int_length / 2)]


#-----------------Example-------------------
if __name__ == "__main__":
    print "----> Testing parse_next_var_int(hexString)"
    print "parse_next_var_int(\"1\"):                      ", parse_next_var_int("1")
    print "parse_next_var_int(\"01\"):                     ", parse_next_var_int("01")
    print "parse_next_var_int(\"10\"):                     ", parse_next_var_int("10")
    print "parse_next_var_int(\"5a01\"):                   ", parse_next_var_int("5a01")
    print "parse_next_var_int(\"0717191901810f\"):         ", parse_next_var_int("0717191901810f")
    print "parse_next_var_int(\"810f\"):                   ", parse_next_var_int("810f")
    print "parse_next_var_int(\"9192a4c3f5b6e78899\"):     ", parse_next_var_int("9192a4c3f5b6e78899")
    print "parse_next_var_int(\"9192a4c3f5b6e78899ab2\"):  ", parse_next_var_int("9192a4c3f5b6e78899ab2")

    print "\n----> Testing parse_all_var_ints(hexString)"
    print "parse_all_var_ints(\"1\"):                      ", parse_all_var_ints("1")
    print "parse_all_var_ints(\"01\"):                     ", parse_all_var_ints("01")
    print "parse_all_var_ints(\"10\"):                     ", parse_all_var_ints("10")
    print "parse_all_var_ints(\"5a01\"):                   ", parse_all_var_ints("5a01")
    print "parse_all_var_ints(\"0717191901810f\"):         ", parse_all_var_ints("0717191901810f")
    print "parse_all_var_ints(\"810f\"):                   ", parse_all_var_ints("810f")
    print "parse_all_var_ints(\"9192a4c3f5b6e78899\"):     ", parse_all_var_ints("9192a4c3f5b6e78899")
    print "parse_all_var_ints(\"9192a4c3f5b6e78899ab2\"):  ", parse_all_var_ints("9192a4c3f5b6e78899ab2")
#-----------------Example-------------------