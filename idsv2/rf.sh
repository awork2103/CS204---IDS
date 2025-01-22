echo "Running RF Model on $1"
# Run CICFlowMeter to convert pcap to CSV
CFM_PATH="/home/ids/cfm-cli/build/distributions/CICFlowMeter-4.0/CICFlowMeter-4.0/bin"
OUTPUT_CSV_DIR="/home/ids/CS204-Scripts//csv/"
mkdir -p $OUTPUT_CSV_DIR
cd $CFM_PATH
PCAP_FILE="/home/ids/CS204-Scripts/output/$(basename $1)"
./cfm $PCAP_FILE $OUTPUT_CSV_DIR
cd /home/ids/CS204-Scripts
FILE_NAME=$(basename $1)
CSV="./csv/$(echo $FILE_NAME)_Flow.csv"

# Run Python Script
# Arg 1: CSV, Arg 2: pcap
./rf_venv/bin/python3 rfmodel_use.py $CSV $1

rm $CSV

# Python Script reponsible for send email if malicious is detected