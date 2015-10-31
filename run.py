#!/usr/bin/python


from fabfile import wrapper_run_all
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--source", dest="source_database_host",
                  help="The IP or Hostname of the database server from where database would be copied.")
parser.add_option("-d", "--destination",dest="destination_database_host",
                  help="The destination host where database is being copied to.")
parser.add_option("-u", "--username",dest="username",
                  help="The user which will be executing.")



(options, args) = parser.parse_args()

def copy_database(source,destination,username):
	wrapper_run_all( source, destination , username )

def main():
	global options
	copy_database( options.source_database_host , options.destination_database_host , options.username )

main()	
