#!/usr/bin/python2.7

import os
import sys
import argparse
import subprocess

CACHE_PARTITION = "/dev/block/mmcblk0p7"
DATA_PARTITION = "/dev/block/mmcblk0p10"
EMMC_PARTITION = "/dev/block/mmcblk0p11"
SYSTEM_PARTITION = "/dev/block/mmcblk0p9"
SDCARD_PARTITION = "/dev/block/mmcblk0p1"

def determine_dst_path(src, dst):
	return dst + "/" + src.rsplit('/')[-1]

def get_adb_checksum(path):
	return subprocess.check_output(["adb", "shell", "sha256sum", path]).rsplit(' ')[0]

def get_checksum(path):
	return subprocess.check_output(["sha256sum", path]).rsplit(' ')[0]

def dump_partition(src, dst):
	subprocess.call(["adb", "pull", str(src), str(determine_dst_path(src, dst))])

def comp_checksums(c1, c2):
	if c1 == c2:
		return "OK"
	else:
		return "FAILED"

def dump_partitions(debug, path):
	if debug is True:
		print "Building checksums before dumping ..."
		print "WARNING: This may take a while."
		print ""
		sys.stdout.write('/cache\t' +  CACHE_PARTITION + '\t')
		sys.stdout.flush()
		cache_c0 = get_adb_checksum(CACHE_PARTITION)
		sys.stdout.write(cache_c0 + '\n')

		sys.stdout.write('/data\t' +  DATA_PARTITION + '\t')
		sys.stdout.flush()
		data_c0 = get_adb_checksum(DATA_PARTITION)
		sys.stdout.write(data_c0 + '\n')

		sys.stdout.write('/emmc\t' +  EMMC_PARTITION + '\t')
		sys.stdout.flush()
		emmc_c0 = get_adb_checksum(EMMC_PARTITION)
		sys.stdout.write(emmc_c0 + '\n')

		sys.stdout.write('/system\t' +  SYSTEM_PARTITION + '\t')
		sys.stdout.flush()
		system_c0 = get_adb_checksum(SYSTEM_PARTITION)
		sys.stdout.write(system_c0 + '\n')

		sys.stdout.write('/sdcard\t' +  SDCARD_PARTITION + '\t')
		sys.stdout.flush()
		sdcard_c0 = get_adb_checksum(SDCARD_PARTITION)
		sys.stdout.write(sdcard_c0 + '\n')
	
	print ""
	print ""
	print "Starting to dump partitions ..."
	print ""

	sys.stdout.write('/cache\t' +  CACHE_PARTITION + '\t')
	sys.stdout.flush()
	dump_partition(CACHE_PARTITION, path)
	sys.stdout.write('DONE\n')

	sys.stdout.write('/data\t' +  DATA_PARTITION + '\t')
	sys.stdout.flush()
	dump_partition(DATA_PARTITION, path)
	sys.stdout.write('DONE\n')

	sys.stdout.write('/emmc\t' +  EMMC_PARTITION + '\t')
	sys.stdout.flush()
	dump_partition(EMMC_PARTITION, path)
	sys.stdout.write('DONE\n')

	sys.stdout.write('/system\t' +  SYSTEM_PARTITION + '\t')
	sys.stdout.flush()
	dump_partition(SYSTEM_PARTITION, path)
	sys.stdout.write('DONE\n')

	sys.stdout.write('/sdcard\t' +  SDCARD_PARTITION + '\t')
	sys.stdout.flush()
	dump_partition(SDCARD_PARTITION, path)
	sys.stdout.write('DONE\n')

	if debug is True:
		print ""
		print ""
		print "Checking integrity of dumps ..."
		print ""
		sys.stdout.write('/cache\t' +  CACHE_PARTITION + '\t')
		sys.stdout.flush()
		cache_c1 = get_checksum(determine_dst_path(CACHE_PARTITION, path))
		sys.stdout.write(cache_c1 + '\t' + comp_checksums(cache_c0, cache_c1) + '\n')
		
		sys.stdout.write('/data\t' +  DATA_PARTITION + '\t')
		sys.stdout.flush()
		data_c1 = get_checksum(determine_dst_path(DATA_PARTITION, path))
		sys.stdout.write(data_c1 + '\t' + comp_checksums(data_c0, data_c1) + '\n')

		sys.stdout.write('/emmc\t' +  EMMC_PARTITION + '\t')
		sys.stdout.flush()
		emmc_c1 = get_checksum(determine_dst_path(EMMC_PARTITION, path))
		sys.stdout.write(emmc_c1 + '\t' + comp_checksums(emmc_c0, emmc_c1) + '\n')

		sys.stdout.write('/system\t' +  SYSTEM_PARTITION + '\t')
		sys.stdout.flush()
		system_c1 = get_checksum(determine_dst_path(SYSTEM_PARTITION, path))
		sys.stdout.write(system_c1 + '\t' + comp_checksums(system_c0, system_c1) + '\n')

		sys.stdout.write('/sdcard\t' +  SDCARD_PARTITION + '\t')
		sys.stdout.flush()
		sdcard_c1 = get_checksum(determine_dst_path(SDCARD_PARTITION, path))
		sys.stdout.write(sdcard_c1 + '\t' + comp_checksums(sdcard_c0, sdcard_c1) + '\n')

	print ""
	print ""
	print "Partitions dumped."

def main(debug, path):

	os.system("clear")
	print """\033[0;32m
	          _____  ________  ___________.____
	         /  _  \ \______ \ \_   _____/|    |
	        /  /_\  \ |    |  \ |    __)_ |    |
	       /    |    \|    `   \|        \|    |___
	       \____|__  /_______  /_______  /|_______ \  
	               \/        \/        \/         \/
	     Android Data Extractor Lite - Partition Dumper


	\033[m"""
	dump_partitions(debug, path)
		

if __name__ == "__main__":
	usage = "adel_dump_partitions.py [-i] [-o directory]"
	parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('-i', '--integrity', action='store_true', help="When set integrity checks are made")
	parser.add_argument('-o', '--output', default=".", nargs=1, help="Directory, where to save the dumps")
	options = parser.parse_args(sys.argv[1:])

	main(options.integrity, options.output[0])
