#!/usr/bin/env python3

filename = '/home/hiro/shiyanlou_project/calculator_file/test.cfg'
config_dict = {}
with open(filename) as file:
    for line in file.readlines():
        a = line.strip('\n').split('=')
        config_dict[a[0].strip()] = a[1].strip()
        print(config_dict) 
       
