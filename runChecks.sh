#!/bin/bash

# Run the three scripts in parallel --> pass in pcap as argument ($1 == pcap)
./rf.sh $1 &
PID1=$!

./virustotal.sh $1 &
PID2=$!
# ./snort.sh $1 &
# PID3=$!

# Wait for all scripts to complete
wait $PID1
wait $PID2
# wait $PID3

echo "All scripts have completed."

rm $1