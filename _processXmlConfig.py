#!/usr/bin/python2.7 
# Copyright (C) 2012 Michael Spreitzenbarth, Sven Schmitt, Tobias Latzo
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

import sys, subprocess
from xml.dom import minidom
import _adel_log

# Represents the xml config 
class PhoneConfig(object):
    def __init__(self, xml_file, device, os_version):
        self.device = device
        self.os_version = os_version
        self.model = subprocess.Popen(['adb', 'shell', 'getprop', 'ro.product.model'], stdout=subprocess.PIPE).communicate(0)[0].rstrip("\r\n ")
        if self.model == "":
            self.model = "local"
        try:
            self.xml_doc = minidom.parse(xml_file)
        except:
            print "Could not parse xml config file."
            sys.exit(1)
        self.select_smartphone()
        self.process()

    # Searches smartphone in XML file. If no config available, user can choose which configuration to use
    def select_smartphone(self):
        phones = self.xml_doc.getElementsByTagName("phone")
        # Search specific config for smartphone
        for phone in phones:
            if (phone.getAttribute("device") == self.device) and (phone.getAttribute("model") == self.model) and (phone.getAttribute("os_version") == self.os_version):
                self.phone = phone
                _adel_log.log("PhoneConfig:   ----> Found right config in the database.", 3)
                return
        # Otherwise take the first match or die
        for phone in phones:
            if (phone.getAttribute("device") == self.device):
                self.phone = phone
                _adel_log.log("PhoneConfig:   ----> The ADEL configuration for this phone \"" + self.device + " " + phone.getAttribute("model") + " Android " + phone.getAttribute("os_version") +  "\" is different from the real phone \"" + self.device + " " + self.model + " Android " + self.os_version +  "\"! Please check output carefully!", 2)
                return
        _adel_log.log("PhoneConfig:   ----> No suitable config found for " + str(self.device), 2)
        sys.exit(1)

    # Extracts all data from the XML file
    def process(self):
        # Standard databases
        databases = self.phone.getElementsByTagName("databases")[0] 
        self.process_calls(databases.getElementsByTagName("call_logs")[0])
        self.process_sms(databases.getElementsByTagName("sms")[0])
        self.process_calendar(databases.getElementsByTagName("calendar")[0])
        self.process_contacts(databases.getElementsByTagName("contacts")[0])
        self.process_smartphone_info(self.phone.getElementsByTagName("smartphone_information")[0])
        # Apps databases
        apps = self.xml_doc.getElementsByTagName("apps")[0] 
        self.process_facebook(apps.getElementsByTagName("facebook")[0])
        self.process_twitter(apps.getElementsByTagName("twitter")[0])
    
    # Concatenates all integers in a subtree, where the children are all leaves
    def tree_to_list(self, entries):
        res_list = []
        for entry in entries.childNodes:
            if entry.nodeType == entry.ELEMENT_NODE:
                res_list.append(int(entry.firstChild.data))
        return res_list

    # Extracts call information from XML file
    def process_calls(self, calls):
        # DB_NAME
        call_db_name = calls.getElementsByTagName("db_name")[0]
        if call_db_name == []:
            if self.os_version < 200:
                self.db_file_call_logs = "contacts.db"
            else:
                self.db_file_call_logs = "contacts2.db"
        else:
            self.db_file_call_logs = call_db_name.firstChild.data
        # TABLE_NUM
        call_table_num = calls.getElementsByTagName("table_num")[0]
        self.call_log_table_num = int(call_table_num.firstChild.data)
        # POSITIONS
        self.call_log_entry_positions = self.tree_to_list(calls.getElementsByTagName("call_log_entry_positions")[0])

    # Extracts sms information from XML file
    def process_sms(self, sms):
        # DB_NAME
        sms_db_name = sms.getElementsByTagName("db_name")[0]
        if sms_db_name == []:
            self.db_file_sms = "mmssms.db"
        else:
            self.db_file_sms = sms_db_name.firstChild.data
        # TABLE_NUM
        sms_table_num = sms.getElementsByTagName("table_num")[0]
        if sms_table_num == []:
            if (os_version < 233):
                self.sms_table_num = 6
            else:
                self.sms_table_num = 7
        else:
            self.sms_table_num = int(sms_table_num.firstChild.data)
        # POSITIONS
        self.sms_entry_positions = self.tree_to_list(sms.getElementsByTagName("sms_entry_positions")[0])

    # Extracts calendar information from XML file
    def process_calendar(self, calendar):
        # DB_NAME
        calendar_db_name = calendar.getElementsByTagName("db_name")[0]
        if calendar_db_name == []:
            self.db_file_calendar = "calendar.db"
        else:
            self.db_file_calendar = calendar_db_name.firstChild.data
        # Name Table
        name_table = calendar.getElementsByTagName("name_table")[0]
        ## TABLE_NUM
        self.calendar_name_table_num = int(name_table.getElementsByTagName("table_num")[0].firstChild.data)
        ## POSITIONS
        self.calendar_name_list = self.tree_to_list(name_table.getElementsByTagName("calendar_name_positions")[0])
        # Event Table
        event_table = calendar.getElementsByTagName("events")[0]
        ## TABLE_NUM
        self.calendar_events_table_num = int(event_table.getElementsByTagName("table_num")[0].firstChild.data)
        ## POSITIONS
        self.calendar_events_list = self.tree_to_list(event_table.getElementsByTagName("calendar_event_positions")[0])

    # Extract contacts information from XML file
    def process_contacts(self, contacts):
        # DB_NAME
        contacts_db_name = contacts.getElementsByTagName("db_name")[0]
        if contacts_db_name == []:
            if self.os_version < 200:
                self.db_file_contacts = "contacts.db"
            else:
                self.db_file_contacts = "contacts2.db"
        else:
            self.db_file_contacts = contacts_db_name.firstChild.data
        # Normal Contacts
        normal_contacts = contacts.getElementsByTagName("normal_contacts")[0]
        ## TABLE_NUM
        self.contacts_normal_table_num = int(normal_contacts.getElementsByTagName("table_num")[0].firstChild.data)
        ## POSITIONS
        self.contacts_normal_list = self.tree_to_list(normal_contacts.getElementsByTagName("contacts_positions")[0])
        # Raw Contacts
        raw_contacts = contacts.getElementsByTagName("raw_contacts")[0]
        ## TABLE_NUM
        self.raw_contacts_table_num = int(raw_contacts.getElementsByTagName("table_num")[0].firstChild.data)
        ## RAW CONTACT LIST
        self.raw_contacts_list = self.tree_to_list(raw_contacts.getElementsByTagName("raw_contacts_options")[0])
        ## RAW CONTACT DELETED LIST
        self.raw_contacts_deleted_list = self.tree_to_list(raw_contacts.getElementsByTagName("raw_contacts_deleted_positions")[0])
        # Data
        data = contacts.getElementsByTagName("data")[0]
        ## TABLE_NUM
        self.data_table_num = int(data.getElementsByTagName("table_num")[0].firstChild.data)
        ## DATA LIST
        self.data_entry_list = self.tree_to_list(data.getElementsByTagName("data_entry_positions")[0])
        # Mimetypes
        mimetypes = contacts.getElementsByTagName("mimetypes")[0]
        ## TABLE_NUM
        self.mime_table_num = int(mimetypes.getElementsByTagName("table_num")[0].firstChild.data)
        ## MIMETYPE LIST
        self.mime_type_entry_list = self.tree_to_list(mimetypes.getElementsByTagName("mimetype_positions")[0])

    # Extract facebook information from XML file
    def process_facebook(self, facebook):
        self.fb_db_filename = facebook.getElementsByTagName("db_name")[0].firstChild.data
        # User's values
        users_values = facebook.getElementsByTagName("users_values")[0]
        ## TABLE_NUM
        self.fb_users_values_table_num = int(users_values.getElementsByTagName("table_num")[0].firstChild.data)
        ## FB_USERS_VALUES
        self.fb_users_values_list = self.tree_to_list(users_values.getElementsByTagName("users_values_positions")[0])
        # Connections
        cons = facebook.getElementsByTagName("connections")[0]
        ## TABLE_NUM
        self.fb_connections_table_num = int(cons.getElementsByTagName("table_num")[0].firstChild.data)
        ## FB_CONNECTION_LIST
        self.fb_connection_list = self.tree_to_list(cons.getElementsByTagName("connection_positions")[0])
        # Friend's data
        friends_data = facebook.getElementsByTagName("friends_data")[0]
        ## TABLE_NUM
        self.fb_friends_data_table_num = int(friends_data.getElementsByTagName("table_num")[0].firstChild.data)
        ## FB_CONNECTION_LIST
        self.fb_friends_data_list = self.tree_to_list(friends_data.getElementsByTagName("friends_data_positions")[0])

    # Extract twitter information from XML file
    def process_twitter(self, twitter):
        # DB filename is in _analyzeDBs
        # Twitter user
        user = twitter.getElementsByTagName("twitter_user")[0]
        ## TABLE_NUM
        self.twitter_user_table_num = int(user.getElementsByTagName("table_num")[0].firstChild.data)
        ## TWITTER USER LIST
        self.twitter_user_list = self.tree_to_list(user.getElementsByTagName("twitter_user_positions")[0])
        # Statuses
        statuses = twitter.getElementsByTagName("statuses")[0]
        ## TABLE_NUM
        self.statuses_table_num = int(statuses.getElementsByTagName("table_num")[0].firstChild.data)
        ## TWITTER STATUSES
        self.twitter_statuses_list = self.tree_to_list(statuses.getElementsByTagName("status_positions")[0])

    # Extract smartphone information from XML file
    def process_smartphone_info(self, info):
        # Info 1 
        info1 = info.getElementsByTagName("info1")[0]
        db_filename = info1.getElementsByTagName("db_name")
        if db_filename == "":
            if os_version < 200:
                self.file_info1_db_name = "contacts.db"
                self.file_info1_table_num = 19
            else:
                if os_version > 220:
                    self.file_info1_db_name = "accounts.db"
                    self.file_info1_table_num = 1
                else:
                    self.file_info1_db_name = "contacts2.db"
                    self.file_info1_table_num = 19
        else:
            self.file_info1_db_name = db_filename[0].firstChild.data
            self.file_info1_table_num = int(info1.getElementsByTagName("table_num")[0].firstChild.data)
        accounts = info1.getElementsByTagName("accounts")[0]
        self.account_entry_list = self.tree_to_list(accounts.getElementsByTagName("accounts_positions")[0])
        # Info 2
        info2 = info.getElementsByTagName("info2")[0]
        db_filename = info2.getElementsByTagName("db_name")
        self.file_info2_table_num = int(info2.getElementsByTagName("table_num")[0].firstChild.data)
        if db_filename == "":
                    self.file_info2_db_name = "accounts.db"
        else:
            self.file_info2_db_name = db_filename[0].firstChild.data
        meta = info2.getElementsByTagName("meta")[0]
        self.meta_entry_list = self.tree_to_list(meta.getElementsByTagName("meta_positions")[0])
        # Info 3
        info3 = info.getElementsByTagName("info3")[0]
        db_filename = info3.getElementsByTagName("db_name")
        self.file_info3_table_num = int(info3.getElementsByTagName("table_num")[0].firstChild.data)
        if db_filename == "":
                    self.file_info3_db_name = "settings.db"
        else:
            self.file_info3_db_name = db_filename[0].firstChild.data
        settings = info3.getElementsByTagName("settings")[0]
        self.settings_entry_list = self.tree_to_list(settings.getElementsByTagName("settings_positions")[0])
