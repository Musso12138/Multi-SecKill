from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import Src.time_func as time_func
import Src.taobao_buy as taobao_buy
import Src.tianmao_buy as tianmao_buy
import threading
from Src.MyLib.RoundShadowWidget import RoundShadow


class UiMainWindow(RoundShadow, QWidget):
    """秒杀主窗口"""

    def __init__(self, parent=None):
        self.platform = "taobao"
        self.method = 0
        self.id = "tb189084993"
        self.goods_url = ""
        super(UiMainWindow, self).__init__(parent)
        self.resize(1000, 700)

        # 淘宝用户名输入
        self.lineEdit_id = QLineEdit(self)
        self.lineEdit_id.setObjectName("lineEdit")
        self.lineEdit_id.setGeometry(QRect(200, 385, 150, 50))
        self.lineEdit_id.setFont(QFont("幼圆", 11))
        self.lineEdit_id.setPlaceholderText("请输入用户名")
        self.lineEdit_id.setStyleSheet("background-color: rgb(255, 255, 255);"
                                       "border-radius:4px;")
        self.lineEdit_id.textChanged.connect(self.lineEditChange)

        # 购物平台选择框
        self.comboBox_platform = QComboBox(self)
        self.comboBox_platform.setGeometry(QRect(200, 445, 200, 50))
        # self.comboBox_platform.setStyleSheet("border-color: rgb(255, 255, 255);")
        self.comboBox_platform.setObjectName("comboBox")
        self.comboBox_platform.setPlaceholderText("请选择购物平台")
        self.comboBox_platform.addItem("淘宝")
        self.comboBox_platform.addItem("天猫")
        # 优化ComboBox样式
        self.comboBox_platform.setStyleSheet("border-color: rgb(0,0,0);"
                                             "selection-background-color: rgb(178, 178, 178);"  # 选中项背景色
                                             "selection-color: rgb(0, 0, 0);"  # 选中项文字颜色
                                             "background: white;"  # combobox背景色
                                             "border: 1px solid gray;"  # 边框宽度、颜色
                                             "border-radius: 3px;")
        self.comboBox_platform.setFont(QFont("幼圆", 12))
        self.comboBox_platform.setAttribute(Qt.WA_TranslucentBackground)
        self.comboBox_platform.setWindowFlags(Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.comboBox_platform.currentIndexChanged.connect(self.platformchange)

        # 购物模式选择框
        self.comboBox_mod = QComboBox(self)
        self.comboBox_mod.setGeometry(QRect(450, 445, 350, 50))
        self.comboBox_mod.setStyleSheet("selection-background-color: rgb(178, 178, 178);"  # 选中项背景色
                                        "selection-color: rgb(0, 0, 0);"  # 选中项文字颜色
                                        "background: white;"  # combobox背景色
                                        "border: 1px solid gray;"  # 边框宽度、颜色
                                        "border-radius: 3px;")
        self.comboBox_mod.setObjectName("comboBox")
        self.comboBox_mod.setPlaceholderText("请选择秒杀模式")
        self.comboBox_mod.addItem("自动全选购物车")
        self.comboBox_mod.addItem("手动选择商品")
        self.comboBox_mod.addItem("手动输入商品链接")
        # self.comboBox_mod.setStyleSheet("background-color: rgb(255, 255, 255);\n"
        #                                 "color: rgb(0, 0, 0);")
        self.comboBox_mod.setFont(QFont("幼圆", 12))
        self.comboBox_mod.currentIndexChanged.connect(self.methodchange)

        # 模式为2时手动输入商品链接框
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setGeometry(QRect(355, 385, 445, 50))
        self.lineEdit.setFont(QFont("幼圆", 11))
        self.lineEdit.setPlaceholderText("请输入商品链接")
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);"
                                    "border-radius:4px;")
        self.lineEdit.setHidden(True)
        self.lineEdit.textChanged.connect(self.lineEditChange)

        # 秒杀时间选择框
        self.dateTimeEdit = QDateTimeEdit(self)
        self.dateTimeEdit.setGeometry(QRect(200, 510, 600, 50))
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.dateTimeEdit.setAccelerated(True)
        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm:ss")
        self.dateTimeEdit.setStyleSheet("background: white;"  # combobox背景色
                                        "border: 1px solid gray;"  # 边框宽度、颜色
                                        "border-radius: 3px;")
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

        # 背景图配置
        # self.formFrame = QtWidgets.QFrame()
        # self.formFrame.setGeometry(QtCore.QRect(0, -1, 540, 411))
        # self.formFrame.setStyleSheet("border-color: rgb(0, 85, 255);\n"
        #                              "background-image: url(images/nike1.jpg);")
        # self.formFrame.setObjectName("formFrame")
        # self.formLayout = QtWidgets.QFormLayout(self.formFrame)
        # self.formLayout.setObjectName("formLayout")

    def platformchange(self):
        """监测购物平台切换"""
        if self.comboBox_platform.currentText() == "淘宝":
            self.platform = "taobao"
        elif self.comboBox_platform.currentText() == "天猫":
            self.platform = "tianmao"

    def methodchange(self):
        """监测购物模式切换"""
        if self.comboBox_mod.currentText() == "自动全选购物车":
            self.method = 0
            self.lineEdit.setHidden(True)
        elif self.comboBox_mod.currentText() == "手动选择商品":
            self.method = 1
            self.lineEdit.setHidden(True)
        elif self.comboBox_mod.currentText() == "手动输入商品链接":
            self.method = 2
            self.lineEdit.setHidden(False)

    def datetimechange(self):
        """监测设定秒杀时间切换"""
        self.set_time = self.dateTimeEdit.text()

    def lineEditChange(self):
        """监测商品链接输入改变"""
        self.goods_url = self.lineEdit.text()

    def miaosha(self):
        print("当前平台: " + self.platform)
        print("当前模式: " + str(self.method))
        print("秒杀时间: " + self.set_time)
        print("秒杀时间: " + self.set_time)
        if self.platform == "taobao":
            # 确定平台后关闭窗口，否则占用资源且无法响应
            self.close()
            taobao_buy.Tb(set_time=self.set_time, method=self.method, tb_id=self.id, goods_url=self.goods_url)
        elif self.platform == "tianmao":
            self.close()
            taobao_buy.Tb(set_time=self.set_time, method=self.method, tb_id=self.id, goods_url=self.goods_url)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = UiMainWindow()
    # t = RoundImage('./Asset/new_icons/close.png')
    t.show()
    app.exec_()
