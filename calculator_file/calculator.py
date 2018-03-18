#!/usr/bin/env python3

import sys
import csv
import os

class Args(object):
    #获取各参数位置
    def __init__(self):
        self.args = sys.argv[1:]
        self.indexc = self.args.index('-c') + 1
        self.indexd = self.args.index('-d') + 1
        self.indexo = self.args.index('-o') + 1

    def _check_para(self):
    #判断参数的数量,是否有6个
        return len(self.args) == 6 

    def _check_file(self):
    #判断各文件是否存在
        return os.path.exists(self.args[self.indexc]) and os.path.exists(self.args[self.indexd]) and os.path.exists(self.args[self.indexo])
    
class Config(object):
    #定义配置文件类,并将配置文件内容赋值给其属性.config
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
    #定义员工数据类,并将员工基本信息生成一个字典,赋值给属性.userdata
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
    #生成需要的信息:计算社保,税金,税后工资,并生成多行列表,并可以输出到gongzi.csv
    def __init__(self, cfg, ud):
    #定义各种属性,用来保存所需的信息
        self.rate_shebao = 0.00
        self.shebaobase = 0.00
        self.shebao = 0.00
        self.tax = 0.00
        self.taxed = 0.00
        self.result = []
        self.data = self._make_data(cfg, ud)
        
    def _make_data(self, cfg, ud):
    #计算各项所需信息,并保存到对应的属性中
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
    #计算税金
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
    输出信息到gongzi.csv
        with open(ar.args[ar.indexo], 'w') as file:
            writer = csv.writer(file)
            writer.writerows(self.result)
    
if __name__=='__main__':
    #check paramater
    ar = Args()
    if ar._check_para():    #检查参数数量是否完整
        if ar._check_file():    #检查文件是否存在
            cfg = Config(ar)    #创建配置文件对象,并获取配置文件信息
            ud = UserData(ar)    #创建员工数据库对象,并获取员工信息
            itc = IncomeTaxCalculator(cfg, ud)    #计算税金,社保,税后工资,并生成待输出信息
            itc._export(ar)    #将待输出信息输出到文件中
        else:        
            print('file is not existed')
    else:
        print('Parameter Error')
