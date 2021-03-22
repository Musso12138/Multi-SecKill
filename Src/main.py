from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import Src.time_func as time_func
import Src.taobao_buy as taobao_buy
import Src.tianmao_buy as tianmao_buy
from Src.MyLib.RoundShadowWidget import RoundShadow


class UiMainWindow(RoundShadow, QWidget):
    """秒杀主窗口"""

    def __init__(self, parent=None):
        self.platform = "taobao"
        self.method = 0
        super(UiMainWindow, self).__init__(parent)
        self.resize(1000, 700)
        # 购物平台选择框
        self.comboBox_platform = QComboBox(self)
        self.comboBox_platform.setGeometry(QRect(200, 390, 200, 50))
        self.comboBox_platform.setStyleSheet("border:none")
        self.comboBox_platform.setObjectName("comboBox")
        self.comboBox_platform.addItem("淘宝")
        self.comboBox_platform.addItem("天猫")
        self.comboBox_platform.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                             "color: rgb(0, 0, 0);")
        self.comboBox_platform.setFont(QFont("幼圆", 13))
        self.comboBox_platform.setAttribute(Qt.WA_TranslucentBackground)
        # self.comboBox_platform.setView("border-radius:4px;")
        self.comboBox_platform.setWindowFlags(Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.comboBox_platform.currentIndexChanged.connect(self.platformchange)

        # 购物模式选择框
        self.comboBox_mod = QComboBox(self)
        self.comboBox_mod.setGeometry(QRect(500, 390, 300, 50))
        self.comboBox_mod.setStyleSheet("border:none")
        self.comboBox_mod.setObjectName("comboBox")
        self.comboBox_mod.addItem("自动全选购物车")
        self.comboBox_mod.addItem("手动选择商品")
        self.comboBox_mod.addItem("手动输入商品链接")
        self.comboBox_mod.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                        "color: rgb(0, 0, 0);")
        self.comboBox_mod.setFont(QFont("幼圆", 13))
        self.comboBox_mod.currentIndexChanged.connect(self.methodchange)

        # 模式为2时手动输入商品链接框
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setGeometry(QRect(200, 510, 600, 50))
        self.lineEdit.setFont(QFont("幼圆", 11))
        self.lineEdit.setPlaceholderText("请输入商品链接")
        self.lineEdit.setStyleSheet("border:none")
        self.lineEdit.setReadOnly(True)
        self.lineEdit.textChanged.connect(self.lineEditChange)

        # 秒杀时间选择框
        self.dateTimeEdit = QDateTimeEdit(self)
        self.dateTimeEdit.setGeometry(QRect(200, 450, 600, 50))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.dateTimeEdit.setStyleSheet("border:none")
        # self.dateTimeEdit.setFont(QtGui.QFont("", 11))
        self.dateTimeEdit.setAccelerated(True)
        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                        "color: rgb(0, 0, 0);")
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
        self.pushButton.setStyleSheet("border-radius:50px")
        self.pushButton.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                      "color: rgb(255, 255, 255);")
        self.pushButton.setFont(QFont("微软雅黑 Light", 10))
        self.pushButton.setText("开始秒杀")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.miaosha)

        # 背景图配置
        # self.formFrame = QtWidgets.QFrame()
        # self.formFrame.setGeometry(QtCore.QRect(0, -1, 540, 411))
        # self.formFrame.setStyleSheet("border-color: rgb(0, 85, 255);\n"
        #                              "background-image: url(images/nike1.jpg);")
        # self.formFrame.setObjectName("formFrame")
        # self.formLayout = QtWidgets.QFormLayout(self.formFrame)
        # self.formLayout.setObjectName("formLayout")

    def platformchange(self):
        """购物平台切换"""
        if self.comboBox_platform.currentText() == "淘宝":
            self.platform = "taobao"
        elif self.comboBox_platform.currentText() == "天猫":
            self.platform = "tianmao"

    def methodchange(self):
        """购物模式切换"""
        if self.comboBox_mod.currentText() == "自动全选购物车":
            self.method = 0
            self.lineEdit.setReadOnly(True)
        elif self.comboBox_mod.currentText() == "手动选择商品":
            self.method = 1
            self.lineEdit.setReadOnly(True)
        elif self.comboBox_mod.currentText() == "手动输入商品链接":
            self.method = 2
            self.lineEdit.setReadOnly(False)

    def datetimechange(self):
        """秒杀时间切换"""
        self.set_time = self.dateTimeEdit.text()

    def lineEditChange(self):
        """商品链接输入改变"""
        self.goods_url = self.lineEdit.text()

    def miaosha(self):
        print("当前平台: " + self.platform)
        print("当前模式: " + str(self.method))
        print("秒杀时间: " + self.set_time)
        if self.platform == "taobao":
            taobao_buy.Tb(goods_url=self.goods_url, set_time=self.set_time, method=self.method)
        elif self.platform == "tianmao":
            taobao_buy.Tb(goods_url=self.goods_url, set_time=self.set_time, method=self.method)

        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = UiMainWindow()
    # t = RoundImage('./Asset/new_icons/close.png')
    t.show()
    app.exec_()
