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


def time_out(set_time, now_time, time_limit=180):
    """
    超时函数，若当前时间超出预设时间预设时限长，则返回true
    当前时间：now_time，"%Y-%m-%d %H:%M:%S"格式
    预设时间：set_time，"%Y-%m-%d %H:%M:%S"格式
    预设时限：time_limit，默认为180（3分钟），int型
    """
    # 将输入的时间转化为int格式
    set_time_int = int(set_time[11:13]) * 3600 + int(set_time[14:16]) * 60 + int(set_time[17:19])
    now_time_int = int(now_time[11:13]) * 3600 + int(now_time[14:16]) * 60 + int(now_time[17:19])
    # print(set_time)
    # print(set_time_int)
    # print(now_time)
    # print(now_time_int)
    if now_time_int - set_time_int >= time_limit:
        return True
    else:
        return False


if __name__ == "__main__":
    if time_out("2020-03-31 19:40:03", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"), 180):
        print(datetime.datetime.now())
