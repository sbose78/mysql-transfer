from fabric.api import run,settings
from fabric.state import env
from fabric.tasks import execute
# self 147

def host_type():
    run('uname -s')

# H = 192.168.43.149

def take_cold_backup( mysql_conf_file='/etc/mysql/my.cnf',mysql_data_dir='/var/lib/mysql',destination_host='192.168.43.148',user='sbose'):


	# create backup directory
	run('mkdir -p /tmp/mysql-backup/conf ; mkdir -p /tmp/mysql-backup/data')
	run('cp -R %s /tmp/mysql-backup/conf/ ; sudo cp -R  %s /tmp/mysql-backup/data/'%( mysql_conf_file , mysql_data_dir ) )

	# tar it 
	run('sudo tar -zcvf /tmp/mysql-backup.tar.gz /tmp/mysql-backup')

	# send the zipped file over scp
	run('scp /tmp/mysql-backup.tar.gz %s@%s:/tmp/mysql-backup.tar.gz'%(user,destination_host))
	print "Moved backup to destination host %s"%( destination_host ) 


# H = 192.168.43.148

def restore_backup(backup_path='/tmp/mysql-backup.tar.gz',backup_dir='/tmp/mysql-backup/', mysql_conf_file='/etc/mysql/my.cnf',mysql_data_dir='/var/lib/mysql'):

	# unzip it under /tmp/
	run('mkdir -p /tmp/mysql-restore')
	run('sudo tar -xvf /tmp/mysql-backup.tar.gz -C /tmp/mysql-restore')

	# check if mysql is installed in remote server.
	
	# move conf file 
	run('sudo cp /tmp/mysql-restore/tmp/mysql-backup/conf/my.cnf /etc/mysql/my.cnf')
	run('sudo mkdir -p /var/lib/mysql ; sudo cp -R /tmp/mysql-restore/tmp/mysql-backup/data/mysql /var/lib/')

	#permissions
	run("sudo chown mysql:mysql -R /var/lib/mysql ")
	
		
	# move data dir
	print "End of backup"

def bind_to_host():
	print env.host
	# Comment out existing
	run("sudo sed -i -e 's/bind-address/#bind-address/g' /etc/mysql/my.cnf ")
	run("echo 'bind-address = %s' | sudo tee --append /etc/mysql/my.cnf"%(env.host))

def stop_mysql():
	with settings(warn_only=True):
		run("sudo service mysql stop")


def start_mysql():
	
	# start mysql
	run("sudo service mysql start")

def wrapper_run_all(source_database_host,destination_database_host,username):
	'''
		fab take_cold_backup -H $SOURCE_DB_HOST
		fab restore_backup -H $DESTINATION_DB_HOST
		fab bind_to_host -H $DESTINATION_DB_HOST
	'''
	execute( take_cold_backup , hosts = [ '%s@%s'%(username,source_database_host) ] )
	execute( restore_backup , hosts = [ '%s@%s'%(username,destination_database_host) ] )
	execute( bind_to_host , hosts = [ '%s@%s'%(username,destination_database_host) ] )
	execute( stop_mysql , hosts = [ '%s@%s'%(username,destination_database_host) ] )
	execute( start_mysql , hosts = [ '%s@%s'%(username,destination_database_host) ] )


