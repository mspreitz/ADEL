ADEL - Android Data Extractor Lite
==============

This Python script dumps all important SQLite Databases from a connected Android smartphone to the local
disk and analyzes these files in a forensically accurate workflow. If no smartphone is connected you can
specify a local directory which contains the databases you want to analyze. Afterwards this script creates
a clearly structured XML report.

If you connect a smartphone you need a rooted and insecure kernel/recovery installed on the smartphone.

Example for connected smartphone:
        adel.py -d device -l 4

Example for database backups:
        adel.py -d /home/user/backup -l 4
