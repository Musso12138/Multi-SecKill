from selenium import webdriver
import Src.time_func as time_func
import time
import datetime


class Tm():
    """天猫秒杀≈淘宝"""
    def __init__(self, goods_url, set_time, method=0):
        self.url = "https://www.tmall.com/"  # 天猫网站
        # 设置Chrome开发者模式
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.browser = webdriver.Chrome(options=options)
        self.goods_url = goods_url
        self.set_time = set_time
        self.method = method
        self.login()
        self.tm_buy()

    def login(self):
        """打开浏览器并登录"""
        self.browser.get(self.url)
        if self.browser.find_element_by_link_text("请登录"):
            self.browser.find_element_by_link_text("请登录").click()
            print("[{}] 请扫码登录".format(time_func.get_time()))
        # 天猫登录后网页元素”请登录“会被替换为用户名
        while True:
            try:
                if not self.browser.find_element_by_link_text("请登录"):
                    print("[{}] 登录成功".format(time_func.get_time()))
                    break
                time.sleep(0.3)
            except:
                pass

    def tm_buy(self):
        # 打开天猫购物车（和淘宝url同）
        self.browser.get("https://cart.taobao.com/cart.htm")
        # 等待打开购物车（找到购物车中独有”全选“元素，判定为打开）
        time.sleep(2)
        # 待测试
        # while True:
        #     try:
        #         if self.browser.find_element_by_id("J_SelectAll1"):
        #             break
        #     except:
        #         pass

        # self.method:
        # 0:自动全选购物车
        # 1:用户自主选择要购买的商品
        if self.method == 0:
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
        elif self.method == 1:
            print("[{}] 请手动勾选需购买的物品".format(time_func.get_time()))
            time.sleep(10)
            self.auto_pay()

    def auto_pay(self):
        """自动结算提交订单"""
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

