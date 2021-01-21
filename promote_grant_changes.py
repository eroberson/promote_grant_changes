#!/usr/bin/env python

###########
# imports #
###########
import argparse
import glob
import hashlib
import datetime
import logging
import os
import shutil
import sys

####################
# Version and name #
####################
__script_path__ = sys.argv[0]
__script_name__ = __script_path__.split('/')[-1].split('\\')[-1]
__version__ = '0.0.1'

def GetDigest( fname, byteLimit = 2 ** 11 ):
	hasher = hashlib.md5()
	
	with open( fname, 'rb' ) as infile:
		buf = infile.read( byteLimit )
		while( len( buf ) > 0 ):
			hasher.update( buf )
			buf = infile.read( byteLimit )
	return str( hasher.hexdigest() )
	
def MakeDirIfNotExists( dir_path ):
	if not os.path.isdir( dir_path ):
		os.makedirs( dir_path )
		
def run():
	#############
	# arg parse #
	#############
	parser = argparse.ArgumentParser( prog=__script_name__, epilog="%s v%s" % ( __script_name__, __version__ ) )
	
	parser.add_argument( "target_directory", help="Directory where files will be moved to for organization" )
	parser.add_argument( "--readbuffer", help="What is maximum size (bytes) to slurp into memory at once?", type=int, default = 2 ** 11 ) 
	parser.add_argument( "--dryrun", help="Go through the motions, but don't move anything", default=False, action='store_true' )
	
	parser.add_argument( "--loglevel", choices=[ 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' ], default='INFO' )

	input_args = parser.parse_args()
	
	assert input_args.readbuffer > 0
	
	#################
	# setup logging #
	#################
	logging.basicConfig( format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )
	logger = logging.getLogger( __script_name__ )
	logger.setLevel( input_args.loglevel )
	
	#####################
	# Give us some info #
	#####################
	opt_string = "Run info"
	opt_string += "%s v%s\n" %( __script_name__, __version__ )
	opt_string += "Target: %s\n" % ( input_args.target_directory )
	opt_string += "Read buffer for hashing: %s\n" % ( input_args.readbuffer )
	opt_string += "Dryrun? %s" % ( input_args.dryrun )
	
	logger.info( opt_string )
	
	############
	# clean up #
	############
	target_directory = os.path.normpath( input_args.target_directory )
	hash_filename = os.path.join( target_directory, "files.hash" )
	
	##############
	# no clobber #
	##############
	assert "." != target_directory
	
	#############################
	# make target if not exists #
	#############################
	MakeDirIfNotExists( target_directory )
	
	###################
	# load RMS number #
	###################
	rms_num = ""
	
	with open( "rms_doc_num.txt", 'r' ) as RMS:
		rms_num = RMS.readline()
		rms_num = rms_num.rstrip()
		
	#################
	# Set time code #
	#################
	time_string = datetime.datetime.strftime( datetime.datetime.now(), "%Y-%m-%d-%H%M" )
	
	################
	# Track hashes #
	################	
	hash_dict = {}
	
	if os.path.isfile( hash_filename ):
		with open( hash_filename, 'r' ) as HASH_IN:
			for line in HASH_IN:
				line = line.rstrip()
				fname, hashval = line.split( '\t' )
				hash_dict[ fname ] = hashval
				
	#######################
	# Get every grant doc #
	#######################
	for curr_file in glob.iglob( "../%s_*" % ( rms_num ) ):
		curr_file = str( curr_file )
		curr_file_hash = GetDigest( curr_file )
		
		prev_file_hash = hash_dict.get( curr_file, None )
		
		logger.debug( "current: %s" % ( curr_file_hash ) )
		logger.debug( "prev: %s" % ( prev_file_hash ) )
		
		if curr_file_hash == hash_dict.get( curr_file, None ):
			logger.info( "%s is up-to-date, skipping." % ( curr_file ) )
			continue
		
		hash_dict[ curr_file ] = curr_file_hash
		
		# new filename
		base = os.path.basename( curr_file )
		filebase, ext = os.path.splitext( base )
		
		outfile = os.path.join( target_directory, "%s_%s%s" % ( filebase, time_string, ext ) )
		
		# copy with shutil
		if input_args.dryrun:
			logger.info( "%s is out-of-date - no action (dryrun)" % ( curr_file ) )
		else:
			logger.info( "%s is out-of-date, copying to %s" % ( curr_file, outfile ) )
			shutil.copy( curr_file, outfile )
				
	#####################
	# write hash values #
	#####################	
	if not input_args.dryrun:
		with open( hash_filename, 'w' ) as HASH_OUT:
			for key, value in hash_dict.items():
				HASH_OUT.write( "{}\t{}\n".format( key, value ) )
	
if __name__ == "__main__":
	run()
