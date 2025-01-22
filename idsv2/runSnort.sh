#!/bin/bash

# echo "Running Snort on $1"
# Pass in PCAP into snort
SNORT_CONFIG=/etc/snort/snort.conf
LOG_DIR=./snortlog/$(date +%H%M%S)
TIMER=60s


mkdir -p $LOG_DIR
# Pass Pcap to snort and output to log variable
timeout $TIMER snort -c $SNORT_CONFIG -l $LOG_DIR -A fast -q

# Run Snort script
./snort.sh $LOG_DIR

echo "Snort finished"

# Remove log file after done
# rm -rf $LOG_DIR