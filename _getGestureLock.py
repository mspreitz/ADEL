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
import sqlite3
import array
import datetime
from binascii import hexlify

import _adel_log

SQLITE_DB = "GestureRainbowTable.db"


def crack(backup_dir):
    try:
        f = open(backup_dir + "/databases/gesture.key", "rb")
        for line in f:
            lookup_hash = hexlify(line).decode()
            _adel_log.log("Screenlock:    ----> Screenlock Hash: \033[0;32m" + lookup_hash + "\033[m", 0)
            conn = sqlite3.connect(SQLITE_DB)
            cur = conn.cursor()
            cur.execute("SELECT pattern FROM RainbowTable WHERE hash = ?", (lookup_hash,))
            result = cur.fetchone()
            if result:
                gesture = result[0]
                _adel_log.log("Screenlock:    ----> Screenlock Gesture: \033[0;32m" + gesture + "\033[m", 0)
    except:
        _adel_log.log("Screenlock:    ----> Can't find gesture in RainbowTable !!!", 2)