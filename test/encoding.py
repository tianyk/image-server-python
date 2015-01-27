#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'tyk'

import urllib

# text = u'黑体字'
#
# print urllib.quote(text.encode('utf-8'))

text = u'%E9%BB%91%E4%BD%93%E5%AD%97'
print text.decode('utf-8')
print text.encode('utf-8')

print urllib.unquote(text.encode('utf-8'))
# print type(urllib.unquote(text))
#
# print urllib.unquote(text).decode('utf-8')
