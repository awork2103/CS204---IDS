#!/bin/bash
echo "Running Snort on $1"
# Pass in PCAP into snort
SNORT_CONFIG=/etc/snort/snort.conf
LOG_DIR=./snortlog/$(date +%H%M%S)
LOG_FILE=$LOG_DIR/alert

mkdir -p $LOG_DIR
# Pass Pcap to snort and output to log variable
snort -r $1 -c $SNORT_CONFIG -l $LOG_DIR -A fast -q

ip_array=()

# Check if snort detects Web Attacks
# Loop through each "WEB ATTACK" entry in the log file
# 11/07-10:41:26.470489 [**] [1:1000001:1] WEB ATTACK - Brute Force Login Attempt [**] [Priority: 0] {TCP} 192.168.175.102:50525 -> 192.168.175.43:80
grep -q "WEB ATTACK" $LOG_FILE | while read -r line; do
    # Extract the attack type and IP address using awk
    ATTACK_TYPE=$(echo "$line" | awk -F'[][]' '{print $5}')
    IP_ADDRESS=$(echo "$line" | awk '{print $15}' | awk -F':' '{print $1}')
    echo "Detected $ATTACK_TYPE from $IP_ADDRESS"

    # Check if item is in array
    found=false
    for ip in "${ip_array[@]}"; do
        if [[ "$ip" == "$IP_ADDRESS" ]]; then
            found=true
            break
        fi
    done

    if [[ $found == false ]]; then
        ip_array+=("$IP_ADDRESS")
        ./sendNotif.sh $1 "$IP_ADDRESS" "$ATTACK_TYPE" &
    fi
done

# Remove log file after done
rm -rf $LOG_DIR