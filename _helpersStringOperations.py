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

# TODO: implement other encodings, e.g. UTF-8 if necessary


# Translates a hexadecimal string (without any spaces) into an ascii string.
# Example: "53514c69746520666f726d61742033" ----> "SQLite format 3"
# @hexString:           hexadecimal string to translate
# @return:              ascii string interpretation of hexString
def hexstring_to_ascii(hexString):
        asciiString = ""
        for char in range(len(hexString) / 2):
                position = char * 2
                asciiString = asciiString + chr(int(hexString[(position):(position + 2)], 16))
        return asciiString


# Checks whether a string starts with a particular substring and ignores case sensitivity.
# @mainString:          string to search
# @subString:           substring to check for at the beginning of mainString
# @return:              returns 0 if mainString starts with subString, 1 otherwise.
def starts_with_string(mainString, subString):
    mainStringLength = len(mainString)
    subStringLength = len(subString)
    if (mainStringLength == 0) or (subStringLength == 0) or (mainStringLength < subStringLength):
        return 1

    # ingore case sensitivity
    mainString = mainString.lower()
    subString = subString.lower()

    # check whether mainString starts exactly with subString
    for i in range(subStringLength):
        if (mainString[i] != subString[i]):
            return 1

    # if function did not yet return 1, mainString starts with subString
    return 0


# Splits a hexadecimal string into to parts at each occurrence of a certain character,
# while paying attention to possible parentheses inside of the string. No cotent inside
# an opening and a closing parenthesis will be split.
# @hexString:           hexadecimal string to split
# @searchCharacter:     ascii character to search for
# @return:              list with the split elements of the original string
#                       or an empty list if searchCharacter was not found
def split_parenthesis_sensitive(hexString, searchCharacter):
    # check input
    crop_whitespace(hexString)
    # check if param list has a leading paranthesis
    if (fist_occurrence(hexString, "(") == 0):
        # cut paranthesis
        tmpString = cut_first_last_exclude(hexString, "(", ")")
        if len(tmpString) == (len(hexString) - 2):
            hexString = tmpString

    # intitialise result list
    splitList = []

    # parse complete hexString once
    parenthesesOpen = 0
    cutterPos = 0
    position = 0
    length = len(hexString)
    while (position < length):
        character = hexString[(position):(position + 1)]
        if character == "(":
            # opening parenthesis
            parenthesesOpen += 1
        if character == ")":
            # closing parenthesis
            parenthesesOpen -= 1
        #print "position: " + str(position) + ", parenthesesOpen: " + str(parenthesesOpen) + ", character: " + str(character) + ", cutterPos: " + str(cutterPos)
        if (character == searchCharacter) and (parenthesesOpen <= 0):
            # no parenthesis open: split string
            if position > cutterPos: # ensure that there is something to cut off in front
                result = hexString[cutterPos:position]
                crop_whitespace(result)
                # check if result has a leading parentheses
                if (fist_occurrence(result, "(") == 0):
                    # cut parentheses
                    tmpString = cut_first_last_exclude(result, "(", ")")
                    if len(tmpString) == (len(result) - 2):
                        result = tmpString
                splitList.append(result)
                #print "splitList: " + str(splitList)
            cutterPos = position + 1
        position += 1

    # append last element
    result = hexString[cutterPos:position]
    crop_whitespace(result)
    # check if result has a leading parentheses
    if (fist_occurrence(result, "(") == 0):
        # cut parentheses
        tmpString = cut_first_last_exclude(result, "(", ")")
        if len(tmpString) == (len(result) - 2):
            result = tmpString
    splitList.append(result)

    # return the splitted elements
    return splitList


# Splits a hexadecimal string into to parts at the first occurrence of a certain character.
# @hexString:           hexadecimal string to split
# @searchCharacter:     ascii character to search for
# @return:              tuple (list with exactly two elements) with the split string
#                       or an empty list if searchCharacter was not found
def split_at_first_occurrence(hexString, searchCharacter):
    occurrence = fist_occurrence(hexString, searchCharacter)
    # ensure we split the string correctly
    if occurrence > 0:
        return [hexString[0:occurrence], hexString[(occurrence + 1):]]
    else:
        return []


# Returns a string that is cut out of the given string between the first occurrence of
# a character and the next following occurrence of another character excluding both
# characters themselves.
# @hexString:           hexadecimal source string
# @firstCharacter:      ascii character to cut from (excluding this character)
# @secondCharacter:     ascii character to cut to (excluding this character)
# @return:              cut string between first occurrence of firstCharacter and
#                       next following occurrence of secondCharacter or empty string
#                       if one or both characters could not be found
def cut_first_next_exclude(hexString, firstCharacter, secondCharacter):
    cutStart = fist_occurrence(hexString, firstCharacter) + 1 # exclude character itself
    cutStop = next_occurrence(hexString, secondCharacter, cutStart)
    # ensure we cut the string correctly
    if (cutStart >= 0) and (cutStop > 0) and (cutStart < cutStop):
        return hexString[cutStart:cutStop]
    else:
        return ""


# Returns a string that is cut out of the given string between the first occurrence of
# a character and the next following occurrence of another character including both
# characters themselves.
# @hexString:           hexadecimal source string
# @firstCharacter:      ascii character to cut from (including this character)
# @secondCharacter:     ascii character to cut to (including this character)
# @return:              cut string between first occurrence of firstCharacter and
#                       next following occurrence of secondCharacter or empty string
#                       if one or both characters could not be found
def cut_first_next_include(hexString, firstCharacter, secondCharacter):
    cutStart = fist_occurrence(hexString, firstCharacter)
    cutStop = next_occurrence(hexString, secondCharacter, cutStart) + 1 # include character itself
    # ensure we cut the string correctly
    if (cutStart >= 0) and (cutStop > 0) and (cutStart < cutStop):
        return hexString[cutStart:cutStop]
    else:
        return ""


# Returns a tuple, the first element is the string cut out between the first occurrence of
# a character and the last occurrence of another character excluding both characters
# themselves, the second element is the rest of string. Returns an empty list if one or
# both characters could not be found.
# @hexString:           hexadecimal source string
# @firstCharacter:      ascii character to cut from (excluding this character)
# @secondCharacter:     ascii character to cut to (excluding this character)
# @return:              tuple with string between first occurrence of firstCharacter and
#                       last occurrence of secondCharacter as first element and the rest
#                       of the string as sencond element or empty string if one or both
#                       characters could not be found
def cut_first_last_exclude_into_tuple(hexString, firstCharacter, secondCharacter):
    cutStart = fist_occurrence(hexString, firstCharacter) + 1 # exclude character itself
    cutStop = last_occurrence(hexString, secondCharacter)
    # ensure we cut the string correctly
    if (cutStart >= 0) and (cutStop > 0) and (cutStart < cutStop):
        return [hexString[cutStart:cutStop], hexString[(cutStop + 1):]]
    else:
        return []


# Returns a tuple, the first element is the string cut out between the first occurrence of
# a character and the last occurrence of another character including both characters
# themselves, the second element is the rest of string. Returns an empty list if one or
# both characters could not be found.
# @hexString:           hexadecimal source string
# @firstCharacter:      ascii character to cut from (excluding this character)
# @secondCharacter:     ascii character to cut to (excluding this character)
# @return:              tuple with string between first occurrence of firstCharacter and
#                       last occurrence of secondCharacter as first element and the rest
#                       of the string as sencond element or empty string if one or both
#                       characters could not be found
def cut_first_last_include_into_tuple(hexString, firstCharacter, secondCharacter):
    cutStart = fist_occurrence(hexString, firstCharacter)
    cutStop = last_occurrence(hexString, secondCharacter) + 1 # include character itself
    # ensure we cut the string correctly
    if (cutStart >= 0) and (cutStop > 0) and (cutStart < cutStop):
        return [hexString[cutStart:cutStop], hexString[(cutStop):]]
    else:
        return []


# Returns a string that is cut out of the given string between the first occurrence of
# a character and the last occurrence of another character excluding both
# characters themselves.
# @hexString:           hexadecimal source string
# @firstCharacter:      ascii character to cut from (excluding this character)
# @secondCharacter:     ascii character to cut to (excluding this character)
# @return:              cut string between first occurrence of firstCharacter and
#                       last occurrence of secondCharacter or empty string if one or both
#                       characters could not be found
def cut_first_last_exclude(hexString, firstCharacter, secondCharacter):
    cutStart = fist_occurrence(hexString, firstCharacter) + 1 # exclude character itself
    cutStop = last_occurrence(hexString, secondCharacter)
    # ensure we cut the string correctly
    if (cutStart >= 0) and (cutStop > 0) and (cutStart < cutStop):
        return hexString[cutStart:cutStop]
    else:
        return ""


# Returns a string that is cut out of the given string between the first occurrence of
# a character and the last occurrence of another character including both
# characters themselves.
# @hexString:           hexadecimal source string
# @firstCharacter:      ascii character to cut from (including this character)
# @secondCharacter:     ascii character to cut to (including this character)
# @return:              cut string between first occurrence of firstCharacter and
#                       last occurrence of secondCharacter or empty string if one or both
#                       characters could not be found
def cut_first_last_include(hexString, firstCharacter, secondCharacter):
    cutStart = fist_occurrence(hexString, firstCharacter)
    cutStop = last_occurrence(hexString, secondCharacter) + 1 # include character itself
    # ensure we cut the string correctly
    if (cutStart >= 0) and (cutStop > 0) and (cutStart < cutStop):
        return hexString[cutStart:cutStop]
    else:
        return ""


# Returns the first occurrence of a character in a hexadecimal string.
# @hexString:           hexadecimal string to search
# @searchCharacter:     ascii character to search for
# @return:              offset of first occurrence of searchCharacter in hexString or
#                       -1 if searchCharacter was not found in hexString
def fist_occurrence(hexString, searchCharacter):
    for position in range(len(hexString)):
        if str(hexString[(position):(position + 1)]) == searchCharacter:
            return position
    return -1


# Returns the next occurrence of a character in a hexadecimal string
# starting to search at a given offset.
# @hexString:           hexadecimal string to search
# @searchCharacter:     ascii character to search for
# @searchFromOffset:    integer offset to start search from
# @return:              offset of next occurrence of searchCharacter in hexString
#                       after searchOffset or -1 if searchCharacter was not found
#                       in hexString
def next_occurrence(hexString, searchCharacter, searchOffset):
    # ensure correct searchOffset
    if (searchOffset < 0) or (searchOffset > (len(hexString) - 1)):
        return ""
    # determine next occurrence
    occurrence = fist_occurrence(hexString[searchOffset:], searchCharacter)
    # ensure that character was found
    if occurrence < 0:
        return -1
    else:
        return searchOffset + occurrence


# Returns the last occurrence of a character in a hexadecimal string.
# @hexString:           hexadecimal string to search
# @searchCharacter:     ascii character to search for
# @return:              offset of first occurrence of searchCharacter in hexString or
#                       -1 if searchCharacter was not found in hexString
def last_occurrence(hexString, searchCharacter):
    position = len(hexString) - 1
    while position >= 0:
        if str(hexString[(position):(position + 1)]) == searchCharacter:
            return position
        position -= 1
    return -1


# Crops all leading and tailing white space from a string.
# @string:              string to crop
# @return:              string without leading and tailing white space
def crop_whitespace(string):
    # ensure we got a string
    length = len(string)
    if length == 0:
        return ""

    # cut out any newlines
    index = 0
    previousSpace = 1
    while (index < len(string)):
#        print "loop " + str(index) + ", string          : " + str(string)
        # replace unprintable signs (like linefeeds, carriage return, tabs, space etc...) trough a simple space
        if (str(string[index]) <= "\x19"):
            string = string[:index] + " " + string[(index + 1):]
#            print "loop " + str(index) + ": sign replaced through space"

        # erase possible series of spaces
        if (str(string[index]) == "\x20"):
#            print "loop " + str(index) + ", sign is space"
#            print "loop " + str(index) + ", previousSpace   : " + str(previousSpace)
            if (previousSpace == 0):
                # set previous space, so we remember this space in case another space follows immediately
                previousSpace = 1
            else:
                # previous sign was a space already, cut the sign
                string = string[:index] + string[(index + 1):]
#                print "loop " + str(index) + ", cut sign, string : " + str(string)
                # continue without raising the index
                continue
        else:
            if (str(string[index]) == "("):
                # after an opening parenthesis, there is no need for a space, so remember this parenthesis
                previousSpace = 1
            else:
                # unset previous space
                previousSpace = 0
        index += 1

    # crop leading white space finally
    index = 0
    while (str(string[index]) == "\x20"):
        string = string[1:]

    # crop tailing white space finally
    index = len(string) - 1
    while (str(string[index]) == "\x20"):
        string = string[:index]
        index -= 1

    # return string without leading and trailing white space
    return string


#-----------------Example-------------------
if __name__ == "__main__":
    string = "CREATE TABLE name_lookup (data_id INTEGER REFERENCES data(_id) NOT NULL,raw_contact_id INTEGER REFERENCES raw_contacts(_id) NOT NULL,normalized_name TEXT NOT NULL,name_type INTEGER NOT NULL,PRIMARY KEY (data_id, normalized_name, name_type))"
    stringParantheses = "data_id INTEGER REFERENCES data(_id,test_foo, habalabi ,BAR , TESTSUPER_USER) NOT NULL,raw_contact_id INTEGER REFERENCES raw_contacts(_id) NOT NULL,normalized_name TEXT NOT NULL,name_type INTEGER NOT NULL,PRIMARY KEY (data_id, normalized_name, name_type)"

    print ""
    print "printing test string..."
    print string
    print ""
    print "crop white space: \"\"                : TEST" + str(crop_whitespace("")) + "TEST"
    print "crop white space: \"hello\"           : TEST" + str(crop_whitespace("hello")) + "TEST"
    print "crop white space: \"yabba     \"      : TEST" + str(crop_whitespace("yabba  	 \n   ")) + "TEST"
    print "crop white space: \"     yabba\"      : TEST" + str(crop_whitespace("     yabba")) + "TEST"
    print "crop white space: \" Good Bye \"      : TEST" + str(crop_whitespace(" Good Bye ")) + "TEST"
    print "crop white space: \"NLGood ByeNL\"    : TEST" + str(crop_whitespace("\nGood Bye\n")) + "TEST"
    print "crop white space: \" NLGood ByeNL \"  : TEST" + str(crop_whitespace(" \nGood Bye\n ")) + "TEST"
    print "crop white space: \" NL Good Bye NL \": TEST" + str(crop_whitespace(" \n Good Bye \n ")) + "TEST"
    print "crop white space: \" NL Good  NL Bye NL \": TEST" + str(crop_whitespace(" \n 	Good  \n Bye \n ")) + "TEST"
    print ""
    print "first occurrence of '(': " + str(fist_occurrence(string, "("))
    print "first occurrence of 'p': " + str(fist_occurrence(string, "p"))
    print ""
    print "next occurrence of 'e'  -1: " + str(next_occurrence(string, "e", -1))
    print "next occurrence of 'e'   0: " + str(next_occurrence(string, "e", 0))
    print "next occurrence of 'e'  13: " + str(next_occurrence(string, "e", 13))
    print "next occurrence of 'e'  14: " + str(next_occurrence(string, "e", 14))
    print "next occurrence of 'e'  15: " + str(next_occurrence(string, "e", 15))
    print "next occurrence of 'e' 100: " + str(next_occurrence(string, "e", 100))
    print "next occurrence of 'e' 200: " + str(next_occurrence(string, "e", 200))
    print "next occurrence of 'e' 300: " + str(next_occurrence(string, "e", 300))
    print "next occurrence of 'e' 400: " + str(next_occurrence(string, "e", 400))
    print ""
    print "last occurrence of '(': " + str(last_occurrence(string, "("))
    print "last occurrence of ')': " + str(last_occurrence(string, ")"))
    print "last occurrence of 'p': " + str(last_occurrence(string, "p"))
    print ""
    print "cut first last include '(' ')': " + str(cut_first_last_include(string, "(", ")"))
    print ""
    print "cut first last exclude '(' ')': " + str(cut_first_last_exclude(string, "(", ")"))
    print ""
    print "cut first next include '(' ')': " + str(cut_first_next_include(string, "(", ")"))
    print ""
    print "cut first next exclude '(' ')': " + str(cut_first_next_exclude(string, "(", ")"))
    print ""
    print "split at first occurrence '(': " + str(split_at_first_occurrence(string, "("))
    print ""
    print "split parenthesis sensitive ',': " + str(split_parenthesis_sensitive(stringParantheses, ","))
    print ""
    print "starts with string (\"homer\", \"home\"):                      " + str(starts_with_string("homer", "home"))
    print "starts with string (\"this is my home\", \"home\"):            " + str(starts_with_string("this is my home", "home"))
    print "starts with string (\"this is my home\", \"his\"):             " + str(starts_with_string("this is my home", "his"))
    print "starts with string (\"this is my home\", \"this is my \"):     " + str(starts_with_string("this is my home", "this is my "))
    print "starts with string (\"This is my home\", \"this is my \"):     " + str(starts_with_string("This is my home", "this is my "))
    print "starts with string (\"thIs iS My home\", \"thIs iS My \"):     " + str(starts_with_string("thIs iS My home", "thIs iS My "))


#-----------------Example-------------------