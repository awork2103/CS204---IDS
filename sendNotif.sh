#!/bin/bash

# SSMTP Detail are in config file in /etc/ssmtp/ssmtp.config

# Email details
TO="smucs2023@gmail.com"
SUBJECT="$3 on $(date +%Y/%m/%d) at $(date +%H:%M:%S) from IP address: $2"

# Send mail
# $ mpack -s "Subject_heading" -d BODY  /path/to/file  recipient_email@example.com
mpack -s "$SUBJECT" $1 $TO

# Block IP address
ufw insert 1 reject from $2 to any

echo "Email sent successfully."