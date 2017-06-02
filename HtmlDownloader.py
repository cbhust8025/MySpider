#!/usr/bin/env python
# encoding: gbk
'''
这里使用urllib2下载Html，用于解析
'''
import urllib2

class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None
        print url
        response = urllib2.urlopen(url)
        html = response.read()
        #print html
        return html