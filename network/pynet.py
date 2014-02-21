# coding=utf-8
#!/usr/bin/env python


from utils import network
from utils import util
import json
import urllib


_net_dict = {'sina_ip':
            {'query': {'format': 'text'}, 'base_url':
             'http://int.dpool.sina.com.cn/iplookup/iplookup.php?'},
             'youdao_ip':
            {'query': {'type': 'ip'}, 'base_url':
             'http://www.youdao.com/smartresult-xml/search.s?'},
             'baidu_releate':
            {'query': {}, 'base_url':
             'http://shangqing.baidu.com/trade/wordPv_view.htm?'},
             'baidu_search_num':
            {'query': {}, 'base_url':
             'http://shangqing.baidu.com/trade/wordPv_statistics.htm?'},
             'baidu_area_num':
            {'query': {'areaid': ''}, 'base_url':
             'http://shangqing.baidu.com/recomword/recomWordCache_findProvPvCache.htm?'},
             'sina_phone':
            {'query': {'output': 'json'}, 'base_url':
             'http://api.showji.com/Locating/www.showji.co.m.aspx?'}
             }


class PyNet(object):

    def __get_response(self, url, **kw):
        http_get_url = url + self.__encode_params(**kw)
        __response = network.get_html_string(http_get_url)
        if __response:
            return __response
        else:
            raise NetException, __callurl

    def __encode_params(self, **kw):
        args = []
        for k, v in kw.iteritems():
            qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
            args.append('%s=%s' % (k, urllib.quote(qv)))
        return '&'.join(args)

    def __getattr__(self, key):
        def wrap(**kw):
            if _net_dict.has_key(key):
                if _net_dict[key].has_key('base_url'):
                    __url = _net_dict[key]['base_url']
                else:
                    raise Exception('%s not contain base_url' % key)
            else:
                raise Exception('%s can\'t find service' % key)
            if _net_dict[key].has_key('query'):
                for __key, __val in _net_dict[key]['query'].items():
                    kw[__key] = __val
            return self.__get_response(url=__url, **kw)
        return wrap


if __name__ == '__main__':
    p = PyNet()
    print p.baidu_search_num(word='htc')
    print p.baidu_releate(word='htc')
    print p.baidu_area_num(word='htc', num=10, areaid='')
    print p.sina_ip(ip='220.181.111.86')
    print p.sina_phone(m='13833445577')
    # print p.youdao_ip(q = '220.181.111.86')