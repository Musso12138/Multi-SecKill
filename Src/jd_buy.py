from selenium import webdriver
import Src.time_func as time_func
import time
import datetime
import logging
import Src.MyLib.PopupWindow as PopupWindow
import Src.MyLib.SendEmail as SendMail

# 配置log输出模式
logging.basicConfig(level=logging.INFO,
                    filename='record.log',
                    filemode='a',
                    format='%(filename)s - %(levelname)s: %(message)s')
logging.FileHandler(filename='record.log', encoding='utf-8')

class Jd():
    """京东秒杀"""
    def __init__(self, set_time="", method=0, jd_id="Musso190", goods_url="", email=""):
        self.url = "https://www.jd.com/"  # 京东网站
        # 设置Chrome开发者模式
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # 设置不加载图片，可打开
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # options.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(options=options)
        self.set_time = set_time  # 预设抢购开始时间
        self.method = method      # 抢购模式
        self.jd_id = jd_id        # 淘宝用户名
        self.goods_url = goods_url  # 手动输入商品链接模式下，输入的商品链接
        if "@" in email:
            self.email = email    # 用户邮箱，用来接收抢购结果反馈
        self.logger = logging.getLogger()  # 日志
        self.login()
        self.jd_buy()

    def login(self):
        """打开浏览器并登录"""
        self.browser.get(self.url)
        if self.browser.find_element_by_link_text("你好，请登录"):
            self.browser.find_element_by_link_text("你好，请登录").click()
            print("[{}] 请扫码登录".format(time_func.get_time()))
        # 京东登录后”你好，请登录“元素会消失，也会增加用户名元素，通过检查用户名元素来判断是否成功登录
        while True:
            try:
                if self.browser.find_element_by_class_name("nickname"):
                    print("[{}] 登录成功".format(time_func.get_time()))
                    break
                time.sleep(0.3)
            except:
                pass

    def jd_buy(self):
        # self.method:
        # 0:自动全选购物车
        # 1:用户自主选择要购买的商品
        # 2:用户输入宝贝链接
        self.logger.info("开始抢购商品，抢购模式为:" + str(self.method) + "设定时间为:" + self.set_time)
        # 自动全选购物车
        if self.method == 0:
            # 打开京东购物车
            self.browser.get("https://cart.jd.com/cart_index/")
            # 等待打开购物车
            time.sleep(2)
            while True:
                try:
                    # 找到全选按钮并点击
                    if self.browser.find_element_by_class_name("cart-checkbox"):
                        self.browser.find_element_by_class_name("cart-checkbox").click()
                        break
                except:
                    pass
                    # print("[{}] 未找到全选按钮".format(time_func.get_time()))
                    # time.sleep(0.1)
            self.auto_pay()

        # 用户自主选择要购买的商品
        elif self.method == 1:
            # 打开京东购物车
            self.browser.get("https://cart.jd.com/cart_index/")
            # 等待打开购物车（找到购物车中独有”全选“元素，判定为打开）
            time.sleep(2)
            # 此处无法判断用户何时选择完毕，选择等待10s为用户选择完毕时间
            print("[{}] 请手动勾选需购买的物品".format(time_func.get_time()))
            time.sleep(10)
            self.auto_pay()

        # 用户输入宝贝链接
        elif self.method == 2:
            # 检查给入商品链接是否为合法淘宝链接
            if "jd" in self.goods_url:
                try:
                    # 打开指定商品链接
                    self.browser.get(self.goods_url)
                    time.sleep(2)
                    # 等待勾选抢购的商品型号
                    print("[{}] 请尽快勾选所需物品型号".format(time_func.get_time()))
                    time.sleep(5)
                    # 京东要先加入购物车
                    if self.browser.find_element_by_link_text("加入购物车"):
                        self.browser.find_element_by_link_text("加入购物车").click()
                    time.sleep(0.5)
                    self.auto_pay()
                except:
                    print("[{}] 无法打开指定链接".format(time_func.get_time()))
                    self.logger.info("无法打开指定链接，抢购失败")
            else:
                print("[{}] 链接非法，请输入合法淘宝网商品链接".format(time_func.get_time()))
                self.logger.info("给入链接非法，抢购失败")

    def auto_pay(self):
        """自动结算"""
        # 比较时间点击结算
        while True:
            server_time = time_func.get_tb_server_time()  # get_jd_server_time
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            # 如果结算超时，则判定为抢购失败
            if time_func.time_out(set_time=self.set_time, now_time=now_time):
                print("[{}][{}] <---------------结算超时，抢购失败--------------->".format(now_time, server_time))
                # 将超时记录记入日志
                self.logger.info(now_time + "商品结算超时，抢购失败")
                # 弹窗失败提示
                PopupWindow.UiMainWindow(message=PopupWindow.fail_message)
                if self.email:
                    SendMail.SendEmail(self.email, SendMail.platform_list["jingdong"], SendMail.fail_text)
                return

            # 如果当前本地时间或服务器时间有一个超过了预设抢购时间，则开始抢购
            if (now_time > self.set_time) or (server_time > self.set_time):
                # self.logger.info(now_time + "开始秒杀")
                while True:
                    try:
                        # 在页面内寻找结算元素，若找到则点击
                        if self.browser.find_element_by_link_text("去结算"):
                            self.browser.find_element_by_link_text("去结算").click()
                            print("[{}][{}] <---------------结算成功，等待提交订单--------------->".format(now_time, server_time))
                            # 将结算成功记录记入日志
                            self.logger.info(now_time + "商品结算成功!")
                            # 调用自动提交订单函数
                            if self.auto_submit():
                                return
                    except:
                        pass

    # 页面跳转太慢了，此处从结算到提交订单是最大的时间损耗点
    def auto_submit(self):
        """自动提交订单"""
        while True:
            try:
                # 在页面内寻找提交订单元素，若找到则点击
                if self.browser.find_element_by_id("order-submit"):
                    self.browser.find_element_by_id("order-submit").click()
                    # 抢购成功，则打印成功信息
                    print("[{}][{}] <---------------抢购成功，请尽快付款--------------->".format(time_func.get_datetime(),
                                                                                       time_func.get_tb_server_time()))
                    # 将成功记录记入日志
                    self.logger.info(time_func.get_datetime() + "<---商品抢购成功!--->")
                    # 弹窗提示成功
                    PopupWindow.UiMainWindow(message=PopupWindow.success_message)
                    # 发邮件提示成功
                    if self.email:
                        SendMail.SendEmail(self.email, SendMail.platform_list["jingdong"], SendMail.success_text)
                    return True
            except:
                print("再次尝试提交订单")
