#!/usr/bin/env python3

import sys
import csv
import os

def check_para(args):
    index = args.index('-c')
    index1 = args.index('-d')
    return os.path.exists(args[index+1]) and os.path.exists(args[index+1])

class Config(object):
    def __init__(self, configfile):
        self._config = {}
        

if __name__=='__main__':
    #check paramater
    if len(sys.argv) == 7:
        args = sys.argv[1:]
        if check_para(args):
            print('ok')
        else:
            print('file is not existed')
    else:
        print('Parameter Error')
