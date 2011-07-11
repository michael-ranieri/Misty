#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
calc.py - Phenny Calculator Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

# MODIFIED FROM FILE ABOVE TO WORK WITH MISTY

import sys, re, web, json

def c(input): 
   """Google calculator."""
   q = re.split(' ', input, 2)
   q = q[1].encode('utf-8')
   q = q.replace('\xcf\x95', 'phi') # utf-8 U+03D5
   q = q.replace('\xcf\x80', 'pi') # utf-8 U+03C0
   uri = 'http://www.google.com/ig/calculator?q='
   bytes = web.get(uri + web.urllib.quote(q))
   parts = bytes.split('",')
   answer = [p for p in parts if p.startswith('rhs: "')][0][6:]
   if answer: 
      answer = answer.decode('unicode-escape')
      answer = answer.replace(u'\xc2\xa0', ',')
      answer = answer.replace('<sup>', '^(')
      answer = answer.replace('</sup>', ')')
      answer = web.decode(answer)
      print answer.encode('utf-8')
   else: print 'Sorry, no result.'

if __name__ == '__main__':
   params = json.loads(sys.argv[1])
   msg, user, channel, users = params
   c(msg)

