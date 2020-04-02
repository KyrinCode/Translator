#!/usr/bin/env python

import sys, getopt
import urllib.request
from HandleJs import Py4Js

from config import _h2, _l, __list

def open_url(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url = url,headers=headers)
    response = urllib.request.urlopen(req)
    data = response.read().decode('utf-8')
    return data
    
def translate(settings, content, tk):
    if len(content) > 4891:
        print("limit exceeded!")
        return
        
    content = urllib.parse.quote(content)
        
    url = "http://translate.google.cn/translate_a/single?client=t" + "&sl=%s&tl=%s"%(settings[0], settings[1]) + "&hl=en&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&srcrom=0&ssel=0&tsel=0&kc=2" + "&tk=%s&q=%s"%(tk, content)
        
    result = open_url(url)

    if(settings[2] == "dev"):
        print(result)
    else:
        end = result.find("\",")
        if end > 4:
            print(result[4:end])

def process_argv(argv):
    try:
        opts, args = getopt.getopt(argv, "hl", ["help", "list"])
    except getopt.GetoptError:
        print("google_translate_v2.py -h")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(_h2)
            sys.exit()
        elif opt == "-l":
            print(_l)
            sys.exit()
        elif opt == "--list":
            print(__list)
            sys.exit()
    
def main(argv):
    if argv:
        process_argv(argv)
    settings = ["auto", "auto", "def"]
    print("\n----------Settings----------")
    print("sl: %s tl: %s mode: %s" % (settings[0], settings[1], settings[2]))
    
    js = Py4Js()
    
    while 1:
        content = input("\nTranslate/(S): ")
        
        if content in ("q", "exit"):
            break
        
        if content in ("S"):
            print("\n--------Old Settings--------")
            print("sl: %s tl: %s mode: %s" % (settings[0], settings[1], settings[2]))
            
            print("\n------Change Settings-------")
            input_settings = input("sl tl mode: ")
            input_settings = input_settings.replace("cn", "zh-CN")
            input_settings = input_settings.replace("tw", "zh-TW")
            new_settings = input_settings.split()
            for i in range(len(new_settings)):
                settings[i] = new_settings[i]
            
            print("\n--------New Settings--------")
            print("sl: %s tl: %s mode: %s" % (settings[0], settings[1], settings[2]))
            continue
        
        tk = js.getTk(content)
        translate(settings, content, tk)
        
if __name__ == "__main__":
    main(sys.argv[1:])