

SOURCE_DB_HOST=$1
DESTINATION_DB_HOST=$2


fab take_cold_backup -H $SOURCE_DB_HOST
fab restore_backup -H $DESTINATION_DB_HOST
fab bind_to_host -H $DESTINATION_DB_HOST
