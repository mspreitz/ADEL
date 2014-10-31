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

import os, subprocess, hashlib
import _adel_log

# Get database files through the android SDK
def get_SQLite_files(backup_dir, os_version, device_name):
    hash_value_file = backup_dir + "/hash_values.log"
    hash_value = open(hash_value_file, "a+")
    _adel_log.log("\n############  DUMP SQLite FILES  ############\n", 2)
    # Standard applications

    # Accounts database (IMSI, Account_Name, Account_Type, sha1_hash)
    try:
        accountdb = subprocess.Popen(['adb', 'pull', '/data/system/accounts.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        accountdb.wait()
        _adel_log.log("accounts.db -> " + accountdb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/accounts.db").hexdigest(), 3)
        hash_value.write("accounts.db -> " + hashlib.sha256(backup_dir + "/accounts.db").hexdigest() + " \n")
    except:
        _adel_log.log("dumpDBs:       ----> accounts database doesn't exist!", 2)
    
    # Contacts database ()
    if os_version < 2.0:
        contactsdb_name = "contacts.db"
    else:
        contactsdb_name = "contacts2.db"
    try:
        contactsdb = subprocess.Popen(['adb', 'pull', '/data/data/com.android.providers.contacts/databases/' + contactsdb_name, backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        contactsdb.wait()
        _adel_log.log(contactsdb_name + " -> " + contactsdb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/contacts2.db").hexdigest(), 3)
        hash_value.write(contactsdb_name + " -> " + hashlib.sha256(backup_dir + "/" + contactsdb_name).hexdigest() + " \n")
    except:
        _adel_log.log("dumpDBs:       ----> contacts database doesn't exist!", 2)
    
    # MMS and SMS database ()
    try:
        smsdb = subprocess.Popen(['adb', 'pull', '/data/data/com.android.providers.telephony/databases/mmssms.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        smsdb.wait()
        _adel_log.log("mmssms.db -> " + smsdb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/mmssms.db").hexdigest(), 3)
        hash_value.write("mmssms.db -> " + hashlib.sha256(backup_dir + "/mmssms.db").hexdigest() + " \n")
    except:
        _adel_log.log("dumpDBs:       ----> mms/sms database doesn't exist!", 2)
    
    # Calendar database ()
    try:
        calendardb = subprocess.Popen(['adb', 'pull', '/data/data/com.android.providers.calendar/databases/calendar.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        calendardb.wait()
        _adel_log.log("calendar.db -> " + calendardb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/calendar.db").hexdigest(), 3)
        hash_value.write("calendar.db -> " + hashlib.sha256(backup_dir + "/calendar.db").hexdigest() + " \n")
    except:
        _adel_log.log("dumpDBs:       ----> calendar database doesn't exist!", 2)
    
    # Settings database ()
    try:
        settingsdb = subprocess.Popen(['adb', 'pull', '/data/data/com.android.providers.settings/databases/settings.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        settingsdb.wait()
        _adel_log.log("settings.db -> " + settingsdb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/settings.db").hexdigest(), 3)
        hash_value.write("settings.db -> " + hashlib.sha256(backup_dir + "/settings.db").hexdigest() + " \n")
    except:
        _adel_log.log("dumpDBs:       ----> settings database doesn't exist!", 2)
    
    # Location caches (cell & wifi)
    if os_version < 2.3:
        try:
            cachecell = subprocess.Popen(['adb', 'pull', '/data/data/com.google.android.location/files/cache.cell', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            cachecell.wait()
            _adel_log.log("chache.cell-> " + cachecell.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/chache.cell").hexdigest(), 3)
            hash_value.write("chache.cell -> " + hashlib.sha256(backup_dir + "/chache.cell").hexdigest() + " \n")
        except:
            _adel_log.log("dumpDBs:       ----> cell GPS cache doesn't exist!", 2)
        try:
            cachewifi = subprocess.Popen(['adb', 'pull', '/data/data/com.google.android.location/files/cache.wifi', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            cachewifi.wait()
            _adel_log.log("chache.wifi-> " + cachewifi.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/chache.wifi").hexdigest(), 3)
            hash_value.write("chache.wifi -> " + hashlib.sha256(backup_dir + "/chache.wifi").hexdigest() + " \n")
        except:
            _adel_log.log("dumpDBs:       ----> wifi GPS cache doesn't exist!", 2)

    # Optional applications and databases ----> analyzing is not implemented right now
    # Downloaded data and apps database ()
    try:
        downloadsdb = subprocess.Popen(['adb', 'pull', '/data/data/com.android.providers.downloads/databases/downloads.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        downloadsdb.wait()
        _adel_log.log("downloads.db -> " + downloadsdb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/downloads.db").hexdigest(), 3)
    except:
        _adel_log.log("dumpDBs:       ----> downloads database doesn't exist!", 2)
    
    # User dictionary database ()
    try:
        userdb = subprocess.Popen(['adb', 'pull', '/data/data/com.android.providers.userdictionary/databases/user_dict.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        userdb.wait()
        _adel_log.log("user_dict.db -> " + userdb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/user_dict.db").hexdigest(), 3)
    except:
        _adel_log.log("dumpDBs:       ----> user dict doesn't exist!", 2)    
    # Phone database ()
    try:
        phonedb = subprocess.Popen(['adb', 'pull', '/data/data/com.android.providers.telephony/databases/telephony.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        phonedb.wait()
        _adel_log.log("telephony.db -> " + phonedb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/telephony.db").hexdigest(), 3)
    except:
        _adel_log.log("dumpDBs:       ----> telephony database doesn't exist!", 2)

    # Automated dictionary database ()
    try:
        autodb = subprocess.Popen(['adb', 'pull', '/data/data/com.android.inputmethod.latin/databases/auto_dict.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        autodb.wait()
        _adel_log.log("auto_dict.db -> " + autodb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/auto_dict.db").hexdigest(), 3)
    except:
        _adel_log.log("dumpDBs:       ----> auto dict doesn't exist!", 2)

    # Weather data database ()
    try:
        weatherdb = subprocess.Popen(['adb', 'pull', '/data/data/com.google.android.apps.genie.geniewidget/databases/weather.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        weatherdb.wait()
        _adel_log.log("weather.db -> " + weatherdb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/weather.db").hexdigest(), 3)
    except:
        _adel_log.log("dumpDBs:       ----> weather database doesn't exist!", 2)
    try:
        weatherdb = subprocess.Popen(['adb', 'pull', '/data/data/com.sec.android.widgetapp.weatherclock/databases/WeatherClock', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        weatherdb.wait()
        _adel_log.log("WeatherClock.db -> " + weatherdb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/WeatherClock.db").hexdigest(), 3)
    except:
        _adel_log.log("dumpDBs:       ----> weather widget doesn't exist!", 2)

    # Google-Mail programm database ()
    try:
        gmaildb = subprocess.Popen(['adb', 'pull', '/data/data/com.google.android.gm/databases/gmail.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        gmaildb.wait()
        _adel_log.log("gmail.db -> " + gmaildb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/gmail.db").hexdigest(), 3)
    except:
        _adel_log.log("dumpDBs:       ----> gmail database doesn't exist!", 2)

    # Other Email Accounts than Gmail ()
    try:
        providerdb = subprocess.Popen(['adb', 'pull', '/data/data/com.android.email/databases/EmailProvider.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        providerdb.wait()
        _adel_log.log("EmailProvider.db -> " + providerdb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/EmailProvider.db").hexdigest(), 3)
    except:
        _adel_log.log("dumpDBs:       ----> EmailProvider database doesn't exist!", 2)

    # Clock and alarms database ()
    try:
        alarmdb = subprocess.Popen(['adb', 'pull', '/data/data/com.android.deskclock/databases/alarms.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        alarmdb.wait()
        _adel_log.log("alarms.db -> " + alarmdb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/alarms.db").hexdigest(), 3)
    except:
        _adel_log.log("dumpDBs:       ----> alarms database doesn't exist!", 2)

    # Twitter database ()
    try:
        for i in range(6):
            try:
                file_name = subprocess.Popen(['adb', 'shell', 'ls', '/data/data/com.twitter.android/databases/'], stdout=subprocess.PIPE).communicate(0)[0].split()[i]
                if ".db" in file_name:
                    twitter_db = '/data/data/com.twitter.android/databases/' + file_name
                    twitter_db_name = subprocess.Popen(['adb', 'pull', twitter_db, backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    twitter_db_name.wait()
                    _adel_log.log(file_name + " -> " + twitter_db_name.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + file_name).hexdigest(), 3)
                else:
                    continue
            except:
                continue
    except:
        _adel_log.log("dumpDBs:       ----> twitter database doesn't exist!", 2)

    # Google-Talk database ()
    try:
        gtalkdb = subprocess.Popen(['adb', 'pull', '/data/data/com.google.android.gsf/databases/talk.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        gtalkdb.wait()
        _adel_log.log("talk.db -> " + gtalkdb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/talk.db").hexdigest(), 3)
    except:
        _adel_log.log("dumpDBs:       ----> Google-Talk database doesn't exist!", 2)

    # Search and download the Google-Mail mail database ()
    try:
        for i in range(6):
            file_name = subprocess.Popen(['adb', 'shell', 'ls', '/data/data/com.google.android.gm/databases/'], stdout=subprocess.PIPE).communicate(0)[0].split()[i]
            if file_name.startswith('mailstore'):
                mail_db = '/data/data/com.google.android.gm/databases/' + file_name
                emaildb = subprocess.Popen(['adb', 'pull', mail_db, backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                emaildb.wait()
                _adel_log.log(file_name + " -> " + emaildb.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + file_name).hexdigest(), 3)
                break
            else:
                continue
    except:
        _adel_log.log("dumpDBs:       ----> Google-Mail database doesn't exist!", 2)

    # Google+ database
    try:
        for i in range(6):
            try:
                file_name = subprocess.Popen(['adb', 'shell', 'ls', '/data/data/com.google.android.apps.plus/databases/'], stdout=subprocess.PIPE).communicate(0)[0].split()[i]
                if ".db" in file_name:
                    plus_db = '/data/data/com.google.android.apps.plus/databases/' + file_name
                    plus_db_name = subprocess.Popen(['adb', 'pull', plus_db, backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    plus_db_name.wait()
                    _adel_log.log(file_name + " -> " + plus_db_name.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + file_name).hexdigest(), 3)
                else:
                    continue
            except:
                continue
    except:
        _adel_log.log("dumpDBs:       ----> Google+ database doesn't exist!", 2)

    # Google-Maps database
    try:
        try:
            maps_file_name = subprocess.Popen(['adb', 'pull', '/data/data/com.google.android.apps.maps/databases/da_destination_history', backup_dir + "/da_destination_history.db"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            maps_file_name.wait()
            _adel_log.log("da_destination_history -> " + maps_file_name.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "da_destination_history.db").hexdigest(), 3)
        except:
            _adel_log.log("dumpDBs:       ----> Google-Maps navigation history doesn't exist!", 2)
        for i in range(6):
            try:
                file_name = subprocess.Popen(['adb', 'shell', 'ls', '/data/data/com.google.android.apps.maps/databases/'], stdout=subprocess.PIPE).communicate(0)[0].split()[i]
                if ".db" in file_name:
                    maps_db = '/data/data/com.google.android.apps.maps/databases/' + file_name
                    maps_db_name = subprocess.Popen(['adb', 'pull', maps_db, backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    maps_db_name.wait()
                    _adel_log.log(file_name + " -> " + maps_db_name.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + file_name).hexdigest(), 3)
                else:
                    continue
            except:
                continue
    except:
        _adel_log.log("dumpDBs:       ----> Google-Maps database doesn't exist!", 2)

    # Facebook database
    try:
        facebook = subprocess.Popen(['adb', 'pull', '/data/data/com.facebook.katana/databases/fb.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        facebook.wait()
        _adel_log.log("fb.db -> " + facebook.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/fb.db").hexdigest(), 3)
    except:
        _adel_log.log("dumpDBs:       ----> Facebook database doesn't exist!", 2)

    # Browser GPS database
    try:
        browserGPS = subprocess.Popen(['adb', 'pull', '/data/data/com.android.browser/app_geolocation/CachedGeoposition.db', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        browserGPS.wait()
        _adel_log.log("CachedGeoposition.db -> " + browserGPS.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/CachedGeoposition.db").hexdigest(), 3)
    except:
        _adel_log.log("dumpDBs:       ----> Cached geopositions within browser don't exist!", 2)

    # Gesture Lock File
    try:
        gesture = subprocess.Popen(['adb', 'pull', '/data/system/gesture.key', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        gesture.wait()
        _adel_log.log("gesture.key -> " + gesture.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/gesture.key").hexdigest(), 3)
    except:
        _adel_log.log("dumpDBs:       ----> No gesture lock found!", 2)

    # Password Lock File
    try:
        password = subprocess.Popen(['adb', 'pull', '/data/system/password.key', backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        password.wait()
        _adel_log.log("password.key -> " + password.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + "/password.key").hexdigest(), 3)
    except:
        _adel_log.log("dumpDBs:       ----> No password lock found!", 2)

    # Stored files (pictures, documents, etc.)
    if device_name != "local":
        # Pictures
        picture_dir = backup_dir.split("/")[0] + "/pictures/"
        os.mkdir(picture_dir)
        try:
            _adel_log.log("dumpDBs:       ----> dumping pictures (internal_sdcard)....", 0)
            pictures = subprocess.Popen(['adb', 'pull', '/sdcard/DCIM/Camera/', picture_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            pictures.wait()
        except:
            _adel_log.log("dumpDBs:       ----> No pictures on the internal SD-card found!", 2)
        try:
            pictures = subprocess.Popen(['adb', 'pull', '/data/media/0/DCIM/Camera/', picture_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            pictures.wait()
        except:
            _adel_log.log("dumpDBs:       ----> No pictures on the internal SD-card (alternate path) found!", 2)
        try:
            _adel_log.log("dumpDBs:       ----> dumping pictures (external_sdcard)....", 0)
            pictures = subprocess.Popen(['adb', 'pull', '/sdcard/external_sd/DCIM/Camera/', picture_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            pictures.wait()
        except:
            _adel_log.log("dumpDBs:       ----> No pictures on the external SD-card found!", 2)
        try:
            _adel_log.log("dumpDBs:       ----> dumping screen captures (internal_sdcard)....", 0)
            pictures = subprocess.Popen(['adb', 'pull', '/sdcard/ScreenCapture/', picture_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            pictures.wait()
        except:
            _adel_log.log("dumpDBs:       ----> No screen captures on the internal SD-card found!", 2)
        try:
            _adel_log.log("dumpDBs:       ----> dumping screen captures (internal_sdcard)....", 0)
            pictures = subprocess.Popen(['adb', 'pull', '/data/media/0/ScreenCapture/', picture_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            pictures.wait()
        except:
            _adel_log.log("dumpDBs:       ----> No screen captures on the internal SD-card (alternate path) found!", 2)
    hash_value.close()    


def get_twitter_sqlite_files(backup_dir, os_version):
    _adel_log.log("\n############  DUMP TWITTER SQLite FILES  ############\n", 2)
    twitterdbnamelist = []
    try:
        for i in range(6):
            try:
                file_name = subprocess.Popen(['adb', 'shell', 'ls', '/data/data/com.twitter.android/databases/'], stdout=subprocess.PIPE).communicate(0)[0].split()[i]
                if ".db" in file_name:
                    twitterdbnamelist.append(file_name)
                    twitter_db = '/data/data/com.twitter.android/databases/' + file_name
                    twitter_db_name = subprocess.Popen(['adb', 'pull', twitter_db, backup_dir], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    twitter_db_name.wait()
                    _adel_log.log(file_name + " -> " + twitter_db_name.communicate(0)[1].split("(")[1].split(")")[0] + " -> " + hashlib.sha256(backup_dir + file_name).hexdigest(), 3)
                else:
                    continue
            except:
                continue
    except:
        _adel_log.log("dumpDBs:       ----> Twitter database doesn't exist!", 2)
    return twitterdbnamelist