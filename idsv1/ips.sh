#!/bin/bash

# Function to run TShark
run_tshark() {
    echo "Running TShark"
    /bin/bash ./runTShark.sh
    if [ $? -eq 0 ]; then
        echo "Completed Running TShark"
    else
        echo "An error occurred while running TShark"
    fi
}

# Main function
main() {
    TSHARK_INTERVAL=60  # 60 seconds

    while true; do
        run_tshark &  # Run the function in the background
        sleep $((TSHARK_INTERVAL / 2))
    done
}

# Start the main function
main