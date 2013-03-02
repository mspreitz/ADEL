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

from xml.dom.minidom import Document
import re

import _adel_log


# Make pretty XML without linebreaks in the elements
def make_pretty_xml(uglyXML):
    text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)    
    prettyXml = text_re.sub('>\g<1></', uglyXML)
    return prettyXml


# ContactsList = [[id, photo_id, times_contacted, last_time_contacted,
# starred, number, display_name, lastname, firstname, company, 
# email, url, address],[......],.....]
def contacts_to_xml(xml_dir, contactsList):
    _adel_log.log("############  XML OUTPUT GENERATION -> CONTACTS  ############ \n", 2)
    # Create the minidom document
    doc = Document()
    xml = doc.createElement("contacts")
    doc.appendChild(xml)
    for i in range(0, len(contactsList)):
        # Create the <contact> element
        contact = doc.createElement("contact")
        xml.appendChild(contact)
        id = doc.createElement("id")
        contact.appendChild(id)
        id_text = doc.createTextNode(contactsList[i][0])
        id.appendChild(id_text)
        photo_id = doc.createElement("photo_id")
        contact.appendChild(photo_id)
        photo_id_text = doc.createTextNode(contactsList[i][1])
        photo_id.appendChild(photo_id_text)
        times_contacted = doc.createElement("times_contacted")
        contact.appendChild(times_contacted)
        times_contacted_text = doc.createTextNode(contactsList[i][2])
        times_contacted.appendChild(times_contacted_text)
        last_time_contacted = doc.createElement("last_time_contacted")
        contact.appendChild(last_time_contacted)
        last_time_contacted_text = doc.createTextNode(contactsList[i][3])
        last_time_contacted.appendChild(last_time_contacted_text)
        starred = doc.createElement("starred")
        contact.appendChild(starred)
        starred_text = doc.createTextNode(contactsList[i][4])
        starred.appendChild(starred_text)
        number = doc.createElement("number")
        contact.appendChild(number)
        number_text = doc.createTextNode(contactsList[i][5])
        number.appendChild(number_text)
        display_name = doc.createElement("display_name")
        contact.appendChild(display_name)
        display_name_text = doc.createTextNode(contactsList[i][6])
        display_name.appendChild(display_name_text)
        lastname = doc.createElement("lastname")
        contact.appendChild(lastname)
        lastname_text = doc.createTextNode(contactsList[i][7])
        lastname.appendChild(lastname_text)
        firstname = doc.createElement("firstname")
        contact.appendChild(firstname)
        firstname_text = doc.createTextNode(contactsList[i][8])
        firstname.appendChild(firstname_text)
        company = doc.createElement("company")
        contact.appendChild(company)
        company_text = doc.createTextNode(contactsList[i][9])
        company.appendChild(company_text)
        email = doc.createElement("email")
        contact.appendChild(email)
        email_text = doc.createTextNode(contactsList[i][10])
        email.appendChild(email_text)
        url = doc.createElement("url")
        contact.appendChild(url)
        url_text = doc.createTextNode(contactsList[i][11])
        url.appendChild(url_text)
        address = doc.createElement("address")
        contact.appendChild(address)
        address_text = doc.createTextNode(contactsList[i][12])
        address.appendChild(address_text)
    # Print our newly created XML files to Log
    _adel_log.log(make_pretty_xml(doc.toprettyxml(indent="  ", encoding="UTF-8")), 3)
    # create xml file
    xml_contacts = open(xml_dir + "/contacts.xml", "a+")
    xml_contacts.write(make_pretty_xml(doc.toprettyxml(indent="  ", encoding="UTF-8")))
    xml_contacts.close()
    _adel_log.log("xmlParser:          ----> contacts.xml created!", 4)
    

# SmsList = [[id, thread_id, number, person, date, read, type,
# subject, body],[......],......]
def sms_messages_to_xml(xml_dir, sms_list):
    _adel_log.log("############  XML OUTPUT GENERATION -> SMS MESSAGES  ############ \n", 2)
    # Create the minidom document
    doc = Document()
    xml = doc.createElement("SMS_Messages")
    doc.appendChild(xml)
    for i in range(0, len(sms_list)):
        # Create the <SMS_Message> element
        sms_message = doc.createElement("SMS_Message")
        xml.appendChild(sms_message)
        id = doc.createElement("id")
        sms_message.appendChild(id)
        id_text = doc.createTextNode(sms_list[i][0])
        id.appendChild(id_text)
        thread_id = doc.createElement("thread_id")
        sms_message.appendChild(thread_id)
        thread_id_text = doc.createTextNode(sms_list[i][1])
        thread_id.appendChild(thread_id_text)
        number = doc.createElement("number")
        sms_message.appendChild(number)
        number_text = doc.createTextNode(sms_list[i][2])
        number.appendChild(number_text)
        person = doc.createElement("person")
        sms_message.appendChild(person)
        person_text = doc.createTextNode(sms_list[i][3])
        person.appendChild(person_text)
        date = doc.createElement("date")
        sms_message.appendChild(date)
        date_text = doc.createTextNode(sms_list[i][4])
        date.appendChild(date_text)
        read = doc.createElement("read")
        sms_message.appendChild(read)
        read_text = doc.createTextNode(sms_list[i][5])
        read.appendChild(read_text)
        type = doc.createElement("type")
        sms_message.appendChild(type)
        type_text = doc.createTextNode(sms_list[i][6])
        type.appendChild(type_text)
        subject = doc.createElement("subject")
        sms_message.appendChild(subject)
        subject_text = doc.createTextNode(sms_list[i][7])
        subject.appendChild(subject_text)
        body = doc.createElement("body")
        sms_message.appendChild(body)
        body_text = doc.createTextNode(sms_list[i][8])
        body.appendChild(body_text)
    # Print our newly created XML files to Log
    _adel_log.log(make_pretty_xml(doc.toprettyxml(indent="  ", encoding="UTF-8")), 3)
    # create xml file
    xml_sms_messages = open(xml_dir + "/sms_Messages.xml", "a+")
    xml_sms_messages.write(make_pretty_xml(doc.toprettyxml(indent="  ", encoding="UTF-8")))
    xml_sms_messages.close()
    _adel_log.log("xmlParser:          ----> sms_Messages.xml created!", 4)
    

# smartphone_infolist = [account_name, account_type, imsi, android_id, 
# handheld_id, android_version]
def smartphone_info_to_xml(xml_dir, smartphone_infolist):
    _adel_log.log("############  XML OUTPUT GENERATION -> SMARTPHONE INFOS  ############ \n", 2)
    # Create the minidom document
    doc = Document()
    info = doc.createElement("smartphone_info")
    doc.appendChild(info)
    account_name = doc.createElement("account_name")
    info.appendChild(account_name)
    account_name_text = doc.createTextNode(smartphone_infolist[0])
    account_name.appendChild(account_name_text)
    account_type = doc.createElement("account_type")
    info.appendChild(account_type)
    account_type_text = doc.createTextNode(smartphone_infolist[1])
    account_type.appendChild(account_type_text)
    imsi = doc.createElement("imsi")
    info.appendChild(imsi)
    imsi_text = doc.createTextNode(smartphone_infolist[2])
    imsi.appendChild(imsi_text)
    android_id = doc.createElement("android_id")
    info.appendChild(android_id)
    android_id_text = doc.createTextNode(smartphone_infolist[3])
    android_id.appendChild(android_id_text)
    handheld_id = doc.createElement("handheld_id")
    info.appendChild(handheld_id)
    handheld_id_text = doc.createTextNode(smartphone_infolist[4])
    handheld_id.appendChild(handheld_id_text)
    model = doc.createElement("model")
    info.appendChild(model)
    model_text = doc.createTextNode(smartphone_infolist[5])
    model.appendChild(model_text)
    android_version = doc.createElement("android_version")
    info.appendChild(android_version)
    android_version_text = doc.createTextNode(smartphone_infolist[6])
    android_version.appendChild(android_version_text)
    # Print our newly created XML files to Log
    _adel_log.log(make_pretty_xml(doc.toprettyxml(indent="  ", encoding="UTF-8")), 3)
    # create xml file
    xml_info = open(xml_dir + "/info.xml", "a+")
    xml_info.write(make_pretty_xml(doc.toprettyxml(indent="  ", encoding="UTF-8")))
    xml_info.close()
    _adel_log.log("xmlParser:          ----> info.xml created!", 4)
    

# calendarList = [[id, calendarName, title, eventLocation, description, 
# allDay, start, end, hasAlarm, alarmTime, notifyTime],[......],......]
def calendar_to_xml(xml_dir, calendar_list):
    _adel_log.log("############  XML OUTPUT GENERATION -> CALENDAR ENTRIES  ############ \n", 2)
    # Create the minidom document
    doc = Document()
    xml = doc.createElement("Calendar_Entries")
    doc.appendChild(xml)
    for i in range(0, len(calendar_list)):
        # Create the <Calendar_Entry> element
        calendar_entry = doc.createElement("Calendar_Entry")
        xml.appendChild(calendar_entry)
        id = doc.createElement("id")
        calendar_entry.appendChild(id)
        id_text = doc.createTextNode(calendar_list[i][0])
        id.appendChild(id_text)
        calendarName = doc.createElement("calendarName")
        calendar_entry.appendChild(calendarName)
        calendarName_text = doc.createTextNode(calendar_list[i][1])
        calendarName.appendChild(calendarName_text)
        title = doc.createElement("title")
        calendar_entry.appendChild(title)
        title_text = doc.createTextNode(calendar_list[i][2])
        title.appendChild(title_text)
        eventLocation = doc.createElement("eventLocation")
        calendar_entry.appendChild(eventLocation)
        event_location_text = doc.createTextNode(calendar_list[i][3])
        eventLocation.appendChild(event_location_text)
        description = doc.createElement("description")
        calendar_entry.appendChild(description)
        description_text = doc.createTextNode(calendar_list[i][4])
        description.appendChild(description_text)
        all_day = doc.createElement("all_day")
        calendar_entry.appendChild(all_day)
        allDay_text = doc.createTextNode(calendar_list[i][5])
        all_day.appendChild(allDay_text)
        start = doc.createElement("start")
        calendar_entry.appendChild(start)
        start_text = doc.createTextNode(calendar_list[i][6])
        start.appendChild(start_text)
        end = doc.createElement("end")
        calendar_entry.appendChild(end)
        end_text = doc.createTextNode(calendar_list[i][7])
        end.appendChild(end_text)
        has_alarm = doc.createElement("has_alarm")
        calendar_entry.appendChild(has_alarm)
        has_alarm_text = doc.createTextNode(calendar_list[i][8])
        has_alarm.appendChild(has_alarm_text)
    # Print our newly created XML files to Log
    _adel_log.log(make_pretty_xml(doc.toprettyxml(indent="  ", encoding="UTF-8")), 3)
    # create xml file
    xml_calendar = open(xml_dir + "/calendar.xml", "a+")
    xml_calendar.write(make_pretty_xml(doc.toprettyxml(indent="  ", encoding="UTF-8")))
    xml_calendar.close()
    _adel_log.log("xmlParser:          ----> calendar.xml created!", 4)
    

# callLogList = [[id, number, date, duration, name, type],[......],......]
def call_log_to_xml(xml_dir, callLogList):
    _adel_log.log("############  XML OUTPUT GENERATION -> CALL LOG ENTRIES  ############ \n", 2)
    # Create the minidom document
    doc = Document()
    xml = doc.createElement("Call_Log_Entries")
    doc.appendChild(xml)
    for i in range(0, len(callLogList)):
        # Create the <Call_Log_Entry> element
        call_log_entry = doc.createElement("Call_Log_Entry")
        xml.appendChild(call_log_entry)
        id = doc.createElement("id")
        call_log_entry.appendChild(id)
        id_text = doc.createTextNode(callLogList[i][0])
        id.appendChild(id_text)
        number = doc.createElement("number")
        call_log_entry.appendChild(number)
        number_text = doc.createTextNode(callLogList[i][1])
        number.appendChild(number_text)
        date = doc.createElement("date")
        call_log_entry.appendChild(date)
        date_text = doc.createTextNode(callLogList[i][2])
        date.appendChild(date_text)
        duration = doc.createElement("duration")
        call_log_entry.appendChild(duration)
        duration_text = doc.createTextNode(callLogList[i][3])
        duration.appendChild(duration_text)
        type = doc.createElement("type")
        call_log_entry.appendChild(type)
        type_text = doc.createTextNode(callLogList[i][4])
        type.appendChild(type_text)
        name = doc.createElement("name")
        call_log_entry.appendChild(name)
        name_text = doc.createTextNode(callLogList[i][5])
        name.appendChild(name_text)
    # Print our newly created XML files to Log
    _adel_log.log(make_pretty_xml(doc.toprettyxml(indent="  ", encoding="UTF-8")), 3)
    # create xml file
    xml_callLogs = open(xml_dir + "/call_logs.xml", "a+")
    xml_callLogs.write(make_pretty_xml(doc.toprettyxml(indent="  ", encoding="UTF-8")))
    xml_callLogs.close()
    _adel_log.log("xmlParser:          ----> call_logs.xml created!", 4)


def facebook_to_xml (xml_dir, UserDict, FriendsList, ConnList):
    _adel_log.log("############  XML OUTPUT GENERATION -> FACEBOOK ENTRIES  ############ \n", 2)
    # Create the minidom document
    doc = Document()
    fb_entries = doc.createElement("Facebook_Entries")
    doc.appendChild(fb_entries)
    
    # UserDict is a dictionary structure containing the FB_user informations. Following keys are available: 
    # uid -> Facebook User ID
    # secret      \
    # access token \
    # session_key --> these three seem to be hash values for cryptographic purpose
    # first_name
    # last_name -> as given in the account
    # name -> screen name for friendslists (?)
    # username -> loginname for FB account
    # machine_id -> another hash to pinpoint used device (?)
    # pic_square -> Link to account picture
    # Entry generated for FriendsList is User_ID, Last_Name, First_Name, 
    # Birthday, E-mail (if given)
    
    USER_ID = 0
    NAME = 1
    BIRTHDAY = 2
    E_MAIL = 3
    for i in range (0, len(FriendsList)):
        user_entry_node = doc.createElement("Friends_Entry")
        fb_entries.appendChild(user_entry_node)
        user_id_node = doc.createElement("Facebook_User_id")
        user_entry_node.appendChild(user_id_node)
        user_id_note_text = doc.createTextNode(FriendsList[i][USER_ID])
        user_id_node.appendChild(user_id_note_text)
        user_name_node = doc.createElement("Friends_Name")
        user_entry_node.appendChild(user_name_node)
        user_name_node_text = doc.createTextNode(FriendsList[i][NAME])
        user_name_node.appendChild(user_name_node_text)
        birthday_note = doc.createElement("Birthday")
        user_entry_node.appendChild(birthday_note)
        birthday_note_text = doc.createTextNode(FriendsList[i][BIRTHDAY])
        birthday_note.appendChild(birthday_note_text)
        email_node = doc.createElement("E-Mail_Adress")
        user_entry_node.appendChild(email_node)
        email_node_text = doc.createTextNode(FriendsList[i][E_MAIL])
        email_node.appendChild(email_node_text)
        """
        user_id = int(TwitterList[i][USER_ID])
        #print user_id             
        if user_id in TweetList:
            tweets = TweetList[user_id]
            tweetsNode = doc.createElement("Tweets")
            user_entry_node.appendChild(tweetsNode)
            for j in range (0,len(tweets)):
                tweetNode = doc.createElement("Tweet")
                tweetsNode.appendChild(tweetNode)
                dateNode = doc.createElement("Tweet_created")
                tweetNode.appendChild(dateNode)
                dateNode_text = doc.createTextNode(tweets[j][3])
                dateNode.appendChild(dateNode_text)
                messageNode = doc.createElement("Message")
                tweetNode.appendChild(messageNode)
                messageNode_text = doc.createTextNode(str(tweets[j][0]))
                messageNode.appendChild(messageNode_text)
                sourceNode = doc.createElement("Source")
                tweetNode.appendChild(sourceNode)
                sourceNode_text = doc.createTextNode(tweets[j][1])
                sourceNode.appendChild(sourceNode_text)
                sourceUrlNode = doc.createElement("Source_Url")
                tweetNode.appendChild(sourceUrlNode)
                sourceUrlNode_text = doc.createTextNode(tweets[j][2])
                sourceUrlNode.appendChild(sourceUrlNode_text) 
        """  
    # Print our newly created XML files to Log
    _adel_log.log(make_pretty_xml(doc.toprettyxml(indent="  ", encoding="UTF-8")), 3)
    # Create xml file
    xml_fb = open(xml_dir + "/facebook.xml", "a+")
    xml_fb.write(make_pretty_xml(doc.toprettyxml(indent="  ", encoding="UTF-8")))
    xml_fb.close()
    _adel_log.log("xmlParser:          ----> facebook.xml created!", 4) 
  
  
def twitter_to_xml (xml_dir, twitter_list, tweet_list):
    _adel_log.log("############  XML OUTPUT GENERATION -> TWITTER ENTRIES  ############ \n", 2)
    # Create the minidom document
    doc = Document()
    twitter_entries = doc.createElement("Twitter_Entries")
    doc.appendChild(twitter_entries)
    ## Entry generated is User_ID, User_Name, Real_Name, description, location (if given), profile_created, updated, followers, friends
    USER_ID = 0
    USER_NAME = 1
    REAL_NAME = 2
    DESCRIPTION = 3
    LOCATION = 4
    PROFILE_CREATED = 5
    UPDATED = 6
    FOLLOWERS = 7
    FRIENDS = 8
            
    for i in range (0,len(twitter_list)):
        if i == 0:
            user_entry_node = doc.createElement("Twitter_Account_Owner")
        else:    
            user_entry_node = doc.createElement("User_Entry")
        twitter_entries.appendChild(user_entry_node)
        user_id_node = doc.createElement("User_id")
        user_entry_node.appendChild(user_id_node)
        user_id_node_text = doc.createTextNode(twitter_list[i][USER_ID])
        user_id_node.appendChild(user_id_node_text)
        user_name_node = doc.createElement("User_Name")
        user_entry_node.appendChild(user_name_node)
        user_name_node_text = doc.createTextNode(twitter_list[i][USER_NAME])
        user_name_node.appendChild(user_name_node_text)
        real_name_node = doc.createElement("Real_Name")
        user_entry_node.appendChild(real_name_node)
        real_name_node_text = doc.createTextNode(twitter_list[i][REAL_NAME])
        real_name_node.appendChild(real_name_node_text)
        description_node = doc.createElement("Description")
        user_entry_node.appendChild(description_node)
        description_node_text = doc.createTextNode(twitter_list[i][DESCRIPTION])
        description_node.appendChild(description_node_text)
        location_node = doc.createElement("Location")
        user_entry_node.appendChild(location_node)
        location_node_text = doc.createTextNode(twitter_list[i][LOCATION])
        location_node.appendChild(location_node_text)
        profile_created_node = doc.createElement("Profile_created")
        user_entry_node.appendChild(profile_created_node)
        profile_created_node_text = doc.createTextNode(twitter_list[i][PROFILE_CREATED])
        profile_created_node.appendChild(profile_created_node_text)
        updated_node = doc.createElement("Updated")
        user_entry_node.appendChild(updated_node)
        updated_note_text = doc.createTextNode(twitter_list[i][UPDATED])
        updated_node.appendChild(updated_note_text)
        followers_node = doc.createElement("Followers")
        user_entry_node.appendChild(followers_node)
        followers_node_text = doc.createTextNode(twitter_list[i][FOLLOWERS])
        followers_node.appendChild(followers_node_text)
        friends_node = doc.createElement("Friends")
        user_entry_node.appendChild(friends_node)
        friends_node_text = doc.createTextNode(twitter_list[i][FRIENDS])
        friends_node.appendChild(friends_node_text)
        user_id = int(twitter_list[i][USER_ID])
        #print user_id             
        if user_id in tweet_list:
            tweets = tweet_list[user_id]
            tweets_node = doc.createElement("Tweets")
            user_entry_node.appendChild(tweets_node)
            for j in range (0,len(tweets)):
                tweet_node = doc.createElement("Tweet")
                tweets_node.appendChild(tweet_node)
                data_node = doc.createElement("Tweet_created")
                tweet_node.appendChild(data_node)
                data_node_text = doc.createTextNode(tweets[j][3])
                data_node.appendChild(data_node_text)
                message_node = doc.createElement("Message")
                tweet_node.appendChild(message_node)
                message_node_text = doc.createTextNode(tweets[j][0])
                message_node.appendChild(message_node_text)
                source_node = doc.createElement("Source")
                tweet_node.appendChild(source_node)
                source_node_text = doc.createTextNode(tweets[j][1])
                source_node.appendChild(source_node_text)
                source_url_node = doc.createElement("Source_Url")
                tweet_node.appendChild(source_url_node)
                source_url_node_text = doc.createTextNode(tweets[j][2])
                source_url_node.appendChild(source_url_node_text)
    # Print our newly created XML files to Log
    _adel_log.log(make_pretty_xml(doc.toprettyxml(indent="  ", encoding="UTF-8")), 3)
    # Create xml file
    twitter_xml_name = "twitter_" + twitter_list[0][USER_ID] + ".xml"
    xml_twitter = open(xml_dir + "/" + twitter_xml_name, "a+")
    xml_twitter.write(make_pretty_xml(doc.toprettyxml(indent="  ", encoding="UTF-8")))
    xml_twitter.close()
    _adel_log.log("xmlParser:          ----> " + twitter_xml_name + " created!", 4) 