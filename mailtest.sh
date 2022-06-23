#!/bin/bash

# This is a quick script to send test email messages
# to the email server defined below.
#
# June 22, 2022
# Allan Peda <allan.peda@gmail.com>
#
# Usage:
# bash mailtest.sh someone@somewhere.com

declare -r SMTP_SERVER='relay-mail.********.com'

if [[ ${#1} -eq 0 ]]; then
    echo "Please priovide a mail recipient."
    exit 1
fi
declare -r MAIL_FR="${1}"
declare -r MAIL_TO="${2:-$1}"

declare -r DUMMY_LETTER=$(mktemp)
trap "rm -f ${DUMMY_LETTER}" exit
cat<<EOF > "${DUMMY_LETTER}"
From: ${MAIL_FR}
To: ${MAIL_TO}
Subject: Test message from $(hostname)
Date: $(date --rfc-2822)

Hello ${MAIL_TO}
This is a test email message sent using curl.
.
EOF

if curl --help &>/dev/null; then
    curl --verbose --silent smtp://${SMTP_SERVER} --mail-from "${MAIL_FR}" --mail-rcpt "${MAIL_TO}" --upload-file "${DUMMY_LETTER}"
else
    echo "The curl command was not found, or is not in your PATH."
    exit 1
fi
