# coding=utf-8


import threading
import util
import re
import network


ipregx = re.compile("[0-9]{1,3}(\.[0-9]{1,3}){3}", re.UNICODE)
suggesturl = 'http://esug.baidu.com/su?'
ip_url = "http://opendata.baidu.com/api.php?"
ip_sina_url = "http://counter.sina.com.cn/ip?"


sina_regx = re.compile("Array\([^)]*\)")


def get_suggest_word(word):
    query = {"wd": word,
             "p": 3,
             "t": util.timems()}
    return network.get_html_string(baseurl=suggesturl, data=query)


def get_bd_ip_local(ip):
    query = {"query": ip,
             "co": "",
             "resource_id": "6006",
             "t": util.timems(),
             "ie": "utf8",
             "oe": "gbk",
             "cb": "bd__cbs__yk2g9h",
             "format": "json",
             "tn": "baidu"}

    return network.get_html_string(ip_url, query)


def get_ip_location(ip):
    return util.jsonstrtodict(util.getjson(get_bd_ip_local(ip)))['data'][0]['location']


def get_sina_ip_info(ip):
    query = {
        "ip": ip,
        "t": util.timems()
    }
    header = {
        "Host": "counter.sina.com.cn",
        "Referer": "http://biz.finance.sina.com.cn/baishi/ip.php"
    }
    return network.get_html_string(ip_sina_url, query, header)


def is_ip(ip):
    if ipregx.match(str(ip).strip()):
        return True
    return False


def get_sina_ip_location(ip):
    if not is_ip(ip):
        return "not ip!"
    data = get_sina_ip_info(ip)
    m = sina_regx.search(data)
    if m:
        location = m.group().split("\"")
        try:
            locationstr = "%s %s %s %s" % (
                location[3], location[5], location[7], location[9])
        except Exception:
            return ""
        return locationstr
    return "not find ip info"


class test(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            print util.getjson(get_bd_ip_local("220.181.111.86"))

if __name__ == "__main__":
    print network.get_html_string('http://counter.sina.com.cn/ip?ip=220.181.111.85&t=1392362718869', {}).encode("utf-8")
    print get_sina_ip_info("221.5.66.32")
