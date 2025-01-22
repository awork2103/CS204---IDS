#!/bin/bash 

# declare some variables 
FILEOBJ_DIR="./virustotal-files/$(date +%Y%m%d%H%M%S)"
VTAPI_SCRIPT="virustotal_api.py"

mkdir -p $FILEOBJ_DIR

tcpdump -r $1 -w $FILEOBJ_DIR/pcap.pcap dst host "192.168.175.43" > /dev/null 2>&1

tshark -o "tcp.desegment_tcp_streams:TRUE" -r $FILEOBJ_DIR/pcap.pcap --export-objects "http,$FILEOBJ_DIR" > /dev/null 2>&1

# Extract IP addresses of the senders
tshark -r $FILEOBJ_DIR/pcap.pcap -Y "http.file_data" -T fields -e ip.src -e http.file_data > "$FILEOBJ_DIR/ip_file_map.txt" 2>/dev/null
# cat ip_file_map.txt

# loop through each file in directory and send hash to virustotal 
for file in "$FILEOBJ_DIR"/*; do
    if [ -f "$file" ]; then  # Ensure it's a regular file not directory
        if [[ "$file" != *"unrestricted_file_upload"* ]]; then
            continue
        fi
        # Generate SHA1 hash
        HASH=$(sed -n '5,$p' $file | head -n -10 | sha1sum | awk '{ print $1 }') # EXTRACT THE CONTENT OF THE FILE
        # echo $HASH
        VT_SCORE=$(python3 $VTAPI_SCRIPT $HASH | awk '{ print $2 }')
        # echo $VT_SCORE

        # Find the corresponding IP address for the file
        FILE_CONTENT_HEX=$(xxd -p "$file" | tr -d '\n')
        SENDER_IP=$(grep "$FILE_CONTENT_HEX" "$FILEOBJ_DIR/ip_file_map.txt" | awk '{ print $1 }')

        # if VT_SCORE greater than or equal to 10 then send email (pass in the pcap file as an argument)
        VT_SCORE_INT=$(printf "%d" "$VT_SCORE")
        echo "Sender IP: " . $SENDER_IP
        if [[ $VT_SCORE_INT -ge 10 ]]; then
            ./sendNotif.sh $1 $SENDER_IP "Malicious file upload, hash: $HASH, VT Score: $VT_SCORE" 
        fi
        # rm $file
    fi
done

rm -rf $FILEOBJ_DIR