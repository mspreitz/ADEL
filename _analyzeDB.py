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
import os, string, time, subprocess, sys
import _xmlParser, _adel_log, _sqliteParser
from _processXmlConfig import PhoneConfig

def string_replace(input):
    output = input.decode("utf-8")
    return output

def string_replace_2(input):
    output = input.encode("utf-8")
    return output

def analyze_call_logs(backup_dir, os_version, xml_dir, config):
    ######################################################################################################################################################
    #                                                           definition of Tuples                                                                     #
    ######################################################################################################################################################
    # CALL LOGS
    ## Database Name
    db_file_call_logs = backup_dir + "/" +  config.db_file_call_logs
    ######################################################################################################################################################
    ## Table Name
    #### calls
    ## corresponding table number in the database
    CALL_LOG_TABLE_NUMBER = config.call_log_table_num
    ## Table Design
    #### [[['_id', 'INTEGER'], ['number', 'TEXT'], ['presentation', 'INTEGER'], ['date', 'INTEGER'], ['duration', 'INTEGER'], ['type', 'INTEGER'], 
    #      ['new', 'INTEGER'], ['name', 'TEXT'], ['numbertype', 'INTEGER'], ['numberlabel', 'TEXT'], ['countryiso', 'TEXT'], ['voicemail_uri', 'TEXT'], 
    #      ['is_read', 'INTEGER'], ['geocoded_location', 'TEXT'], ['lookup_uri', 'TEXT'], ['matched_number', 'TEXT'], ['normalized_number', 'TEXT'], 
    #      ['photo_id', 'INTEGER'], ['formatted_number', 'TEXT'], ['_data', 'TEXT'], ['has_content', 'INTEGER'], ['mime_type', 'TEXT'],  
    #      ['source_data', 'TEXT'], ['source_package', 'TEXT'], ['state', 'INTEGER']]
    ## Tuple Definition -> the integers in this tuple represent the
    ## corresponding columns of the database table of the above table design
    CALL_LOG_ENTRIES_LIST = config.call_log_entry_positions
    ######################################################################################################################################################
    if os.path.isfile(db_file_call_logs):
        _adel_log.log("parseDBs:      ----> starting to parse \033[0;32mcall logs\033[m", 0)
        call_log_list = []
        try:
            result_list = _sqliteParser.parse_db(db_file_call_logs)
            for i in range(1, len(result_list[CALL_LOG_TABLE_NUMBER])):
                # call_log_list = [[id, number, date, duration, type, name],[......],......]
                if os_version == "442":
                    call_log_list.append([
                        str(result_list[CALL_LOG_TABLE_NUMBER][i][CALL_LOG_ENTRIES_LIST[0]]),
                        str(result_list[CALL_LOG_TABLE_NUMBER][i][CALL_LOG_ENTRIES_LIST[1]]),
                        time.strftime("%a, %d %B %Y %H:%M:%S",time.gmtime(result_list[CALL_LOG_TABLE_NUMBER][i][CALL_LOG_ENTRIES_LIST[2]] / 1000.0)),
                        str(result_list[CALL_LOG_TABLE_NUMBER][i][CALL_LOG_ENTRIES_LIST[3]]),
                        str(result_list[CALL_LOG_TABLE_NUMBER][i][CALL_LOG_ENTRIES_LIST[4]]), 
                        string_replace(str(result_list[CALL_LOG_TABLE_NUMBER][i][CALL_LOG_ENTRIES_LIST[6]]))])
                else:
                    call_log_list.append([
                        str(result_list[CALL_LOG_TABLE_NUMBER][i][CALL_LOG_ENTRIES_LIST[0]]),
                        str(result_list[CALL_LOG_TABLE_NUMBER][i][CALL_LOG_ENTRIES_LIST[1]]),
                        time.strftime("%a, %d %B %Y %H:%M:%S",time.gmtime(result_list[CALL_LOG_TABLE_NUMBER][i][CALL_LOG_ENTRIES_LIST[2]] / 1000.0)),
                        str(result_list[CALL_LOG_TABLE_NUMBER][i][CALL_LOG_ENTRIES_LIST[3]]),
                        str(result_list[CALL_LOG_TABLE_NUMBER][i][CALL_LOG_ENTRIES_LIST[4]]), 
                        string_replace(str(result_list[15][i][CALL_LOG_ENTRIES_LIST[5]]))])
        except:
            _adel_log.log("analyzeDBs:    ----> it seems that there are no call logs or that the database has an unsupported encoding!", 1)
        _xmlParser.call_log_to_xml(xml_dir, call_log_list)
    else:
        _adel_log.log("analyzeDBs:    ----> database file " + db_file_call_logs.split("/")[2] + " missing!", 1)

def analyze_sms_mss(backup_dir, os_version, xml_dir, config):
    ######################################################################################################################################################
    #                                                           definition of Tuples                                                                     #
    ######################################################################################################################################################
    # SMS MMS Messages
    ## Database Name
    db_file_sms = backup_dir + "/" + config.db_file_sms
    ######################################################################################################################################################
    ## Table Name
    #### sms
    ## corresponding table number in the database
    SMS_TABLE_NUMBER = config.sms_table_num
    ## Table Design
    #### [[['_id', 'INTEGER'], ['thread_id', 'INTEGER'], ['address', 'TEXT'], ['person', 'INTEGER'], ['date', 'INTEGER'], ['date_sent', 'INTEGER'],  
    #      ['protocol', 'INTEGER'], ['read', 'INTEGER'], ['status', 'INTEGER'], ['type', 'INTEGER'], ['reply_path_present', 'INTEGER'], ['subject', 'TEXT'], 
    #      ['body', 'TEXT'], ['service_center', 'TEXT'], ['locked', 'INTEGER'], ['error_code', 'INTEGER'], ['seen', 'INTEGER']]
    ## Tuple Definition -> the integers in this tuple represent the corresponding columns of the database table of the above table design
    SMS_ENTRIES_LIST = config.sms_entry_positions
    ######################################################################################################################################################
    if os.path.isfile(db_file_sms):
        _adel_log.log("parseDBs:      ----> starting to parse \033[0;32mSMS messages\033[m", 0)
        sms_list = []
        try:
            result_list = _sqliteParser.parse_db(db_file_sms)
            for i in range(1, len(result_list[SMS_TABLE_NUMBER])):
                # sms_list = [[id, thread_id, number, person, date, read, type, subject, body],[......],......]
                sms_list.append([
                    str(result_list[SMS_TABLE_NUMBER][i][SMS_ENTRIES_LIST[0]]),
                    str(result_list[SMS_TABLE_NUMBER][i][SMS_ENTRIES_LIST[1]]),
                    str(result_list[SMS_TABLE_NUMBER][i][SMS_ENTRIES_LIST[2]]),
                    str(result_list[SMS_TABLE_NUMBER][i][SMS_ENTRIES_LIST[3]]),
                    time.strftime("%a, %d %B %Y %H:%M:%S", time.gmtime(result_list[SMS_TABLE_NUMBER][i][SMS_ENTRIES_LIST[4]] / 1000.0)),
                    str(result_list[SMS_TABLE_NUMBER][i][SMS_ENTRIES_LIST[5]]),
                    str(result_list[SMS_TABLE_NUMBER][i][SMS_ENTRIES_LIST[6]]),
                    str(result_list[SMS_TABLE_NUMBER][i][SMS_ENTRIES_LIST[7]]),
                    string_replace(str(result_list[SMS_TABLE_NUMBER][i][SMS_ENTRIES_LIST[8]]))
                    ])
        except:
            _adel_log.log("analyzeDBs:    ----> it seems that there are no SMS or MMS messages or that the database has an unsupported encoding!", 1)
        _xmlParser.sms_messages_to_xml(xml_dir, sms_list)
    else:
        _adel_log.log("analyzeDBs:    ----> database file " + db_file_sms.split("/")[2] + " missing!", 1) 
  
def analyze_calendar(backup_dir, os_version, xml_dir, config):
    ######################################################################################################################################################
    #                                                           definition of Tuples                                                                     #
    ######################################################################################################################################################
    # CALENDAR ENTRIES
    ## Database Name
    db_file_calendar = backup_dir + "/" + config.db_file_calendar
    ######################################################################################################################################################
    ## Table Name
    #### calendars
    ## corresponding table number in the database
    CALENDAR_NAME_TABLE_NUMBER = config.calendar_name_table_num
    ## Table Design
    #### ['_id', 'INTEGER'], ['account_name', 'TEXT'], ['account_type', 'TEXT'], ['_sync_id', 'TEXT'], ['dirty', 'INTEGER'], ['mutators', 'TEXT'], 
    #    ['name', 'TEXT'], ['calendar_displayName', 'TEXT'], ['calendar_color', 'INTEGER'], ['calendar_color_index', 'TEXT'], ['calendar_access_level', 'INTEGER'], 
    #    ['visible', 'INTEGER'], ['sync_events', 'INTEGER'], ['calendar_location', 'TEXT'], ['calendar_timezone', 'TEXT'], ['ownerAccount', 'TEXT'], 
    #    ['isPrimary', 'INTEGER'], ['canOrganizerRespond', 'INTEGER'], ['canModifyTimeZone', 'INTEGER'], ['canPartiallyUpdate', 'INTEGER'], 
    #    ['maxReminders', 'INTEGER'], ['allowedReminders', 'TEXT'], "1'", ['allowedAvailability', 'TEXT'], "1'", ['allowedAttendeeTypes', 'TEXT'], '1', "2'", 
    #    ['deleted', 'INTEGER'], ['cal_sync1', 'TEXT'], ['cal_sync2', 'TEXT'], ['cal_sync3', 'TEXT'], ['cal_sync4', 'TEXT'], ['cal_sync5', 'TEXT'], 
    #    ['cal_sync6', 'TEXT'], ['cal_sync7', 'TEXT'], ['cal_sync8', 'TEXT'], ['cal_sync9', 'TEXT'], ['cal_sync10', 'TEXT']
    ## Tuple Definition -> the integers in this tuple represent the corresponding columns of the database table of the above table design
    CALENDARS_NAME_LIST = config.calendar_name_list
    ######################################################################################################################################################
    ## Table Name
    #### events
    ## corresponding table number in the database
    CALENDAR_EVENTS_TABLE_NUMBER = config.calendar_events_table_num
    ## Table Design
    #### ['_id', 'INTEGER'], ['_sync_id', 'TEXT'], ['dirty', 'INTEGER'], ['mutators', 'TEXT'], ['lastSynced', 'INTEGER'], ['calendar_id', 'INTEGER'], 
    #    ['title', 'TEXT'], ['eventLocation', 'TEXT'], ['description', 'TEXT'], ['eventColor', 'INTEGER'], ['eventColor_index', 'TEXT'], 
    #    ['eventStatus', 'INTEGER'], ['selfAttendeeStatus', 'INTEGER'], ['dtstart', 'INTEGER'], ['dtend', 'INTEGER'], ['eventTimezone', 'TEXT'], 
    #    ['duration', 'TEXT'], ['allDay', 'INTEGER'], ['accessLevel', 'INTEGER'], ['availability', 'INTEGER'], ['hasAlarm', 'INTEGER'], 
    #    ['hasExtendedProperties', 'INTEGER'], ['rrule', 'TEXT'], ['rdate', 'TEXT'], ['exrule', 'TEXT'], ['exdate', 'TEXT'], ['original_id', 'INTEGER'], 
    #    ['original_sync_id', 'TEXT'], ['originalInstanceTime', 'INTEGER'], ['originalAllDay', 'INTEGER'], ['lastDate', 'INTEGER'], ['hasAttendeeData', 'INTEGER'], 
    #    ['guestsCanModify', 'INTEGER'], ['guestsCanInviteOthers', 'INTEGER'], ['guestsCanSeeGuests', 'INTEGER'], ['organizer', 'STRING'], 
    #    ['isOrganizer', 'INTEGER'], ['deleted', 'INTEGER'], ['eventEndTimezone', 'TEXT'], ['customAppPackage', 'TEXT'], ['customAppUri', 'TEXT'], ['uid2445', 'TEXT'], 
    #    ['sync_data1', 'TEXT'], ['sync_data2', 'TEXT'], ['sync_data3', 'TEXT'], ['sync_data4', 'TEXT'], ['sync_data5', 'TEXT'], ['sync_data6', 'TEXT'], 
    #    ['sync_data7', 'TEXT'], ['sync_data8', 'TEXT'], ['sync_data9', 'TEXT'], ['sync_data10', 'TEXT']
    ## Tuple Definition -> the integers in this tuple represent the corresponding columns of the database table of the above table design
    CALENDAR_EVENTS_LIST = config.calendar_events_list
    ######################################################################################################################################################
    if os.path.isfile(db_file_calendar):
        _adel_log.log("parseDBs:      ----> starting to parse \033[0;32mcalendar entries\033[m", 0)
        calendar_list = []
        try:
            result_list = _sqliteParser.parse_db(db_file_calendar)
            for i in range(1, len(result_list[CALENDAR_EVENTS_TABLE_NUMBER])):
                if str(result_list[CALENDAR_EVENTS_TABLE_NUMBER][i][CALENDAR_EVENTS_LIST[6]]) != "None":
                    end = time.strftime("%a, %d %B %Y %H:%M:%S", time.gmtime(result_list[CALENDAR_EVENTS_TABLE_NUMBER][i][CALENDAR_EVENTS_LIST[6]] / 1000.0))
                else:
                    end = time.strftime("%a, %d %B %Y %H:%M:%S", time.gmtime(result_list[CALENDAR_EVENTS_TABLE_NUMBER][i][CALENDAR_EVENTS_LIST[5]] / 1000.0))
                # calendar_list = [[id, calendarName, title, eventLocation, description, allDay, start, end, hasAlarm],[......],......]
                calendar_list.append([
                    str(result_list[CALENDAR_EVENTS_TABLE_NUMBER][i][CALENDAR_EVENTS_LIST[0]]),
                    str(result_list[CALENDAR_NAME_TABLE_NUMBER][result_list[CALENDAR_EVENTS_TABLE_NUMBER][i][CALENDAR_EVENTS_LIST[1]]][CALENDARS_NAME_LIST[1]]),
                    string_replace(str(result_list[CALENDAR_EVENTS_TABLE_NUMBER][i][CALENDAR_EVENTS_LIST[2]])),
                    string_replace(str(result_list[CALENDAR_EVENTS_TABLE_NUMBER][i][CALENDAR_EVENTS_LIST[3]])),
                    string_replace(str(result_list[CALENDAR_EVENTS_TABLE_NUMBER][i][CALENDAR_EVENTS_LIST[4]])),
                    str(result_list[CALENDAR_EVENTS_TABLE_NUMBER][i][CALENDAR_EVENTS_LIST[7]]),
                    time.strftime("%a, %d %B %Y %H:%M:%S", time.gmtime(result_list[CALENDAR_EVENTS_TABLE_NUMBER][i][CALENDAR_EVENTS_LIST[5]] / 1000.0)),
                    end,
                    str(result_list[CALENDAR_EVENTS_TABLE_NUMBER][i][CALENDAR_EVENTS_LIST[8]])
                    ])
        except:
            _adel_log.log("analyzeDBs:    ----> it seems that there are no entries in the calendar or that the database has an unsupported encoding!", 1)
        _xmlParser.calendar_to_xml(xml_dir, calendar_list)
    else:
        _adel_log.log("analyzeDBs:    ----> database file " + db_file_calendar.split("/")[2] + " missing!", 1)

def analyze_contacts(backup_dir, os_version, xml_dir, config):
    ######################################################################################################################################################
    #                                                           definition of Tuples                                                                     #
    ######################################################################################################################################################
    # CONTACTS ENTRIES
    ## Database Name
    db_file_contacts = backup_dir + "/" + config.db_file_contacts
    ######################################################################################################################################################
    ## Table Name
    #### contacts
    ## corresponding table number in the database
    CONTACTS_TABLE_NUMBER = config.contacts_normal_table_num
    ## Table Design
    #### [['_id', 'INTEGER'], ['name_raw_contact_id', 'INTEGER'], ['photo_id', 'INTEGER'], ['photo_file_id', 'INTEGER'], ['custom_ringtone', 'TEXT'], 
    #    ['send_to_voicemail', 'INTEGER'], ['times_contacted', 'INTEGER'], ['last_time_contacted', 'INTEGER'], ['starred', 'INTEGER'], ['pinned', 'INTEGER'], 
    #    ['has_phone_number', 'INTEGER'], ['lookup', 'TEXT'], ['status_update_id', 'INTEGER'], ['contact_last_updated_timestamp', 'INTEGER']]
    ## Tuple Definition -> the integers in this tuple represent the corresponding columns of the database table of the above table design
    CONTACTS_LIST = config.contacts_normal_list
    ######################################################################################################################################################
    ## Table Name
    #### raw_contacts
    ## corresponding table number in the database
    RAW_CONTACTS_TABLE_NUMBER = config.raw_contacts_table_num
    ## Table Design
    #### [['_id', 'INTEGER'], ['account_id', 'INTEGER'], ['sourceid', 'TEXT'], ['raw_contact_is_read_only', 'INTEGER'], ['version', 'INTEGER'], 
    #    ['dirty', 'INTEGER'], ['deleted', 'INTEGER'], ['contact_id', 'INTEGER'], ['aggregation_mode', 'INTEGER'], ['aggregation_needed', 'INTEGER'], 
    #    ['custom_ringtone', 'TEXT'], ['send_to_voicemail', 'INTEGER'], ['times_contacted', 'INTEGER'], ['last_time_contacted', 'INTEGER'], 
    #    ['starred', 'INTEGER'], ['pinned', 'INTEGER'], ['display_name', 'TEXT'], ['display_name_alt', 'TEXT'], ['display_name_source', 'INTEGER'], 
    #    ['phonetic_name', 'TEXT'], ['phonetic_name_style', 'TEXT'], ['sort_key', 'TEXT'], ['phonebook_label', 'TEXT'], ['phonebook_bucket', 'INTEGER'], 
    #    ['sort_key_alt', 'TEXT'], ['phonebook_label_alt', 'TEXT'], ['phonebook_bucket_alt', 'INTEGER'], ['name_verified', 'INTEGER'], ['sync1', 'TEXT'], 
    #    ['sync2', 'TEXT'], ['sync3', 'TEXT'], ['sync4', 'TEXT']]    
    ## Tuple Definition -> the integers in this tuple represent the corresponding columns of the database table of the above table design
    RAW_CONTACTS_LIST = config.raw_contacts_list

    RAW_CONTACTS_LIST_DELETED = config.raw_contacts_deleted_list
    ######################################################################################################################################################
    ## Table Name
    #### data
    ## corresponding table number in the database
    DATA_TABLE_NUMBER = config.data_table_num
    ## Table Design
    #### [['_id', 'INTEGER'], ['package_id', 'INTEGER'], ['mimetype_id', 'INTEGER'], ['raw_contact_id', 'INTEGER'], ['is_read_only', 'INTEGER'], 
    #    ['is_primary', 'INTEGER'], ['is_super_primary', 'INTEGER'], ['data_version', 'INTEGER'], ['data1', 'TEXT'], ['data2', 'TEXT'], ['data3', 'TEXT'], 
    #    ['data4', 'TEXT'], ['data5', 'TEXT'], ['data6', 'TEXT'], ['data7', 'TEXT'], ['data8', 'TEXT'], ['data9', 'TEXT'], ['data10', 'TEXT'], 
    #    ['data11', 'TEXT'], ['data12', 'TEXT'], ['data13', 'TEXT'], ['data14', 'TEXT'], ['data15', 'TEXT'], ['data_sync1', 'TEXT'], ['data_sync2', 'TEXT'], 
    #    ['data_sync3', 'TEXT'], ['data_sync4', 'TEXT']]
    ## Tuple Definition -> the integers in this tuple represent the corresponding columns of the database table of the above table design
    DATA_ENTRY_LIST = config.data_entry_list
    ######################################################################################################################################################
    ## Table Name
    #### mimetypes
    ## corresponding table number in the database
    MIME_TABLE_NUMBER = config.mime_table_num
    ## Table Design and matching mimetypes for the contact entries
    #### [['_id', 'INTEGER'], ['mimetype', 'TEXT']]
    #    [1, 'vnd.android.cursor.item/email_v2'], [2, 'vnd.android.cursor.item/im'], [3, 'vnd.android.cursor.item/nickname'], 
    #    [4, 'vnd.android.cursor.item/organization'], [5, 'vnd.android.cursor.item/phone_v2'], [6, 'vnd.android.cursor.item/sip_address'], 
    #    [7, 'vnd.android.cursor.item/name'], [8, 'vnd.android.cursor.item/postal-address_v2'], [9, 'vnd.android.cursor.item/identity'], 
    #    [10, 'vnd.android.cursor.item/photo'], [11, 'vnd.android.cursor.item/group_membership']]
    MIME_TYPE_LIST = config.mime_type_entry_list
    ######################################################################################################################################################
    if os.path.isfile(db_file_contacts):
        _adel_log.log("parseDBs:      ----> starting to parse \033[0;32maddress book entries\033[m", 0)
        contacts_list = []
        try:
            result_list = _sqliteParser.parse_db(db_file_contacts)
            for i in range(1, len(result_list[CONTACTS_TABLE_NUMBER])):
                email = "None"
                url = "None"
                lastname = "None"
                firstname = "None"
                number = "None"
                address = "None"
                company = "None"
                # convert the date and time of the last call to this contact
                if result_list[CONTACTS_TABLE_NUMBER][i][CONTACTS_LIST[3]] == 0:
                    last_time_contacted = "NEVER"
                else:
                    last_time_contacted = time.strftime("%a, %d %B %Y %H:%M:%S", time.gmtime(result_list[CONTACTS_TABLE_NUMBER][i][CONTACTS_LIST[3]] / 1000.0))
                # search the display name and other data for this contact
                for j in range(1, len(result_list[RAW_CONTACTS_TABLE_NUMBER])):
                    # display name
                    if result_list[RAW_CONTACTS_TABLE_NUMBER][j][RAW_CONTACTS_LIST[0]] == result_list[CONTACTS_TABLE_NUMBER][i][CONTACTS_LIST[0]]:
                        display_name = string_replace(str(result_list[RAW_CONTACTS_TABLE_NUMBER][j][RAW_CONTACTS_LIST[1]]))
                        # other data like name, phone number, etc. => identified by mimetype
                        for k in range(1, len(result_list[DATA_TABLE_NUMBER])):
                            if result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[1]] == j and result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[0]] == MIME_TYPE_LIST[3]:
                                lastname = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[4]]))
                                firstname = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[3]]))
                                break;
                            else:
                                continue;
                        for k in range(1, len(result_list[DATA_TABLE_NUMBER])):
                            if result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[1]] == j and result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[0]] == MIME_TYPE_LIST[0]:
                                if email == "None":
                                    email = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                                else:
                                    email = email + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                            else:
                                continue;
                        for k in range(1, len(result_list[DATA_TABLE_NUMBER])):
                            if result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[1]] == j and result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[0]] == MIME_TYPE_LIST[4]:
                                if url == "None":
                                    url = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                                else:
                                    url = url + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                            else:
                                continue;
                        for k in range(1, len(result_list[DATA_TABLE_NUMBER])):
                            if result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[1]] == j and result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[0]] == MIME_TYPE_LIST[2]:
                                if number == "None":
                                    number = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                                else:
                                    number = number + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                            else:
                                continue;
                        for k in range(1, len(result_list[DATA_TABLE_NUMBER])):
                            if result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[1]] == j and result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[0]] == MIME_TYPE_LIST[1]:
                                if "\n" in string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[5]])):
                                    _adel_log.log("analyzeDBs:    ----> check formatting of postal address for contact with id " + str(result_list[CONTACTS_TABLE_NUMBER][i][CONTACTS_LIST[0]]) + "!", 2)
                                    address = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[5]]))
                                else:
                                    if address == "None":
                                        address = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[5]])) + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[8]])) + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[10]])) + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[11]]))
                                    else:
                                        address = address + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                            else:
                                continue;
                        for k in range(1, len(result_list[DATA_TABLE_NUMBER])):
                            if result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[1]] == j and result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[0]] == MIME_TYPE_LIST[5]:
                                if company == "None":
                                    company = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                                else:
                                    company = company + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                            else:
                                continue;
                        break;
                    else:
                        continue;
                # contacts_list = [[id, photo_id, times_contacted, last_time_contacted, starred, number, display_name, lastname, firstname, company, email, url, address],[......],.....]
                contacts_list.append([
                    str(result_list[CONTACTS_TABLE_NUMBER][i][CONTACTS_LIST[0]]),
                    str(result_list[CONTACTS_TABLE_NUMBER][i][CONTACTS_LIST[1]]),
                    str(result_list[CONTACTS_TABLE_NUMBER][i][CONTACTS_LIST[2]]),
                    last_time_contacted,
                    str(result_list[CONTACTS_TABLE_NUMBER][i][CONTACTS_LIST[4]]),
                    number,
                    display_name,
                    lastname,
                    firstname,
                    company,
                    email,
                    url,
                    address
                    ])
            # search for deleted entries and gather information
            for j in range(1, len(result_list[RAW_CONTACTS_TABLE_NUMBER])):
                del_email = "None"
                del_url = "None"
                del_lastname = "None"
                del_firstname = "None"
                del_number = "None"
                del_address = "None"
                del_company = "None"
                if result_list[RAW_CONTACTS_TABLE_NUMBER][j][RAW_CONTACTS_LIST_DELETED[1]] == 1:
                    _adel_log.log("analyzeDBs:    ----> found deleted contact entry!", 3)
                    # convert the date and time of the last call to this contact
                    if result_list[RAW_CONTACTS_TABLE_NUMBER][j][RAW_CONTACTS_LIST_DELETED[3]] == None:
                        del_last_time_contacted = "NEVER"
                    else:
                        del_last_time_contacted = time.strftime("%a, %d %B %Y %H:%M:%S", time.gmtime(result_list[RAW_CONTACTS_TABLE_NUMBER][j][RAW_CONTACTS_LIST_DELETED[3]] / 1000.0))
                    del_times_contacted = str(result_list[RAW_CONTACTS_TABLE_NUMBER][j][RAW_CONTACTS_LIST_DELETED[2]])
                    del_starred = str(result_list[RAW_CONTACTS_TABLE_NUMBER][j][RAW_CONTACTS_LIST_DELETED[4]])
                    del_display_name = string_replace(str(result_list[RAW_CONTACTS_TABLE_NUMBER][j][RAW_CONTACTS_LIST_DELETED[5]]))
                    # other data like name, phone number, etc. => identified by mimetype
                    for k in range(1, len(result_list[DATA_TABLE_NUMBER])):
                        if result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[1]] == j and result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[0]] == MIME_TYPE_LIST[3]:
                            del_lastname = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[4]]))
                            del_firstname = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[3]]))
                            break;
                        else:
                            continue;
                    for k in range(1, len(result_list[DATA_TABLE_NUMBER])):
                        if result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[1]] == j and result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[0]] == MIME_TYPE_LIST[0]:
                            if del_email == "None":
                                del_email = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                            else:
                                del_email = del_email + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                        else:
                            continue;
                    for k in range(1, len(result_list[DATA_TABLE_NUMBER])):
                        if result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[1]] == j and result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[0]] == MIME_TYPE_LIST[4]:
                            if del_url == "None":
                                del_url = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                            else:
                                del_url = del_url + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                        else:
                            continue;
                    for k in range(1, len(result_list[DATA_TABLE_NUMBER])):
                        if result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[1]] == j and result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[0]] == MIME_TYPE_LIST[2]:
                            if del_number == "None":
                                del_number = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                            else:
                                del_number = del_number + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                        else:
                            continue;
                    for k in range(1, len(result_list[DATA_TABLE_NUMBER])):
                        if result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[1]] == j and result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[0]] == MIME_TYPE_LIST[1]:
                            if "\n" in string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[5]])):
                                _adel_log.log("analyzeDBs:    ----> check formatting of postal address for contact with id " + str(result_list[CONTACTS_TABLE_NUMBER][i][CONTACTS_LIST[0]]) + "!", 2)
                                del_address = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[5]]))
                            else:
                                if del_address == "None":
                                    del_address = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[5]])) + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[8]])) + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[10]])) + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[11]]))
                                else:
                                    del_address = del_address + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                        else:
                            continue;
                    for k in range(1, len(result_list[DATA_TABLE_NUMBER])):
                        if result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[1]] == j and result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[0]] == MIME_TYPE_LIST[5]:
                            if del_company == "None":
                                del_company = string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                            else:
                                del_company = del_company + ";" + string_replace(str(result_list[DATA_TABLE_NUMBER][k][DATA_ENTRY_LIST[2]]))
                        else:
                            continue;
                else:
                    continue;
                # contacts_list = [[id, photo_id, times_contacted, last_time_contacted, starred, number, display_name, lastname, firstname, company, email, url, address],[......],.....]
                contacts_list.append([
                    "DELETED",
                    "DELETED",
                    del_times_contacted,
                    del_last_time_contacted,
                    del_starred,
                    del_number,
                    del_display_name,
                    del_lastname,
                    del_firstname,
                    del_company,
                    del_email,
                    del_url,
                    del_address
                    ])
        except:
            _adel_log.log("analyzeDBs:    ----> it seems that the contact list is empty or that the database has an unsupported encoding!", 1)
        _xmlParser.contacts_to_xml(xml_dir, contacts_list)
    else:
        _adel_log.log("analyzeDBs:    ----> database file " + db_file_contacts.split("/")[2] + " missing!", 1)

def phone_info(backup_dir, os_version, xml_dir, handheld_id, config):
    ######################################################################################################################################################
    #                                                           definition of Tuples                                                                     #
    ######################################################################################################################################################
    # SMARTPHONE INFORMATION
    ## Database Name
    db_file_info_1 = backup_dir + "/" +  config.file_info1_db_name
    ACCOUNTS_TABLE_NUMBER = config.file_info1_table_num
    ######################################################################################################################################################
    ## Table Design
    #### [['row_id', 'INTEGER'], ['account_name', 'TEXT'], ['account_type', 'TEXT']]
    ## Tuple Definition -> the integers in this tuple represent the corresponding columns of the database table of the above table design
    ACCOUNTS_ENTRIES = config.account_entry_list
    ######################################################################################################################################################
    ## Database Name
    db_file_info_2 = backup_dir + "/" + config.file_info2_db_name
    ######################################################################################################################################################
    ## Table Name
    #### meta
    ## corresponding table number in the database
    META_TABLE_NUMBER = config.file_info2_table_num
    ## Table Design
    #### [['key', 'TEXT'], ['value', 'TEXT']]
    ## Tuple Definition -> the integers in this tuple represent the corresponding columns of the database table of the above table design
    META_ENTRY = config.meta_entry_list[0] # only one element 
    ######################################################################################################################################################
    ## Database Name
    db_file_info_3 = backup_dir + "/" + config.file_info3_db_name
    ######################################################################################################################################################
    ## Table Name
    #### secure
    ## corresponding table number in the database
    ID_TABLE_NUMBER = config.file_info3_table_num
    ## Table Design
    #### [['_id', 'INTEGER'],['name', 'TEXT'],['value', 'TEXT']]
    ## Tuple Definition -> the integers in this tuple represent the corresponding columns of the database table of the above table design
    ID_ENTRIES = config.settings_entry_list
    ######################################################################################################################################################
    _adel_log.log("parseDBs:      ----> starting to parse \033[0;32msmartphone info\033[m", 0)
    if os.path.isfile(db_file_info_1):
        try:
            result_list_1 = _sqliteParser.parse_db(db_file_info_1)
            account_name = str(result_list_1[ACCOUNTS_TABLE_NUMBER][1][ACCOUNTS_ENTRIES[0]])
            account_type = str(result_list_1[ACCOUNTS_TABLE_NUMBER][1][ACCOUNTS_ENTRIES[1]])
        except:
            _adel_log.log("analyzeDBs:    ----> can't get required data from " + db_file_info_1.split("/")[2] + "! Please check manually for account data.", 1)
            account_name = "not available"
            account_type = "not available"
    else:
        account_name = "not available"
        account_type = "not available"
    if os.path.isfile(db_file_info_2):
        try:
            result_list_2 = _sqliteParser.parse_db(db_file_info_2)
            imsi = str(result_list_2[META_TABLE_NUMBER][1][META_ENTRY])
        except:
            _adel_log.log("analyzeDBs:    ----> can't get required data from " + db_file_info_2.split("/")[2] + "! Please check manually for IMSI.", 1)
            imsi = "not available"
    else:
        imsi = "not available"
    if os.path.isfile(db_file_info_3):
        try:
            result_list_3 = _sqliteParser.parse_db(db_file_info_3)
            android_id = str(result_list_3[ID_TABLE_NUMBER][ID_ENTRIES[1]][ID_ENTRIES[0]])
        except:
            _adel_log.log("analyzeDBs:    ----> can't get required data from " + db_file_info_3.split("/")[2] + "! Please check manually for android ID.", 1)
            android_id = "not available"
    else:
        android_id = "not available"
    model = subprocess.Popen(['adb', 'shell', 'getprop', 'ro.product.model'], stdout=subprocess.PIPE).communicate(0)[0]
    phone_info_list = [account_name, account_type, imsi, android_id, handheld_id, model, os_version]
    _xmlParser.smartphone_info_to_xml(xml_dir, phone_info_list)

def analyze_twitter(backup_dir, os_version, xml_dir, twitter_dbname_list, config):
    twitter_dbname_list.sort
    ######################################################################################################################################################
    ##Table name
    #### {user_id}.db
    TWITTER_USERS_TABLE = config.twitter_user_table_num
    ## Table Design
    #### [0 ['_id', 'Int'],
    ####  1 ['user_id', 'Int'],
    ####  2 ['username', 'TEXT'],
    ####  3 ['name', 'TEXT'],
    ####  4 ['description', 'TEXT'],
    ####  5 ['web_url', 'TEXT'],
    ####  7 ['location', 'TEXT'],
    #### 10 ['followers', 'Int'],
    #### 11 ['friends', 'Int'],
    #### 13 ['geo_enable', 'Int'],
    #### 14 ['profile_created', 'Int'],
    #### 15 ['image_url', 'TEXT'],
    #### 17 ['updated', 'Int']]
    TWITTER_USERS_USER_ID = config.twitter_user_list[0]
    TWITTER_USERS_USERNAME = config.twitter_user_list[1]
    TWITTER_USERS_NAME = config.twitter_user_list[2]
    TWITTER_USERS_DESCRIPTION = config.twitter_user_list[3]
    TWITTER_USERS_LOCATION = config.twitter_user_list[4]
    TWITTER_USERS_FOLLOWERS = config.twitter_user_list[5]
    TWITTER_USERS_FRIENDS = config.twitter_user_list[6]
    TWITTER_USERS_GEO_ENABLE = config.twitter_user_list[7]
    TWITTER_USERS_PROFILE_CREATED = config.twitter_user_list[8]
    TWITTER_USERS_UPDATED = config.twitter_user_list[9]
    ##
    ## Table Name
    #### statuses
    TWITTER_STATUSES_TABLE = config.statuses_table_num
    ## Table Design
    #### [0 ['_id', 'Int'],
    ####  1 ['status_id', 'Int'],
    ####  2 ['author_id', 'Int'],        seems to correspond to TWITTER_USERS_TABLE [1 ['user_id', 'Int']]
    ####  3 ['content', 'TEXT'],
    ####  4 ['source', 'TEXT']
    ####  5 ['source_url', 'TEXT']
    ####  6 ['created', 'Int']
    TWITTER_STATUSES_AUTHOR_ID = config.twitter_statuses_list[0]
    TWITTER_STATUSES_CONTENT = config.twitter_statuses_list[1]
    TWITTER_STATUSES_SOURCE = config.twitter_statuses_list[2]
    TWITTER_STATUSES_SOURCE_URL = config.twitter_statuses_list[3]
    TWITTER_STATUSES_CREATED = config.twitter_statuses_list[4]

    for k in range (0, len(twitter_dbname_list)):    
        twitter_db_name = backup_dir + "/" + twitter_dbname_list[k]
        if twitter_db_name.split("/")[-1] == "0.db":
            continue
        elif twitter_db_name.split("/")[-1] == "twitter.db":
            continue
        elif twitter_db_name.split("/")[-1] == "global.db":
            continue
        else:
            if os.path.isfile(twitter_db_name):
                    _adel_log.log("parseDBs:      ----> starting to parse \033[0;32m" + twitter_db_name.split("/")[-1] + "\033[m", 0)
                    users_list = []
                    temp_list = _sqliteParser.parse_db(twitter_db_name)
                    try:
                        for i in range (1, len(temp_list[TWITTER_USERS_TABLE])): 
                            ## Entry generated is User_ID, User_Name, Real_Name, description, location (if given), profile_created, updated, followers, friends
                            if temp_list[TWITTER_USERS_TABLE][i][TWITTER_USERS_GEO_ENABLE] == 1:
                                location = str(temp_list[TWITTER_USERS_TABLE][i][TWITTER_USERS_LOCATION])
                            else:
                                location = "no location"  
                            users_list.append([
                            filter(lambda x: x in string.printable, str(temp_list[TWITTER_USERS_TABLE][i][TWITTER_USERS_USER_ID])),
                            filter(lambda x: x in string.printable, str(temp_list[TWITTER_USERS_TABLE][i][TWITTER_USERS_USERNAME])),
                            filter(lambda x: x in string.printable, str(temp_list[TWITTER_USERS_TABLE][i][TWITTER_USERS_NAME])),
                            filter(lambda x: x in string.printable, str(temp_list[TWITTER_USERS_TABLE][i][TWITTER_USERS_DESCRIPTION])),
                            location,
                            time.strftime("%a, %d %B %Y %H:%M:%S", time.gmtime((temp_list[TWITTER_USERS_TABLE][i][TWITTER_USERS_PROFILE_CREATED]) / 1000)),
                            time.strftime("%a, %d %B %Y %H:%M:%S", time.gmtime((temp_list[TWITTER_USERS_TABLE][i][TWITTER_USERS_UPDATED]) / 1000)),
                            filter(lambda x: x in string.printable, str(temp_list[TWITTER_USERS_TABLE][i][TWITTER_USERS_FOLLOWERS])),
                            filter(lambda x: x in string.printable, str(temp_list[TWITTER_USERS_TABLE][i][TWITTER_USERS_FRIENDS])),
                            ])  
                            #_adel_log.log(users_list[0][0],users_list[0][1],users_list[0][2],users_list[0][3],users_list[0][4],users_list[0][5],users_list[0][6],users_list[0][7],users_list[0][8])
                    except:           
                        _adel_log.log("analyzeDBs:    ----> can't get required user data from " + twitter_db_name.split("/")[-1] + " ! DB structure changed?", 1)
                        continue
                    messages_list = {}
                    try:
                        for j in range (1, len(temp_list[TWITTER_STATUSES_TABLE])):
                            k = temp_list[TWITTER_STATUSES_TABLE][j][TWITTER_STATUSES_AUTHOR_ID]
                            if temp_list[TWITTER_STATUSES_TABLE][j][TWITTER_STATUSES_SOURCE_URL] == None:
                                source_url = "n.a."
                            else:
                                source_url = temp_list[TWITTER_STATUSES_TABLE][j][TWITTER_STATUSES_SOURCE_URL]
                            m = (string_replace(str(temp_list[TWITTER_STATUSES_TABLE][j][TWITTER_STATUSES_CONTENT])), string_replace(str(temp_list[TWITTER_STATUSES_TABLE][j][TWITTER_STATUSES_SOURCE])), source_url, time.strftime("%a, %d %B %Y %H:%M:%S", time.gmtime(temp_list[TWITTER_STATUSES_TABLE][j][TWITTER_STATUSES_CREATED] / 1000)))
                            if messages_list.has_key(k):
                                messages_list[k].append(m)
                            else:
                                entry = []
                                entry.append(m)                  
                                messages_list[k] = entry     
                    except:           
                        _adel_log.log("analyzeDBs:    ----> can't get required status data from " + twitter_db_name.split("/")[-1] + " ! DB structure changed?", 1)
                        continue
                    _xmlParser.twitter_to_xml(xml_dir, users_list, messages_list) 
            else:
                    _adel_log.log("analyzeDBs:   ----> database file " + twitter_db_name.split("/")[-1] + " missing!", 1)

def analyze_facebook(backup_dir, os_version, xml_dir, config):
    FB_DB_FILENAME = backup_dir + config.fb_db_filename
    ######################################################################################################################################################
    ## Table Name
    #### user_values
    FB_USER_VALUES_TABLE = config.fb_users_values_table_num
    ## table design
    ## 1 name
    ## 2 value
    ## FB puts some interesting information into this by filling the name/value slots with information. the following entries where of interest.
    ## it has to be tested if other accounts put the information in a different order. currently the order looks like this:
    ## 2 active_session_info -> div. Infos in a {dict} Structur
    ## 4 last_contacts_sync -> timestamp
    ## 5 current_account -> Username of the FB user
    ## 5 last_seen_id_message     \
    ## 6 last_seen_id_poke         \
    ## 7 last_seen_id_friend_request\
    ## 8 last_seen_id_event_invite  -> no field description in sql -> flags?
    FB_USER_VALUES_ACTIVE_SESSION_INFO = config.fb_users_values_list[0]
    FB_USER_VALUES_LAST_CONTACTS_SYNC = config.fb_users_values_list[1]
    FB_USER_VALUES_CURRENT_ACCOUNT = config.fb_users_values_list[2]

    ## table name
    #### connections
    FB_CONNECTIONS = config.fb_connections_table_num
    ## table design
    ## 1 user_id -> uid again
    ## 2 display_name -> full name as given with the FB account
    ## 3 connection_type -> type of account: 0 = person, 2 = fan group
    ## 4 user_image_url 
    ## 5 user_image -> actual image as {blob} inserted
    FB_CONNECTIONS_USER_ID = config.fb_connection_list[0]
    FB_CONNECTIONS_DISPLAY_NAME = config.fb_connection_list[1]
    FB_CONNECTIONS_CONNECTION_TYPE = config.fb_connection_list[2]
    FB_CONNECTIONS_USER_IMAGE_URL = config.fb_connection_list[3]

    ## table name
    #### friends_data
    FB_FRIENDS_DATA = config.fb_friends_data_table_num
    ## table design
    ## 1 user_id -> uid once more
    ## 2 first_name
    ## 3 last_name
    ## 6 email
    ## 7 birthday_month
    ## 8 birthday_day
    ## 9 birthday_year
    FB_FRIENDS_DATA_USER_ID = config.fb_friends_data_list[0]
    FB_FRIENDS_DATA_FIRST_NAME = config.fb_friends_data_list[1]
    FB_FRIENDS_DATA_LAST_NAME = config.fb_friends_data_list[2]
    FB_FRIENDS_DATA_EMAIL = config.fb_friends_data_list[3]
    FB_FRIENDS_DATA_BDAY_MONTH = config.fb_friends_data_list[4]
    FB_FRIENDS_DATA_BDAY_DAY = config.fb_friends_data_list[5]
    FB_FRIENDS_DATA_BDAY_YEAR = config.fb_friends_data_list[6]

    if os.path.isfile(FB_DB_FILENAME):
        _adel_log.log("parseDBs:      ----> starting to parse \033[0;32m" + FB_DB_FILENAME.split("/")[-1] + "\033[m", 0)
        FB_TempList = _sqliteParser.parse_db(FB_DB_FILENAME)
        try:
            # print FB_TempList[FB_USER_VALUES_TABLE][2][2]
            FB_active_session_temp = string.replace(FB_TempList[FB_USER_VALUES_TABLE][2][2], '\"', '\'') #replace the " with ' to use it for dict structure
            FB_active_session = {}
            # print "ping"
            p = 0
            o = 0
            while o < len(FB_active_session_temp): # inside the value of the active session field is a dictionary structure which includes a second dict as value 
                o = o + 1                          # of the 'profile' key of the first structure. I therefore parse the structure as a string and rebuild the dict.
                if FB_active_session_temp[o] == ':':
                    key_start = p + 1
                    key_end = o
                    # print key_start,key_end
                    key = FB_active_session_temp[key_start:key_end]
                    # print key
                    for p in range (o, len(FB_active_session_temp)):
                        if FB_active_session_temp[p] == '{':
                            o = p
                            break
                        elif FB_active_session_temp[p] == '}':
                            value_start = o + 1
                            value_end = p
                            #print value_start,value_end
                            value = FB_active_session_temp[value_start:value_end]
                            #print value
                            FB_active_session [key] = value
                            o = len(FB_active_session_temp)
                            break
                        elif FB_active_session_temp[p] == ',':
                            value_start = o + 1
                            value_end = p
                            #print value_start,value_end
                            value = FB_active_session_temp[value_start:value_end]
                            #print value
                            FB_active_session [key] = value
                            o = p
                            #print o,p
                            break
        except:  
            print "Error: ", sys.exc_info()[0]         
            _adel_log.log("analyzeDBs:    ----> can't get the required active session data from " + FB_DB_FILENAME.split("/")[-1] + " ! DB structure changed?", 1)
        try:
            friends_list = []
            for i in range(1, len(FB_TempList[FB_FRIENDS_DATA])):
                friends_list.append([
                str(FB_TempList[FB_FRIENDS_DATA][i][FB_FRIENDS_DATA_USER_ID]),
                str(FB_TempList[FB_FRIENDS_DATA][i][FB_FRIENDS_DATA_FIRST_NAME]) + " " + str(FB_TempList[FB_FRIENDS_DATA][i][FB_FRIENDS_DATA_LAST_NAME]),
                str(FB_TempList[FB_FRIENDS_DATA][i][FB_FRIENDS_DATA_BDAY_DAY]) + "." + str(FB_TempList[FB_FRIENDS_DATA][i][FB_FRIENDS_DATA_BDAY_MONTH]) + "." + str(FB_TempList[FB_FRIENDS_DATA][i][FB_FRIENDS_DATA_BDAY_YEAR]),
                str(FB_TempList[FB_FRIENDS_DATA][i][FB_FRIENDS_DATA_EMAIL]) 
                                ])   
            #for j in range(0,len(userlist)):
            #    print userlist[j]
        except:
            _adel_log.log("analyzeDBs:   ----> can't get the required friends data from " + FB_DB_FILENAME.split("/")[-1] + " ! DB structure changed?", 1)
        try:
            conn_list = []
            for k in range(1, len(FB_TempList[FB_CONNECTIONS])):
                conn_list.append([
                str(FB_TempList[FB_CONNECTIONS][k][FB_CONNECTIONS_USER_ID]),
                str(FB_TempList[FB_CONNECTIONS][k][FB_CONNECTIONS_DISPLAY_NAME]),
                str(FB_TempList[FB_CONNECTIONS][k][FB_CONNECTIONS_USER_IMAGE_URL])
                                ])
            #for l in range(0,len(conn_list)):
            #    print conn_list[l]
        except:
            _adel_log.log("analyzeDBs:   ----> can't get the required connections data from " + FB_DB_FILENAME.split("/")[-1] + " ! DB structure changed?", 1)
        _xmlParser.facebook_to_xml(xml_dir, FB_active_session, friends_list, conn_list)

def analyze(backup_dir, os_version, xml_dir, twitter_dbname_list, config):
    _adel_log.log("############  DATABASE ANALYSIS ############ \n", 2)
    analyze_calendar(backup_dir, os_version, xml_dir, config)
    analyze_sms_mss(backup_dir, os_version, xml_dir, config)
    analyze_call_logs(backup_dir, os_version, xml_dir, config)
    analyze_contacts(backup_dir, os_version, xml_dir, config)
    analyze_facebook(backup_dir, os_version, xml_dir, config)
    analyze_twitter(backup_dir, os_version, xml_dir, twitter_dbname_list, config)