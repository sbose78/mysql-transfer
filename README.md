**Sample usage**

```
./run.py -s 192.168.43.149 -d 192.168.43.148 -u sbose -p my_mysql_root_password
```

**Prequisites and manual steps**

- MySQL server is installed in both 'source' host and 'destination' hosts.
- SSH authorized keys are setup to avoid login prompt. Ideally this would be done using Puppet/Chef. The handy script to do manually now would be to execute ``` sh utils/copy-all-key.sh ``` on all servers.
- To avoid password prompt during *sudo* directed commands, add a sudoers file exception as shown in ``` sh utils/remove-sudo-password-prompt.sh ```

**Dependencies**
``` 
$ sh utils/install-dependencies.sh

```


**Usage**
```

Usage: run.py [options]

Options:
  -h, --help            show this help message and exit
  -s SOURCE_DATABASE_HOST, --source=SOURCE_DATABASE_HOST
                        The IP or Hostname of the database server from where
                        database would be copied.
  -d DESTINATION_DATABASE_HOST, --destination=DESTINATION_DATABASE_HOST
                        The destination host where database is being copied
                        to.
  -u USERNAME, --username=USERNAME
                        The UNIX user which will be executing.
  -p PASSWORD, --password=PASSWORD
                        The MySQL root password.
```

**Flow**

The current design does the following:

1. Ensure current commits to the source database is complete.
2. Shutdown database.
3. Take cold backup. Tar + gzip it.
4. Start source database.
5. Scp it into the destination host.
6. Unzip, and restore from physical backup.
7. Since then conf file was also copied, update the bind address. ( other conf parameters should be updated too )
8. Start MySQL.

**ACL**

The access control is something that I would keep more at the Unix level than at the database level, to ensure that we do not have to worry about different production and DEBUG builds.

The user who is the MySQL DBA and executes the tool for database migration would need sudo privileges without the password prompt to ensure smooth running of the fabric tasks. If she is willing to enter passwords , the sudoers file entry can be omitted. 

For external environments, the above would be a bad not-very-secure design. 
For internal R&D however, I would choose convenience over security.

To access the different hosts both manually and programmatically, we would need to maintain a central repository of authorized ssh public keys, which could be delivered by a configuration management framework like Puppet/Chef or a more simpler rsync. However for this proof of concept I've manually distributed them to all the 3 hosts.



**Cluster environments ( Replication scenario )**

In a master-slave cluster environment, I would choose the master for copying the database.
Since the method designed by me requires a cold backup, a system shutdown of the master would mean that the failover slave node would take over , preferably in read only mode.

The central repository would contain the following information:
- Mapping of environment with the cluster hosts.
- As for 'source' database host, the master would be considered.
- For destination database hosts(s), the fabric task would need to be called by adding multiple hosts in the -H parameter.  In the current fabfile.py this is where we need to pass on the multiple hosts https://github.com/sbose78/mysql-transfer/blob/master/fabfile.py#L83 in the Python list *hosts*
- After that, the configuration for the mysql server would need to be pushed using the information in the environment description fetced from the central repository.


**Future improvements**

- The fabfile.py should consume an environment descriptor file to get all environment specific parameters of remote hosts. In fact, the MySQL config file parameters should be defined in the environment descriptor and later on pushed to the relevant host(s).
- Support for specifying the database name.
- Distribution of authorized ssh public keys using a configuration manager like Puppet/Chef.
- Add logging.
- Track and wait if an existing database migration is taking place.
