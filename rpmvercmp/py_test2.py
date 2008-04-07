#!/usr/bin/python

import sys

sys.path.append('../pyutils')

import utils


#numbers = [1,2,3,4,5,6,100000,99900]
numbers = ['1','2','3','4','5','6','100000','99900', '1.2.5.6']

numbers = ['1','2','3','4','5','6','100000','99900', '1.2.5.6']

numbers = range(0, 10000)
numbers = map(str, numbers)

print utils.version_sort(numbers)
#utils.version_sort_native(numbers)

