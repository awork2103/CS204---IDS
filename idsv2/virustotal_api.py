#! /usr/bin/python3

import requests
import sys

API_KEY = "db0e4ea06229623a25b0f00ba9cedb3ed09a11ddf9f22daf08263078cf8d304c"  #<--- Put your API key here

class VirusTotal:
    def __init__(self):
        self.headers = {"accept": "application/json","X-Apikey": API_KEY}
        self.url = "https://www.virustotal.com/api/v3/search?query="

    def upload_hash(self, hash):
        url = self.url + hash
        # print(url)
        response = requests.get(url, headers=self.headers)
        result = response.json()
        # print(result)
        if response.status_code == 200 and len(result['data']) > 0:
            try:
                malicious = result['data'][0]['attributes']['last_analysis_stats']['malicious']
            except:
                malicious = 0
        else:
            malicious = 0
        
        if len(sys.argv) > 2:
            if malicious > int(sys.argv[2]):
                print(hash + " " + str(malicious))
        else:
            if malicious > 1:
                print(hash + " " + str(malicious))

if __name__ == "__main__":
    try:
        virustotal = VirusTotal()
        virustotal.upload_hash(sys.argv[1])
    except:
        None