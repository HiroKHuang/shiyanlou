#!/usr/bin/env python3
import getopt
import configparser
import sys
import csv
from datetime import datetime
from multiprocessing import Process, Queue

class Args(object):
    #专门处理命令行参数,用于存放参数信息
    def __init__(self,options):
        self.city = ''
        self.cfgfile = ''
        self.udfile = ''
        self.opfile = ''
        self._get_args(options)
    
    def _get_args(self,options):
        for name,value in options:
            if name == '-C':
                self.city = value.upper()
            if name == '-c':
                self.cfgfile = value
            if name == '-d':
                self.udfile = value
            if name == '-o':
                self.opfile = value
        if self.city == '':
            self.city = 'DEFAULT'

class Config(object):
    #专门处理配置文件,存放配置文件参数信息
    def __init__(self, ar):
        self.shebao_rate = 0.00
        self.jishul = 0.00
        self.jishuh =0.00
        self._read_config(ar)

    def _read_config(self, ar):
        config_dict = {}
        conf = configparser.ConfigParser()
        conf.read(ar.cfgfile)
        self.shebao_rate = conf.getfloat(ar.city, 'YangLao') + \
                           conf.getfloat(ar.city, 'YiLiao') + \
                           conf.getfloat(ar.city, 'GongShang') + \
                           conf.getfloat(ar.city, 'ShengYu') + \
                           conf.getfloat(ar.city, 'ShiYe') + \
                           conf.getfloat(ar.city, 'GongJiJin')
        self.jishul = conf.getfloat(ar.city, 'JiShuL')
        self.jishuh = conf.getfloat(ar.city, 'JiShuH')

class User(object):
    #专门处理人员工资文件,并生成新的工资信息
    def __init__(self):
        self.shebao = 0.00
        self.tax = 0.00
        self.taxed_income = 0.00
        self.result = []

    def _read_users_data(self, ar):
        user_dict = {}
        with open(ar.udfile) as file:
            for line in file.readlines():
                a = line.strip().split(',')
                user_dict[a[0].strip()] = int(a[1].strip())
            queue1.put(user_dict)

    def _create_newdata(self, cfg):
        user_data = queue1.get()
        for key, value in user_data.items():
            if value < cfg.jishul:
                shebaobase = cfg.jishul
            elif value > cfg.jishuh:
                shebaobase = cfg.jishuh
            else:
                shebaobase = value
            self.shebao = shebaobase * cfg.shebao_rate
            self.tax = self._calculate_tax(value - self.shebao - 3500)
            self.taxed_income = value - self.shebao - self.tax
            self.result.append([key, format(value,'.2f'), \
                               format(self.shebao,'.2f'), \
                               format(self.tax,'.2f'), \
                               format(self.taxed_income,'.2f'), \
                               datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')])
        queue2.put(self.result)

    def _calculate_tax(self,tax_base):
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
    #专门输出信息到文件
    result = queue2.get()
    with open(ar.opfile, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(result)

if __name__=='__main__':
    queue1 = Queue()    #queue1用于存放初始员工信息
    queue2 = Queue()    #queue2用于存放处理后的员工信息
    try:
        options,args = getopt.getopt(sys.argv[1:], 'c:d:o:*C:')
    except:
        print("Parameter Error")
    ar = Args(options)
    cfg = Config(ar)
    ud = User()
    Process(target=ud._read_users_data, args=(ar,)).start()
    Process(target=ud._create_newdata, args=(cfg,)).start()
    Process(target=export, args=(ar,)).start()

