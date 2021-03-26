from selenium import webdriver
import Src.time_func as time_func
import time
import datetime
import logging

# 配置log输出模式
logging.basicConfig(level=logging.INFO,
                    filename='record.log',
                    filemode='a',
                    format='%(filename)s - %(levelname)s: %(message)s')
logging.FileHandler(filename='record.log', encoding='utf-8')

class Tm():
    """天猫秒杀"""
    def __init__(self, set_time="", method=0, tb_id="tb189084993", goods_url=""):
        self.url = "https://www.tmall.com"  # 天猫网站
        # 设置Chrome开发者模式
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # 设置不加载图片
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        self.tb_id = tb_id
        self.browser = webdriver.Chrome(options=options)
        self.goods_url = goods_url
        self.set_time = set_time
        self.method = method
        self.logger = logging.getLogger()
        self.login()
        self.tm_buy()

    def login(self):
        """打开浏览器并登录"""
        self.browser.get(self.url)
        if self.browser.find_element_by_link_text("请登录"):
            self.browser.find_element_by_link_text("请登录").click()
            print("[{}] 请扫码登录".format(time_func.get_time()))
        # 淘宝登录后”亲，请登录“元素依然在，但会增加用户名元素，检查用户名已判断是否登录
        while True:
            try:
                if self.browser.find_element_by_link_text(self.tb_id):
                    print("[{}] 登录成功".format(time_func.get_time()))
                    break
                time.sleep(0.3)
            except:
                pass
        # time.sleep(30)  # 等待登录

    def tm_buy(self):
        # self.method:
        # 0:自动全选购物车
        # 1:用户自主选择要购买的商品
        # 2:用户输入宝贝链接
        self.logger.info("开始抢购商品")
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
            # 检查给入商品链接是否为合法淘宝/天猫链接
            if "taobao" in self.goods_url or "tmall" in self.goods_url:
                try:
                    self.browser.get(self.goods_url)
                    time.sleep(2)
                    print("[{}] 请尽快勾选所需物品型号".format(time_func.get_time()))
                    time.sleep(5)
                    while True:
                        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        server_time = time_func.get_tb_server_time()
                        if (now_time > self.set_time) or (server_time > self.set_time):
                            while True:
                                try:
                                    if self.browser.find_element_by_link_text("立即购买"):
                                        self.browser.find_element_by_link_text("立即购买").click()
                                        if self.browser.find_element_by_link_text("提交订单"):
                                            self.browser.find_element_by_link_text("提交订单").click()
                                            print("[{}] <---------------抢购成功，请尽快付款--------------->".format(
                                                time_func.get_datetime()))
                                            self.logger.info(time_func.get_datetime() + "<---抢购成功!--->商品链接:" + self.goods_url)
                                            break
                                except:
                                    pass
                            while True:
                                try:
                                    if self.browser.find_element_by_link_text("提交订单"):
                                        self.browser.find_element_by_link_text("提交订单").click()
                                        print("[{}] <---------------抢购成功，请尽快付款--------------->".format(
                                            time_func.get_datetime()))
                                        self.logger.info(time_func.get_datetime() + "<---抢购成功!--->商品链接:" + self.goods_url)
                                        return
                                except:
                                    print("[{}] 再次尝试提交订单".format(time_func.get_time()))
                except:
                    print("[{}] 无法打开指定链接".format(time_func.get_time()))
            else:
                print("[{}] 链接非法，请输入合法淘宝网商品链接".format(time_func.get_time()))

    def auto_pay(self):
        """自动结算"""
        # 比较时间点击结算
        while True:
            server_time = time_func.get_tb_server_time()
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            if (now_time > self.set_time) or (server_time > self.set_time):
                self.logger.info(now_time + "开始秒杀")
                while True:
                    try:
                        if self.browser.find_element_by_link_text("结 算"):
                            self.browser.find_element_by_link_text("结 算").click()
                            print("[{}][{}] <---------------结算成功，等待提交订单--------------->".format(now_time, server_time))
                            self.logger.info(now_time + "商品结算成功!")
                            self.auto_submit()
                            break
                    except:
                        pass

    # 页面跳转太慢了，此处从结算到提交订单是最大的时间损耗点
    def auto_submit(self):
        """自动提交订单"""
        while True:
            try:
                if self.browser.find_element_by_link_text("提交订单"):
                    self.browser.find_element_by_link_text("提交订单").click()
                    print("[{}][{}] <---------------抢购成功，请尽快付款--------------->".format(time_func.get_datetime(),
                                                                                       time_func.get_tb_server_time()))
                    self.logger.info(time_func.get_datetime() + "<---商品抢购成功!--->")
                    return
            except:
                print("再次尝试提交订单")
