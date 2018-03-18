#!/usr/bin/env python3

import sys
import csv
import os

class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]
        self.indexc = self.args.index('-c') + 1
        self.indexd = self.args.index('-d') + 1
        self.indexo = self.args.index('-o') + 1

    def _check_para(self):
        return len(self.args) == 6 

    def _check_file(self):
        return os.path.exists(self.args[self.indexc]) and os.path.exists(self.args[self.indexd]) and os.path.exists(self.args[self.indexo])
    
class Config(object):
    def __init__(self, ar):
        self.config = self._read_config(ar)
   
    def _read_config(self, ar):
        config_dict = {}
        with open(ar.args[ar.indexc]) as file:
            for line in file.readlines():
                a = line.strip('\n').split('=')
                config_dict[a[0].strip()] = float(a[1].strip())
            return config_dict

class UserData(object):
    def __init__(self, ar):
        self.userdata = self._read_users_data(ar)

    def _read_users_data(self, ar):
        user_dict = {}
        with open(ar.args[ar.indexd]) as file:
            for line in file.readlines():
                a = line.strip().split(',')
                user_dict[a[0].strip()] = int(a[1].strip())
            return user_dict

class IncomeTaxCalculator(object):
    def __init__(self, cfg, ud):
        self.rate_shebao = 0.00
        self.shebaobase = 0.00
        self.shebao = 0.00
        self.tax = 0.00
        self.taxed = 0.00
        self.result = []
        self.data = self._make_data(cfg, ud)
        
    def _make_data(self, cfg, ud):
        for value in cfg.config.values():
            if value < 1: 
                self.rate_shebao += value
        
        for key, value in ud.userdata.items():
            if value < cfg.config['JiShuL']:
                self.shebaobase = cfg.config['JiShuL']
            elif value > cfg.config['JiShuH']:
                self.shebaobase = cfg.config['JiShuH']
            else:
                self.shebaobase = value
            self.shebao = self.shebaobase * self.rate_shebao
            self.tax = self._calculate_tax(value-self.shebao-3500)
            self.taxed = value - self.shebao - self.tax
            self.result.append([str(key), str(value), format(self.shebao, '.2f'), format(self.tax, '.2f'), format(self.taxed, '.2f')])
      
    def _calculate_tax(self,tax_base):
    #calculate tax and return taxed salary
        if tax_base < 0:
            return 0.00
        elif tax_base <= 1500:
            return tax_base * 0.03
        elif tax_base <= 4500:
            return tax_base * 0.10 - 105
        elif tax_base <= 9000:
            return tax_base * 0.20 - 555
        elif tax_base <= 35000:
            return tax_base * 0.25 - 1005
        elif tax_base <= 55000:
            return tax_base * 0.30 - 2755
        elif tax_base <= 80000:
            return tax_base * 0.35 - 5505
        else:
            return tax_base * 0.45 - 13505

    def _export(self, ar, default='csv'):
        with open(ar.args[ar.indexo], 'w') as file:
            writer = csv.writer(file)
            writer.writerows(self.result)
    
if __name__=='__main__':
    #check paramater
    ar = Args()
    if ar._check_para():
        if ar._check_file():
            cfg = Config(ar)
            ud = UserData(ar)
            itc = IncomeTaxCalculator(cfg, ud)
            itc._export(ar)
        else:        
            print('file is not existed')
    else:
        print('Parameter Error')
