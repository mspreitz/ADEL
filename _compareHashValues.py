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

import hashlib

import _adel_log


def compare(backup_dir):
    _adel_log.log("\n############  HASH COMPARISION  ############\n", 2)
    _adel_log.log("compareHash:   ----> starting to compare calculated hash values", 0)
    hash_value_file = open(backup_dir + "/databases/hash_values.log", "a+")
    for line in hash_value_file:
        database = line.split(" ")[0]
        hash_value_old = line.split(" ")[2]
        hash_value_new = hashlib.sha256(backup_dir + "/databases/" + database).hexdigest()
        if hash_value_old != hash_value_new:
            _adel_log.log("hash_comparision -> hash vlaue missmatch on database: " + database, 2)
        else:
            _adel_log.log("hash_comparision -> hash value match on database: " + database, 3)
    hash_value_file.close()