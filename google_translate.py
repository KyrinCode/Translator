#!/usr/bin/env python

import sys, getopt
import urllib.request
from HandleJs import Py4Js

from config import _h, _l, __list

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

    if(settings[2] == "develop"):
        print(result)
    else:
        end = result.find("\",")
        if end > 4:
            print(result[4:end])

def get_settings(argv):
    settings = ["auto", "auto", "default"]
    content = ""
    try:
        opts, args = getopt.getopt(argv,"hlas:t:c:",["help", "list", "all", "sl=", "tl=", "content="])
    except getopt.GetoptError:
        print("google_translate.py -h")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(_h)
            sys.exit()
        elif opt == "-l":
            print(_l)
            sys.exit()
        elif opt == "--list":
            print(__list)
            sys.exit()
        elif opt in ("-a", "--all"):
            settings[2] = "develop"
        elif opt in ("-s", "--sl"):
            if(arg == "cn"):
                settings[0] = "zh-CN"
            elif(arg == "tw"):
                settings[0] = "zh-TW"
            else:
                settings[0] = arg
        elif opt in ("-t", "--tl"):
            if(arg == "cn"):
                settings[1] = "zh-CN"
            elif(arg == "tw"):
                settings[1] = "zh-TW"
            else:
                settings[1] = arg
        elif opt in ("-c", "--content"):
            content = arg
    print("sl: " + settings[0] + " tl: " + settings[1] + " mode: " + settings[2])
    return settings, content
    
def main(argv):
    settings, content = get_settings(argv)
    print("Translate: " + content)
    js = Py4Js()
    
    while 1:   
        if content in ("q", "exit"):
            break
        tk = js.getTk(content)
        translate(settings, content, tk)

        content = input("Translate: ")
        
if __name__ == "__main__":
    main(sys.argv[1:])
