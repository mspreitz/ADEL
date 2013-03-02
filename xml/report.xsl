<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.w3.org/1999/xhtml" version="1.0">
<xsl:template match="/">
  <html>
  <body>
  <div align="center">
  <br />
  <br />
  <table width="700px" border="0">
  <tr>
    <td align="center"><img src="../../xml/logo.png" alt="ADEL_Logo" /></td>
  </tr>
</table>
<br />
<br />
<br />
<table width="1000px" border="1">
      <tr bgcolor="#B2B2B2">
        <th><a href="#info">Smartphone Info</a></th>
        <th><a href="#contacts">Contact Entries</a></th>
        <th><a href="#calendar">Calendar Entries</a></th>
        <th><a href="#calllog">Call-List Entries</a></th>
        <th><a href="#sms">SMS Messages</a></th>
        <th><a href="#twitter">Twitter Messages</a></th>
        <th><a href="../map.html">Movement Profile</a></th>
      </tr>
</table>
<br />
<br />
<br />
  <a name="info"><h2>Smartphone Info</h2></a>
    <table width="1000px" border="1">
      <tr bgcolor="#B2B2B2">
        <th>account name</th>
        <th>account type</th>
        <th>imsi</th>
        <th>imei</th>
        <th>handheld id</th>
        <th>model</th>
        <th>android version</th>
      </tr>
      <xsl:for-each select="report/smartphone_info">
      <tr>
        <td><xsl:value-of select="account_name"/></td>
        <td><xsl:value-of select="account_type"/></td>
        <td><xsl:value-of select="imsi"/></td>
        <td><xsl:value-of select="imei"/></td>
        <td><xsl:value-of select="handheld_id"/></td>
        <td><xsl:value-of select="model"/></td>
        <td>Android <xsl:value-of select="android_version"/></td>
      </tr>
      </xsl:for-each>
    </table>
    <br />
    <br />
  <a name="contacts"><h2>Contact Entries</h2></a>
    <table border="1">
      <tr bgcolor="#B2B2B2">
        <th>id</th>
        <th>photo id</th>
        <th>times contacted</th>
        <th>last time contacted</th>
        <th>starred</th>
        <th>telephone numbers</th>
        <th>display name</th>
        <th>lastname</th>
        <th>firstname</th>
        <th>company</th>
        <th>email</th>
        <th>URL</th>
        <th>address</th>
      </tr>
      <xsl:for-each select="report/contacts/contact">
      <tr>
        <td><xsl:value-of select="id"/></td>
        <td><xsl:value-of select="photo_id"/></td>
        <td><xsl:value-of select="times_contacted"/></td>
        <td><xsl:value-of select="last_time_contacted"/></td>
        <td><xsl:value-of select="starred"/></td>
        <td><xsl:value-of select="number"/></td>
        <td><xsl:value-of select="display_name"/></td>
       <td><xsl:value-of select="lastname"/></td>
       <td><xsl:value-of select="firstname"/></td>
       <td><xsl:value-of select="company"/></td>
       <td><xsl:value-of select="email"/></td>
       <td><xsl:value-of select="url"/></td>
       <td><xsl:value-of select="address"/></td>
      </tr>
      </xsl:for-each>
    </table>
    <br />
    <br />
  <a name="calendar"><h2>Calendar Entries</h2></a>
    <table border="1">
      <tr bgcolor="#B2B2B2">
        <th>id</th>
        <th>calendar name</th>
        <th>title</th>
        <th>event location</th>
        <th>all day</th>
        <th>start</th>
        <th>end</th>
        <th>has alarm</th>
      </tr>
      <xsl:for-each select="report/Calendar_Entries/Calendar_Entry">
      <tr>
        <td><xsl:value-of select="id"/></td>
        <td><xsl:value-of select="calendarName"/></td>
        <td><xsl:value-of select="title"/></td>
        <td><xsl:value-of select="eventLocation"/></td>
        <td><xsl:value-of select="allDay"/></td>
        <td><xsl:value-of select="start"/></td>
        <td><xsl:value-of select="end"/></td>
       <td><xsl:value-of select="hasAlarm"/></td>
      </tr>
      </xsl:for-each>
    </table>
    <br />
    <br />
  <a name="calllog"><h2>Call-Log Entries</h2></a>
    <table border="1">
      <tr bgcolor="#B2B2B2">
        <th>id</th>
        <th>number</th>
        <th>date</th>
        <th>duration</th>
        <th>type</th>
        <th>name</th>
      </tr>
      <xsl:for-each select="report/Call_Log_Entries/Call_Log_Entry">
      <tr>
        <td><xsl:value-of select="id"/></td>
        <td><xsl:value-of select="number"/></td>
        <td><xsl:value-of select="date"/></td>
        <td><xsl:value-of select="duration"/></td>
        <td><xsl:value-of select="type"/></td>
       <td><xsl:value-of select="name"/></td>
      </tr>
      </xsl:for-each>
    </table>
    <br />
    <br />
  <a name="sms"><h2>SMS/MMS Messages</h2></a>
    <table border="1">
      <tr bgcolor="#B2B2B2">
        <th>id</th>
        <th>thread id</th>
        <th>number</th>
        <th>person id</th>
        <th>date</th>
        <th>read</th>
        <th>type</th>
        <th>subject</th>
        <th>body</th>
      </tr>
      <xsl:for-each select="report/SMS_Messages/SMS_Message">
      <tr>
        <td><xsl:value-of select="id"/></td>
        <td><xsl:value-of select="thread_id"/></td>
        <td><xsl:value-of select="number"/></td>
        <td><xsl:value-of select="person"/></td>
        <td><xsl:value-of select="date"/></td>
       <td><xsl:value-of select="read"/></td>
       <td><xsl:value-of select="type"/></td>
       <td><xsl:value-of select="subject"/></td>
       <td><xsl:value-of select="body"/></td>
      </tr>
      </xsl:for-each>
    </table>
  <br />
    <br />
  <a name="twitter"><h2>Twitter Messages</h2></a>
    <table border="1">
      <tr bgcolor="#B2B2B2">
        <th>date</th>
        <th>message</th>
        <th>source</th>
      </tr>
      <xsl:for-each select="report/Twitter_Entries/Twitter_Account_Owner/Tweets/Tweet">
      <tr>
        <td><xsl:value-of select="Tweet_created"/></td>
        <td><xsl:value-of select="Message"/></td>
        <td><xsl:value-of select="Source"/></td>
      </tr>
      </xsl:for-each>
    </table>
    </div>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>