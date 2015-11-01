./run.py -s 192.168.43.149 -d 192.168.43.148 -u sbose -p my_mysql_root_password

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