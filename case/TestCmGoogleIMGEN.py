#!/usr/bin/env python
#-*-coding:utf-8-*-

import time
import random
import os
from time import sleep
from modules.GoogleIMGAPI import GoogleIMGAPI
from utils.logger import logger
class TestCmGoogleIMGEN(object):
    def __init__(self):
        pass

    def test001_find_images_EN(self):
        self.t = GoogleIMGAPI()
        url=''
        text=''
        result=3
        fo = open("conf.txt", "r")
        lo = fo.readlines()
        fo.close()
        for line in lo:
            pattern, value = line.split('=')

            if pattern == 'VISIT_RESULT':
                result = value
                logger.info("result={} ".format(  result))
                continue
            if  pattern == 'VISIT_TEXT' :
                text = value
                print(text)
                continue
            if pattern == 'VISIT_URL' :
                url = value
                print(url)
                continue

        self.t.Step1(url,text,result)
        print('test001_find_images_EN')
        sleep(1)
        self.t.close_chrome_browser()
    def test0_Setup_EN(self):
        print("setup")


    def test0_Teardown_EN(self):
        pass



