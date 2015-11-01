#!/usr/bin/python


from fabfile import wrapper_run_all
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s", "--source", dest="source_database_host",
                  help="The IP or Hostname of the database server from where database would be copied.")
parser.add_option("-d", "--destination",dest="destination_database_host",
                  help="The destination host where database is being copied to.")
parser.add_option("-u", "--username",dest="username",
                  help="The UNIX user which will be executing.")

parser.add_option("-p", "--password",dest="password",
                  help="The MySQL root password.")









(options, args) = parser.parse_args()

def copy_database(source,destination,username,password):
	wrapper_run_all( source, destination , username ,password)

def main():
	global options
	mandatory = [ options.source_database_host , options.destination_database_host , options.username ,options.password ]
	for i in mandatory :
		if i == None:
			print "Mandatory arguments missing "
			return 

	copy_database( options.source_database_host , options.destination_database_host , options.username , options.password )

main()	
