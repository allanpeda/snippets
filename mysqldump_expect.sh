#!/bin/bash

# This uses expect to send the proper password (DB_PASSWORD) to mysqldump

# 30 minute timeout
# avoiding the warning that password on the command line may be insecure
expect -f - <<EOF
set timeout 1800
log_user 0
spawn -noecho mysqldump --dump-date --comments --result-file=${BACKUP_FILE_FULL_PATH} --add-drop-table -u ${DB_USER} -p -h ${DB_HOST} ${DB_NAME}
expect "password:"
send -- "${DB_PASSWORD}\r"
expect eof
catch wait result
exit [lindex \$result 3]
EOF
declare -i exit_code=$?
if [[ "${exit_code}" -eq 0 ]]
then
    echo "Export completed successfully."
else
    echo "Export exited with code: ${exit_code}\n"
fi
