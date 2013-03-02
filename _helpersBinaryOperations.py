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

# Returns the positive or negative integer value of the given two's complement number
# @two:         	number as two's complement
# @length:		length of two in byte
# @return:		corresponding (positiv or negativ) value of two as integer
def twos_complement_to_int(two, lengthInByte):
    lengthInBit = 8 * lengthInByte
    # check the algebraic sign
    if ((two >> lengthInBit - 1) & 1) == 0:
        # positive integer
        return two
    else:
        # negative integer, calculate the two's complement
        return ((two - 1) ^ (pow(2, lengthInBit) - 1)) * (-1)

# Returns the binary string representation of an integer number with a
# certain length that can be specified (in bit).
# @integer:		integer number
# @length:		desired minimum length of the binary string in bit
#                       representation (filled with leading zeros)
# @return:		binary representation of integer
def get_bitstring(integer, length):
    bitString = bin(integer)
    resultString = ""

    if length < 1:
        return None

    bitStringLength = len(bitString)
    if bitStringLength > length:
        # bitString too long: chop some caracters off
        position = 1
        while position <= length:
            resultString = bitString[(bitStringLength - position):((bitStringLength - position) + 1)] + resultString
            position += 1
    else:
        # bitString eventuall too short
        resultString = bitString
        # eventually add some zeroes
        while (len(resultString) < length):
	    resultString = "0" + resultString

    return resultString


# Returns the binary string representation of the given integer
# @integer:		integer number that will be converted into a binary string
# @return:		representation of integer as binary string
def bin(integer):
    if (integer <= 1):
	return str(integer)
    else:
	return str(bin(integer >> 1)) + str(integer & 1)

# Returns the integer value of the given binary string
# @bitString:		binary string that will be converted to an integer number
# @return:		integer number represented by bitString
def bin_to_int(bitString):
    length = len(bitString)
    resultInt = 0
    digit = 1
    while digit <= length:
	resultInt += int(bitString[(digit - 1):digit]) * pow(2, length - digit)
	digit += 1
    return resultInt

# Returns the negation of the given binary string (e.g. "1001" returns "0110")
# @bitString:           bitString to negate
# @return:		negation of bitString as binary string
def negate(bitString):
    negatedBitString = ""
    for char in bitString:
        if char == "1":
            negatedBitString += "0"
        if char == "0":
            negatedBitString += "1"
    return negatedBitString


#-----------------Example-------------------
if __name__ == "__main__":
    print "----> Testing negate(bitString)"
    print "negate(\"0\"):                         ", negate("0")
    print "negate(\"1\"):                         ", negate("1")
    print "negate(\"01\"):                        ", negate("01")
    print "negate(\"10\"):                        ", negate("10")
    print "negate(\"00000000\"):                  ", negate("00000000")
    print "negate(\"11111111\"):                  ", negate("11111111")
    print "negate(\"11011011\"):                  ", negate("11011011")
    print "negate(\"101010011\"):                 ", negate("101010011")

    print "----> Testing bin_to_int(bitString)"
    print "bin_to_int(\"0\"):                       ", bin_to_int("0")
    print "bin_to_int(\"1\"):                       ", bin_to_int("1")
    print "bin_to_int(\"01\"):                      ", bin_to_int("01")
    print "bin_to_int(\"10\"):                      ", bin_to_int("10")
    print "bin_to_int(\"1000\"):                    ", bin_to_int("1000")
    print "bin_to_int(\"1111\"):                    ", bin_to_int("1111")
    print "bin_to_int(\"10000001\"):                ", bin_to_int("10000001")
    print "bin_to_int(\"111111111\"):               ", bin_to_int("111111111")

    print "----> Testing bin(integer)"
    print "bin(0):                              ", bin(0)
    print "bin(1):                              ", bin(1)
    print "bin(01):                             ", bin(01)
    print "bin(10):                             ", bin(10)
    print "bin(00000000):                       ", bin(00000000)
    print "bin(11111111):                       ", bin(11111111)
    print "bin(11011011):                       ", bin(11011011)
    print "bin(101010011):                      ", bin(101010011)

    print "----> Testing get_bitstring(integer, length)"
    print "get_bitstring(0, 4):                  ", get_bitstring(0, 4)
    print "get_bitstring(1, 4):                  ", get_bitstring(1, 4)
    print "get_bitstring(254, 8):                ", get_bitstring(254, 8)
    print "get_bitstring(256, 8):                ", get_bitstring(256, 8)
    print "get_bitstring(256, 16):               ", get_bitstring(256, 16)
    print "get_bitstring(9652342, 8):            ", get_bitstring(9652342, 8)
    print "get_bitstring(9652342, 16):           ", get_bitstring(9652342, 16)
    print "get_bitstring(9652342, 32):           ", get_bitstring(9652342, 32)

    print "----> Testing twos_complement_to_int(two, lengthInByte)"
    print "twos_complement_to_int(0, 1):           ", twos_complement_to_int(0, 1)
    print "twos_complement_to_int(1, 1):           ", twos_complement_to_int(1, 1)
    print "twos_complement_to_int(00000001, 4):    ", twos_complement_to_int(00000001, 1)
    print "twos_complement_to_int(254, 1):         ", twos_complement_to_int(254, 1)
    print "twos_complement_to_int(256, 1):         ", twos_complement_to_int(256, 1)
    print "twos_complement_to_int(1024, 1):        ", twos_complement_to_int(1024, 1)
    print "twos_complement_to_int(9652342, 1):     ", twos_complement_to_int(9652342, 1)
    print "twos_complement_to_int(9652342, 2):     ", twos_complement_to_int(9652342, 2)