from fabric.api import run

# self 147

def host_type():
    run('uname -s')

# H = 192.168.43.149

def take_cold_backup( mysql_conf_file='/etc/mysql/my.cnf',mysql_data_dir='/var/lib/mysql',destination_host='192.168.43.148'):


	# create backup directory
	run('sudo mkdir -p /tmp/mysql-backup/conf ; sudo mkdir -p /tmp/mysql-backup/data')
	run('sudo cp -R /etc/mysql/my.cnf /tmp/mysql-backup/conf/ ; sudo cp -R /var/lib/mysql/ /tmp/mysql-backup/data/' )

	# tar it 
	run('sudo tar -zcvf /tmp/mysql-backup.tar.gz /tmp/mysql-backup')

	# send the zipped file over scp
	run('sudo scp /tmp/mysql-backup.tar.gz sbose@%s:/tmp/mysql-backup.tar.gz'%(destination_host))
	print "Moved backup to destination host %s"%( destination_host ) 


# H = 192.168.43.148

def restore_backup(backup_path='/tmp/mysql-backup.tar.gz',backup_dir='/tmp/mysql-backup/'):

	# unzip it under /tmp/
	run('sudo mkdir -p /tmp/mysql-restore')
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
	print "not implemented"

def stop_mysql():
	with settings(warn_only=True):
		run("sudo service mysql stop")


def start_mysql():
	
	# start mysql
	run("sudo service mysql start")

