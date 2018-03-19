#!/usr/bin/env python4

import sys
import csv
import os
from multiprocessing import Process, Queue, Pool

queue1 = Queue()
queue2 = Queue()

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
        return os.path.exists(self.args[self.indexc]) and os.path.exists(self.args[self.indexd])

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

class User(object):
    def __init__(self, cfg):
    #定义好要用的基本属性
        self.rate_shebao = 0.00
        for value in cfg.config.values():
            if value < 1:
                self.rate_shebao += value
        self.shebao = 0.00
        self.tax = 0.00
        self.taxed_income = 0.00
        self.result = []

    def _read_users_data(self, ar):
    #读取员工的工资信息
        user_dict = {}
        with open(ar.args[ar.indexd]) as file:
            for line in file.readlines():
                a = line.strip().split(',')
                user_dict[a[0].strip()] = int(a[1].strip())
            queue1.put(user_dict)

    def _create_newdata(self, cfg, key, value):
    #生成新的工资信息
        if value < cfg.config['JiShuL']:
            shebaobase = cfg.config['JiShuL']
        elif value > cfg.config['JiShuH']:
            shebaobase = cfg.config['JiShuH']
        else:
            shebaobase = value
        self.shebao = shebaobase * self.rate_shebao
        self.tax = self._calculate_tax(value - self.shebao - 3500)
        self.taxed_income = value - self.shebao - self.tax
        self.result.append([key, format(value,'.2f'), format(self.shebao,'.2f'), format(self.tax,'.2f'), format(self.taxed_income,'.2f')])
        print(self.result)
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

def export(ar, default='csv'):
#输出信息到gongzi.csv
    result = queue2.get()
    with open(ar.args[ar.indexo], 'w') as file:
        writer = csv.writer(file)
        writer.writerows(result)
    
if __name__=='__main__':
    #check paramater
    ar = Args()
    if ar._check_para():    #检查参数数量是否完整
        if ar._check_file():    #检查文件是否存在
            cfg = Config(ar)
            ud = User(cfg)
            Process(target=ud._read_users_data, args=(ar,)).start()
            pool = Pool(processes=3)
            user_data = queue1.get()
            for key, value in user_data.items():
                pool.apply(ud._create_newdata,(cfg,key,value))
            print(ud.result)
            queue2.put(ud.result)
            Process(target=export, args=(ar,)).start()
        else:        
            print('file is not existed')
    else:
        print('Parameter Error')
