#!/usr/bin/python

import rpmvercmp

#numbers = [1,2,3,4,5,6,100000,99900]
numbers = ['1','2','3','4','5','6','100000','99900', '1.2.5.6']

numbers = ['1','2','3','4','5','6','100000','99900', '1.2.5.6']

numbers.sort(rpmvercmp.version_compare)

print numbers

