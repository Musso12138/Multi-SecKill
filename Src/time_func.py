import requests
import http.client
import time
import datetime


def get_time():
    """
    利用time.localtime获取本地时间，秒级
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_datetime():
    """
    datetime获取本地时间，毫秒级
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


def get_tb_server_time():
    """
    淘宝服务器时间，秒级
    """
    conn = http.client.HTTPConnection("www.taobao.com")
    conn.request("GET", "/")
    r = conn.getresponse()
    ts = r.getheader("date")  # 获取http头date部分
    # 将GMT时间转换成北京时间
    # ltime = time.struct_time(tm_year=, tm_mon=, tm_mday=, tm_hour=, tm_min=, tm_sec=, tm_wday=, tm_yday=, tm_isdst=)
    ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    # ttime = time.struct_time(tm_year=, tm_mon=, tm_mday=, tm_hour=, tm_min=, tm_sec=, tm_wday=, tm_yday=, tm_isdst=)
    ttime = time.localtime(time.mktime(ltime) + 8 * 60 * 60)
    # 形成可用时间格式
    format_time = "%u-%02u-%02u %02u:%02u:%02u" % (ttime.tm_year, ttime.tm_mon, ttime.tm_mday,
                                                   ttime.tm_hour, ttime.tm_min, ttime.tm_sec)
    return format_time
