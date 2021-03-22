from selenium import webdriver
import Src.time_func as time_func
import time
import datetime


class Tb():
    """淘宝秒杀"""
    def __init__(self, goods_url, set_time, method=0):
        self.url = "https://www.taobao.com"  # 淘宝网站
        # 设置Chrome开发者模式
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.browser = webdriver.Chrome(options=options)
        self.goods_url = goods_url
        self.set_time = set_time
        self.method = method
        self.login()
        self.tb_buy()

    def login(self):
        """打开浏览器并登录"""
        self.browser.get(self.url)
        if self.browser.find_element_by_link_text("亲，请登录"):
            self.browser.find_element_by_link_text("亲，请登录").click()
            print("[{}] 请扫码登录".format(time_func.get_time()))
        # 淘宝登录后”亲，请登录“元素依然在，但会增加用户名元素，检查用户名已判断是否登录
        while True:
            try:
                if self.browser.find_element_by_link_text("tb189084993"):
                    print("[{}] 登录成功".format(time_func.get_time()))
                    break
                time.sleep(0.3)
            except:
                pass
        # time.sleep(30)  # 等待登录

    def tb_buy(self):
        # self.method:
        # 0:自动全选购物车
        # 1:用户自主选择要购买的商品
        # 2:用户输入宝贝链接

        # 自动全选购物车
        if self.method == 0:
            # 打开淘宝购物车
            self.browser.get("https://cart.taobao.com/cart.htm")
            # 等待打开购物车（找到购物车中独有”全选“元素，判定为打开）
            time.sleep(2)
            while True:
                try:
                    if self.browser.find_element_by_id("J_SelectAll1"):
                        self.browser.find_element_by_id("J_SelectAll1").click()
                        break
                except:
                    pass
                    # print("[{}] 未找到全选按钮".format(time_func.get_time()))
                    # time.sleep(0.1)
            self.auto_pay()

        # 用户自主选择要购买的商品
        elif self.method == 1:
            # 打开淘宝购物车
            self.browser.get("https://cart.taobao.com/cart.htm")
            # 等待打开购物车（找到购物车中独有”全选“元素，判定为打开）
            time.sleep(2)
            print("[{}] 请手动勾选需购买的物品".format(time_func.get_time()))
            time.sleep(10)
            self.auto_pay()

        # 用户输入宝贝链接
        elif self.method == 2:
            # 打开指定商品链接
            # 检查给入商品链接是否为合法淘宝链接
            if "taobao" in self.goods_url or "tmall" in self.goods_url:
                try:
                    self.browser.get(self.goods_url)
                    time.sleep(2)
                    print("[{}] 请尽快勾选所需物品型号")
                    time.sleep(5)
                    while True:
                        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        server_time = time_func.get_tb_server_time()
                        if (now_time > self.set_time) or (server_time > self.set_time):
                            while True:
                                try:
                                    if self.browser.find_element_by_link_text("\"立即购买\""):
                                        self.browser.find_element_by_link_text("\"立即购买\"").click()
                                        break
                                except:
                                    pass
                            while True:
                                try:
                                    if self.browser.find_element_by_link_text("提交订单"):
                                        self.browser.find_element_by_link_text("提交订单").click()
                                        print("[{}] <---------------抢购成功，请尽快付款--------------->".format(
                                            time_func.get_time()))
                                        break
                                except:
                                    print("[{}] 再次尝试提交订单".format(time_func.get_time()))
                except:
                    print("[{}] 无法打开指定链接".format(time_func.get_time()))
            else:
                print("[{}] 链接非法，请输入合法淘宝网商品链接".format(time_func.get_time()))

    def auto_pay(self):
        """自动结算提交订单函数"""
        # 比较时间点击结算
        while True:
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            server_time = time_func.get_tb_server_time()
            if (now_time > self.set_time) or (server_time > self.set_time):
                while True:
                    try:
                        # "id=J_Go"无效
                        # if browser.find_element_by_id("J_Go"):
                        #     browser.find_element_by_id("J_Go").click()
                        if self.browser.find_element_by_link_text("结 算"):
                            self.browser.find_element_by_link_text("结 算").click()
                            print("[{}] <---------------结算成功，等待提交订单--------------->".format(time_func.get_time()))
                            break
                    except:
                        pass
                while True:
                    try:
                        if self.browser.find_element_by_link_text("提交订单"):
                            self.browser.find_element_by_link_text("提交订单").click()
                            print("[{}] <---------------抢购成功，请尽快付款--------------->".format(time_func.get_time()))
                            break
                    except:
                        print("[{}] 再次尝试提交订单".format(time_func.get_time()))

