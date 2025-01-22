#!/bin/bash 

# declare some variables 
CICFLOWMETER_PATH=""
PRIVATEKEY_PATH=""
FILEOBJ_DIR=""
VTAPI_SCRIPT=""

# capture traffic with tshark 
# time interval and space, see which ever hits first
tshark -f "tcp port 44" -i any -a duration:60 -w capture.pcap
# ^ 60 seconds first 

# start thread 1
# run cfm on captured pcap 
cicflowmeter -f capture.pcap -c flows.csv

# run the csv file through the ml model 

# thread 1 ends here 

# start thread 2 
# decrypt pcap traffic and export objects > http 
# tshark -r capture.pcap \
# -o "tls.keylog_file:${PRIVATEKEY_PATH}" \
# -o "tls.desegment_ssl_records:TRUE" \
# -o "tls.desegment_tls_application_data:TRUE" \
# -d tcp.port==443,tls \
# --export-objects http,$FILEOBJ_DIR

tshark -r capture2.pcap \
-Y "http.content_type contains \"multipart/form-data\"" \
-w form-data.pcap

tshark -r form-data.pcap --export-objects http,$FILEOBJ_DIR

# loop through each file in directory and send hash to virustotal 
for file in "$FILEOBJ_DIR"/*; do
    if [ -f "$file" ]; then  # Ensure it's a regular file not directory
        # Generate SHA1 hash
        HASH=$(sed -n '5,$p' $file | head -n -10 | sha256sum | awk '{ print $1 }')
        echo $HASH
        # VT_SCORE=$(python $VTAPI_SCRIPT $HASH | awk '{ print $2 }')
        rm $file
    fi
done

