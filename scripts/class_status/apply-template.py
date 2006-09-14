#!/usr/bin/env python

"""Usage: python make-final-html.py template content output"""
    
import sys, time
    
try:
    excname, template, contentname, outputname = sys.argv
except ValueError:
    print __doc__
    sys.exit(1)
                
template = file(template, 'rb').read()
content = file(contentname, 'rb').read()
output = template.replace('#DATE#', time.strftime('%c')).replace('#CONTENT#', content)
file(outputname, 'wb').write(output)
