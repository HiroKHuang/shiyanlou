#!/usr/bin/env python3

import sys
import csv
import os

class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]
        self.indexc = self.args.index('-c') + 1
        self.indexd = self.args.index('-d') + 1

    def _check_para(self,args):
        return len(args) == 6 

    def _check_file(self,args):
        return os.path.exists(args[self.indexc]) and os.path.exists(args[self.indexd])
    
class Config(object):
    def __init__(self, ar):
        self.config = self._read_config(ar)
   
    def _read_config(self, ar):
        config_dict = {}
        with open(ar.args[ar.indexc]) as file:
            for line in file.readlines():
                a = line.strip('\n').split('=')
                config_dict[a[0].strip()] = a[1].strip()
            return config_dict

class UserData(object):
    def __init__(self, ar):
        self.userdata = self._read_users_data(ar)

    def _read_users_data(self, ar):
        user_dict = {}
        with open(ar.args[ar.indexd]) as file:
            for line in file.readlines():
                a = line.strip('\n').split(',')
                user_dict[a[0].strip()] = a[1].strip()
            return user_dict

class IncomeTaxCalculator(object):
    def __init__(self, cfg, ud):
        self.data = self._make_data(cfg, ud)
    
    def _make_data(self, cfg, ud):
        for a in cfg.config.values:
             print(a)
        
        

if __name__=='__main__':
    #check paramater
    ar = Args()
    if ar._check_para(ar.args):
        if ar._check_file(ar.args):
            cfg = Config(ar)
            ud = UserData(ar)
            itc = IncomeTaxCalculator(cfg, ud)
        else:        
            print('file is not existed')
    else:
        print('Parameter Error')
