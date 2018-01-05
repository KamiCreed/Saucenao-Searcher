# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 23:01:22 2017

@author: KamiCreed
"""

import sys
import datetime
from time import sleep
import saucenao
import asyncio

def main():
    if (len(sys.argv) < 3):
        print("Input path to text file of image urls and path for output.")
        return
    
    s = saucenao.SauceNAO(open('api_key', 'r', encoding='utf-8').readline())
    with open(sys.argv[1], 'r', encoding='utf-8') as uf:
        with open(sys.argv[2], 'w', encoding='utf-8') as of:
            for x in uf:
                search = "http"
                x = search + x.strip().split(search,1)[1]
                if not x: continue

                print("\nSearching: " + x)
                print("Searching: " + x, file=of)
                print("------------------------------------", file=of)
                
                c = 0
                while True:
                    try:
                        loop = asyncio.get_event_loop()
                        results = loop.run_until_complete(s.search(x, 5))
                        if len(results) > 0 and results[0].similarity > 80:
                            size = len(results) if len(results) < 5 else 5
                            for i in range(size):
                                print("\n{}\n{}".format(results[i].desc(), results[i].url()), file=of)
                        else:
                            print("Nothing found")
                            print("Nothing found", file=of)
                        break
                    except saucenao.HTTPError as e:
                        if e.resp == 429:
                            print("Rate limited :(")
                            if c < 1:
                                sleep(602)
                                c += 1
                            else:
                                print("Current Date: " + str(datetime.datetime.now()))
                                sleep(86410) # 24 hours
                        else:
                            # Try Again.
                            print(e)
                            sleep(10)
                            
                sleep(3)

if __name__=='__main__':
    main()
