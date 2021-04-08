import smtplib  # smtplib 用于邮件的发信动作
from email.mime.text import MIMEText  # email 用于构建邮件内容
from email.header import Header  # 用于构建邮件头

platform_list = {
    "taobao": "淘宝",
    "tianmao": "天猫",
    "jingdong": "京东",
}
success_text = "抢购成功，请及时付款完成订单"
fail_text = "抢购失败，感谢您的使用"


# 邮件tool
class SendEmail:
    def __init__(self, to_addr, platform, text):
        """
        :param to_addr: 接收方邮箱
        :param text: 邮件内容
        """
        # 发送方邮箱
        self.from_addr = "13122305203@163.com"  # 发信邮箱
        self.password = "EMRQEFRAHYFVPOPQ"  # 网易邮箱smtp授权码
        self.to_addr = to_addr  # 收信方邮箱
        self.smtp_server = "smtp.163.com"  # 发信服务器
        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        self.msg = MIMEText(platform + text, "plain", "utf-8")
        # 邮件头信息，分别为发件人、收件人、主题
        self.msg['From'] = Header(self.from_addr)
        self.msg['To'] = Header(self.to_addr)
        self.msg['Subject'] = Header("秒杀结果通知")
        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP()
        server.connect(self.smtp_server)
        # set_debuglevel 开启时显示所有 smtp 交互信息
        # server.set_debuglevel(1)
        # 登录发信邮箱
        server.login(self.from_addr, self.password)
        # 发送邮件
        server.sendmail(self.from_addr, self.to_addr, self.msg.as_string())
        # 关闭服务器
        server.quit()


if __name__ == "__main__":
    SendEmail("2020832585@qq.com", success_text)
