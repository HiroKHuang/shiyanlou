#!/usr/bin/env python3
#caculate tax

import sys
try:
    salary = int(sys.argv[1]) - 3500 
except ValueError:
    print("Parameter Error")

if salary <= 1500:
    tax = salary * 0.03
elif salary <= 4500:
    tax = salary * 0.1 - 105
elif salary <= 9000:
    tax = salary * 0.2 - 555
elif salary <= 35000:
    tax = salary * 0.25 - 1005
elif salary <= 55000:
    tax = salary * 0.3 - 2755
elif salary <= 80000:
    tax = salary * 0.35 - 5505
else:
    tax = salary * 0.45 - 13505
print(format(tax,".2f"))


