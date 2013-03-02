ADEL - Android Data Extractor Lite
==============

This Python script dumps all important SQLite Databases from a connected Android smartphone to the local disk and analyzes these files in a forensically accurate workflow. If no smartphone is connected you can specify a local directory which contains the databases you want to analyze. Afterwards this script creates a clearly structured XML report.

If you connect a smartphone you need a rooted and insecure kernel or a custom recovery installed on the smartphone.

ADEL needs a predefined configuration for each device to work proper. This configuration has to be added in the following file:

    xml/phone_configs.xml

As an example we added the configuration for the Samsung Galaxy S2 running Android 2.3.3, more phone configurations will follow.



Example for the use of ADEL with a connected smartphone:

	adel.py -d device -l 4

Example for the use of ADEL with database backups:

	adel.py -d /home/user/backup -l 4