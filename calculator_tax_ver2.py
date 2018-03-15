#!/usr/bin/env python3

import sys

def calculate_tax(salary, tax_base):
#calculate tax and return taxed salary
    if tax_base < 0:
        return salary
    elif tax_base <= 1500:
        return salary - (tax_base * 0.03)
    elif tax_base <= 4500:
        return salary - (tax_base * 0.10 - 105)
    elif tax_base <= 9000:
        return salary - (tax_base * 0.20 - 555)
    elif tax_base <= 35000:
        return salary - (tax_base * 0.25 - 1005)
    elif tax_base <= 55000:
        return salary - (tax_base * 0.30 - 2755)
    elif tax_base <= 80000:
        return salary - (tax_base * 0.35 - 5505)
    else:
        return salary - (tax_base * 0.45 - 13505)
    
if __name__=="__main__":
#recognize error and create a salary dict   
    para_list = sys.argv[1:]
    salarydict = {}
    try:
        for para in para_list:
            a, b = para.split(':')
            salarydict[a] = int(b)
    except ValueError:
        print("Parameter Error")

for key,value in salarydict.items():
    taxed_salary = calculate_tax(value*0.835, value*0.835-3500)
    print(key + ":" + format(taxed_salary,".2f"))    

