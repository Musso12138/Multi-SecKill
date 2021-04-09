from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import Src.MyTools.time_func as time_func
import Src.BuyModes.taobao_buy as taobao_buy
import Src.BuyModes.tianmao_buy as tianmao_buy
import Src.BuyModes.jd_buy as jd_buy
from Src.MyTools.RoundShadowWidget import RoundShadow


class UiMainWindow(RoundShadow, QWidget):
    """秒杀主窗口"""

    def __init__(self, parent=None):
        self.email = ""  # 用户收件邮箱
        self.platform = ""  # 抢购平台
        self.method = -1  # 抢购模式，默认为0，自动全选购物车
        self.id = "tb189084993"  # 平台用户名
        self.goods_url = ""  # 手动输入商品链接模式下，输入的商品链接
        super(UiMainWindow, self).__init__(parent)
        self.resize(1000, 700)  # 主界面大小

        # 反馈邮箱输入框
        self.lineEdit_email = QLineEdit(self)
        self.lineEdit_email.setObjectName("lineEdit")
        self.lineEdit_email.setGeometry(QRect(200, 330, 600, 50))
        self.lineEdit_email.setFont(QFont("幼圆", 11))
        self.lineEdit_email.setPlaceholderText("请输入接收邮箱（非必填，用于接收抢购结果通知）")
        self.lineEdit_email.setStyleSheet("background-color: rgb(255, 255, 255);"
                                          "border-radius:4px;")
        self.lineEdit_email.textChanged.connect(self.lineEditEmailChange)

        # 购物平台用户名输入框
        self.lineEdit_id = QLineEdit(self)
        self.lineEdit_id.setObjectName("lineEdit")
        self.lineEdit_id.setGeometry(QRect(200, 385, 200, 50))
        self.lineEdit_id.setFont(QFont("幼圆", 11))
        self.lineEdit_id.setPlaceholderText("请输入购物网站用户名")
        self.lineEdit_id.setStyleSheet("background-color: rgb(255, 255, 255);"
                                       "border-radius:4px;")
        self.lineEdit_id.textChanged.connect(self.lineEditIdChange)

        # 购物平台选择框
        self.comboBox_platform = QComboBox(self)
        self.comboBox_platform.setGeometry(QRect(200, 445, 200, 50))
        self.comboBox_platform.setObjectName("comboBox")
        self.comboBox_platform.setPlaceholderText("请选择购物平台")
        self.comboBox_platform.addItem("淘宝")
        self.comboBox_platform.addItem("天猫")
        self.comboBox_platform.addItem("京东")
        # 优化ComboBox样式
        self.comboBox_platform.setStyleSheet("QComboBox{"
                                             "border-color: rgb(158,158,158);"
                                             "background: white;"  # combobox背景色
                                             "border: 1px solid gray;"  # 边框宽度、颜色
                                             "border-radius: 3px;}"
                                             "QComboBox::drop-down{"
                                             "border: none;}"
                                             "QComboBox::down-arrow{"
                                             "image: url(./images/down_arrow.png);}"
                                             "QComboBox QAbstractItemView::item{"
                                             "height: 100px;"
                                             "background-color: rgb(0,0,0);}"
                                             "QComboBox QAbstractItemView{"
                                             "selection-background-color: rgb(64, 156, 255);"  # 选中项背景色
                                             "selection-color: rgb(255, 255, 255);"  # 选中项文字颜色"
                                             "background: rgb(255,255,255);"  # 下拉框背景色
                                             "border: 1px solid rgb(158,158,158);"  # 下拉框边框宽度及颜色
                                             "border-radius: 0px 0px 5px 5px;"
                                             "outline: 0px;}")  # 去选中项虚线
        self.comboBox_platform.setFont(QFont("幼圆", 12))
        self.comboBox_platform.setAttribute(Qt.WA_TranslucentBackground)
        self.comboBox_platform.setWindowFlags(Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.comboBox_platform.currentIndexChanged.connect(self.platformchange)

        # 购物模式选择框
        self.comboBox_mod = QComboBox(self)
        self.comboBox_mod.setGeometry(QRect(450, 445, 350, 50))
        self.comboBox_mod.setStyleSheet("QComboBox{"
                                        "border-color: rgb(158,158,158);"
                                        "background: white;"  # combobox背景色
                                        "border: 1px solid gray;"  # 边框宽度、颜色
                                        "border-radius: 3px;}"
                                        "QComboBox::drop-down{"
                                        "border: none;}"
                                        "QComboBox::down-arrow{"
                                        "image: url(./images/down_arrow.png);}"
                                        "QComboBox QAbstractItemView::item{"
                                        "height: 100px;"
                                        "background-color: rgb(0,0,0);}"
                                        "QComboBox QAbstractItemView{"
                                        "selection-background-color: rgb(64, 156, 255);"  # 选中项背景色
                                        "selection-color: rgb(255, 255, 255);"  # 选中项文字颜色"
                                        "background: rgb(255,255,255);"  # 下拉框背景色
                                        "border: 1px solid rgb(158,158,158);"  # 下拉框边框宽度及颜色
                                        "border-radius: 0px 0px 5px 5px;"
                                        "outline: 0px;}")  # 去选中项虚线
        self.comboBox_mod.setObjectName("comboBox")
        self.comboBox_mod.setPlaceholderText("请选择秒杀模式")
        self.comboBox_mod.addItem("自动全选购物车")
        self.comboBox_mod.addItem("手动选择购物车内商品")
        self.comboBox_mod.addItem("手动输入商品链接")
        self.comboBox_mod.setFont(QFont("幼圆", 12))
        self.comboBox_mod.currentIndexChanged.connect(self.methodchange)

        # 模式为2时手动输入商品链接框
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setGeometry(QRect(405, 385, 395, 50))
        self.lineEdit.setFont(QFont("幼圆", 11))
        self.lineEdit.setPlaceholderText("请输入商品链接")
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);"
                                    "border-radius:4px;")
        # 默认method为0，所以
        self.lineEdit.setHidden(True)
        self.lineEdit.textChanged.connect(self.lineEditUrlChange)

        # 秒杀时间选择框
        self.dateTimeEdit = QDateTimeEdit(self)
        self.dateTimeEdit.setGeometry(QRect(200, 510, 600, 50))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.dateTimeEdit.setAccelerated(True)
        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit.setStyleSheet("QDateTimeEdit{"
                                        "border-color: rgb(158,158,158);"
                                        "background: white;"
                                        "border: 1px solid gray;"  # 边框宽度、颜色
                                        "border-radius: 3px;}"
                                        "QDateTimeEdit::up-button{"
                                        "image: url(./images/datetime_add.png);}"
                                        "QDateTimeEdit::down-button{"
                                        "image: url(./images/datetime_reduce.png);}")
        self.dateTimeEdit.setFont(QFont("幼圆", 14))
        # 设置最小日期时间为当前时间
        l_t = time_func.get_time()
        # 默认时间为距离当前时间最近的10min的倍数
        t = [int(l_t[0:4]), int(l_t[5:7]), int(l_t[8:10]), int(l_t[11:13]), int(l_t[14:16]), int(l_t[17:19])]
        if t[4] // 10 == 5:
            if t[3] == 23:
                t[3] = 0
                t[4] = 0
            else:
                t[3] += 1
                t[4] = 0
        else:
            t[4] = (t[4] // 10 + 1) * 10
        self.dateTimeEdit.setDateTime(QDateTime(QDate(t[0], t[1], t[2]),
                                                QTime(t[3], t[4], 0)))
        self.set_time = self.dateTimeEdit.text()
        self.dateTimeEdit.setCurrentSection(QDateTimeEdit.MinuteSection)
        self.dateTimeEdit.dateTimeChanged.connect(self.datetimechange)
        # self.dateTimeEdit.setCalendarPopup(True)  # 弹出日历选择日期，时间无法使用键头调整

        # 按钮
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QRect(200, 580, 600, 60))
        self.pushButton.setStyleSheet("background-color: rgb(65, 205, 82);\n"
                                      "color: rgb(255, 255, 255);"
                                      "border-radius:10px;")
        self.pushButton.setFont(QFont("华文中宋", 16))
        self.pushButton.setText("开 始 秒 杀")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.miaosha)

    def platformchange(self):
        """监测购物平台切换"""
        if self.comboBox_platform.currentText() == "淘宝":
            self.platform = "taobao"
        elif self.comboBox_platform.currentText() == "天猫":
            self.platform = "tianmao"
        elif self.comboBox_platform.currentText() == "京东":
            self.platform = "jingdong"

    def methodchange(self):
        """监测购物模式切换"""
        if self.comboBox_mod.currentText() == "自动全选购物车":
            self.method = 0
            self.lineEdit.setHidden(True)
        elif self.comboBox_mod.currentText() == "手动选择购物车内商品":
            self.method = 1
            self.lineEdit.setHidden(True)
        elif self.comboBox_mod.currentText() == "手动输入商品链接":
            self.method = 2
            # 只有method为2时才显示链接输入框
            self.lineEdit.setHidden(False)

    def datetimechange(self):
        """监测设定秒杀时间切换"""
        self.set_time = self.dateTimeEdit.text()

    def lineEditEmailChange(self):
        """监测邮箱输入改变"""
        self.email = self.lineEdit_email.text()

    def lineEditIdChange(self):
        """监测用户名输入改变"""
        self.id = self.lineEdit_id.text()

    def lineEditUrlChange(self):
        """监测商品链接输入改变"""
        self.goods_url = self.lineEdit.text()

    def miaosha(self):
        if self.platform and self.method != -1:
            if self.method != 2 or (self.method == 2 and "https:" in self.goods_url):
                print("当前平台: " + self.platform)
                print("当前模式: " + str(self.method))
                print("秒杀时间: " + self.set_time)
                print("秒杀时间: " + self.set_time)
                if self.platform == "taobao":
                    # 确定平台后关闭窗口，否则占用资源且无法响应
                    self.close()
                    taobao_buy.Tb(set_time=self.set_time, method=self.method, tb_id=self.id, goods_url=self.goods_url, email=self.email)
                elif self.platform == "tianmao":
                    self.close()
                    tianmao_buy.Tm(set_time=self.set_time, method=self.method, tm_id=self.id, goods_url=self.goods_url, email=self.email)
                elif self.platform == "jingdong":
                    self.close()
                    jd_buy.Jd(set_time=self.set_time, method=self.method, jd_id=self.id, goods_url=self.goods_url, email=self.email)
                return
            else:
                print("请输入抢购网址")
                return
        else:
            print("请选择购物平台和抢购模式")
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = UiMainWindow()
    t.show()
    app.exec_()
