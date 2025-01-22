import subprocess
import re
import os
from collections import defaultdict
import sys

def extract_multipart_files(pcap_file, output_dir):
    """
    Extract multipart/form-data file objects from TCP streams in a PCAP file.
    
    Args:
        pcap_file (str): Path to the PCAP file
        output_dir (str): Directory to save extracted files
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # First, get all TCP streams with HTTP traffic
    tshark_streams_cmd = [
        'tshark',
        '-r', pcap_file,
        '-Y', 'http.request.method == "POST" && http.content_type contains "multipart/form-data"',
        '-T', 'fields',
        '-e', 'tcp.stream'
    ]
    
    result = subprocess.run(tshark_streams_cmd, capture_output=True, text=True)
    tcp_streams = set(result.stdout.strip().split('\n'))
    
    # Process each TCP stream
    for stream in tcp_streams:
        if not stream:  # Skip empty streams
            continue
            
        # Extract reassembled TCP stream
        tshark_follow_cmd = [
            'tshark',
            '-r', pcap_file,
            '-q',
            '-z', f'follow,tcp,raw,{stream}'
        ]
        
        stream_data = subprocess.run(tshark_follow_cmd, capture_output=True, text=True)
        
        # Parse the boundary from Content-Type header
        boundary_match = re.search(r'boundary=(-+\w+)', stream_data.stdout)
        if not boundary_match:
            continue
            
        boundary = boundary_match.group(1)
        
        # Split content by boundary
        parts = stream_data.stdout.split(boundary)
        
        # Process each part
        for part in parts:
            # Look for Content-Disposition header
            disposition_match = re.search(r'Content-Disposition:.*?filename="(.+?)"', part, re.IGNORECASE | re.DOTALL)
            if not disposition_match:
                continue
                
            filename = disposition_match.group(1)
            
            # Find the content by looking for double newline
            content_parts = part.split('\r\n\r\n', 1)
            if len(content_parts) < 2:
                continue
                
            # Extract the content (excluding headers)
            content = content_parts[1].strip()
            
            # Save the content to a file
            output_path = os.path.join(output_dir, f"stream_{stream}_{filename}")
            try:
                with open(output_path, 'wb') as f:
                    # Convert content to bytes, handling potential encoding issues
                    f.write(content.encode('raw_unicode_escape'))
                print(f"Extracted file: {output_path}")
            except Exception as e:
                print(f"Error saving file {filename}: {e}")

def main():
    # Example usage
    pcap_file = sys.argv[1]
    output_dir = "./virustotal-files"
    
    print(f"Processing PCAP file: {pcap_file}")
    extract_multipart_files(pcap_file, output_dir)
    print("Extraction complete!")

if __name__ == "__main__":
    main()
