#!/usr/bin/env python
# encoding: gbk
'''
����ʹ��urllib2����Html�����ڽ���
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