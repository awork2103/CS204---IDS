from scapy.all import rdpcap, TCP, IP
import os
import sys

# Define the pcap file and output directory
pcap_file = sys.argv[1]  
output_dir = "./extracted_payloads"
os.makedirs(output_dir, exist_ok=True)

# Dictionary to hold reassembled TCP streams
tcp_streams = {}

def extract_http_payload(packet):
    # Check if the packet is a TCP packet
    if not packet.haslayer(TCP):
        return

    # Get source and destination IP and ports
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    src_port = packet[TCP].sport
    dst_port = packet[TCP].dport

    # Create a unique key for the TCP stream
    stream_key = (src_ip, src_port, dst_ip, dst_port)

    # Initialize the stream if it doesn't exist
    if stream_key not in tcp_streams:
        tcp_streams[stream_key] = {
            'seq': 0,
            'data': b''
        }

    # Reassemble data based on sequence numbers
    current_seq = packet[TCP].seq
    if current_seq == tcp_streams[stream_key]['seq']:
        # If this is the expected segment, append its payload
        tcp_streams[stream_key]['data'] += bytes(packet[TCP].payload)
        tcp_streams[stream_key]['seq'] += len(bytes(packet[TCP].payload))
    elif current_seq > tcp_streams[stream_key]['seq']:
        # If this segment is ahead of what we expect, we may have missed some data.
        print(f"Warning: Out-of-order segment detected for {stream_key}")

def save_http_payload(stream_key):
    # Save the reassembled HTTP payload if it contains valid data
    data = tcp_streams[stream_key]['data']
    
    # Look for HTTP response header end (delimited by \r\n\r\n)
    headers_end = data.find(b"\r\n\r\n")
    
    if headers_end != -1:
        # Extract the HTTP body (payload) directly after headers
        payload_start = headers_end + 4
        file_payload = data[payload_start:]

        # Save the file payload to the output directory with a unique name
        filename = f"payload_{stream_key[0]}_{stream_key[1]}_{stream_key[2]}_{stream_key[3]}.txt"
        output_path = os.path.join(output_dir, filename)
        
        with open(output_path, "wb") as f:
            f.write(file_payload)
        
        print(f"Extracted payload to: {output_path}")

# Load the pcap file and apply extraction function to each packet
packets = rdpcap(pcap_file)

for pkt in packets:
    extract_http_payload(pkt)

# Save all extracted HTTP payloads from reassembled streams
for stream_key in tcp_streams.keys():
    save_http_payload(stream_key)

print("Payload extraction complete.")