#!/bin/bash

# Define the network interface and output file
INTERFACE="ens33"  # Replace with your network interface
DURATION="60"  # Capture duration in seconds
OUTPUT_FILE_NAME="$(date +%Y%m%d%H%M%S).pcap"
OUTPUT_FILE="./output/$OUTPUT_FILE_NAME"
ATTACKER_IP="192.168.175.235/32"
IDS_IP="192.168.175.43/32"

# mkdir ./output
touch "$OUTPUT_FILE"

# Run TShark on the specified interface and capture for 1 minute (60 seconds)
# Run bash script (that runs VT, RF Model and Snort) --> pass in pcap as arguement
# Wait for above script to finish then remove pcap file
tshark -i "$INTERFACE" -f "net $ATTACKER_IP and net $IDS_IP" -a duration:$DURATION -w "$OUTPUT_FILE" &&  ./runChecks.sh $OUTPUT_FILE && rm $OUTPUT_FILE

echo "TShark capture completed and saved to $OUTPUT_FILE"