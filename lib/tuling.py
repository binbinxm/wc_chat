#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import requests

class tuling:
    def __init__(self, key):
        self.__url = 'http://www.tuling123.com/openapi/api'
        self.__key = key

    def talk(self, msg):
        data = {
                'key'   :   self.__key,
                'info'  :   msg,
                'userid':   ''
                }
        try:
            r = requests.post(self.__url, data=data).json()
            return r.get('text')
        except:
            return

