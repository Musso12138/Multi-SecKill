from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from Src.MyTools.RoundShadowWidget import RoundShadow

success_message = "商品抢购成功！"
fail_message = "商品抢购失败."


class UiMainWindow(RoundShadow, QWidget):
    """告示弹窗"""

    def __init__(self, message="", parent=None):
        self.message = message
        super(UiMainWindow, self).__init__(parent)
        self.resize(400, 300)

        # 通知
        self.messageLabel = QLabel(self)
        self.messageLabel.setGeometry(QRect(125, 110, 250, 50))
        self.messageLabel.setStyleSheet("border:none")
        self.messageLabel.setFont(QFont("幼圆", 13))
        self.messageLabel.setText(self.message)

        # 按钮
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QRect(285, 225, 75, 45))
        self.pushButton.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                                      "color: rgb(255, 255, 255);"
                                      "border-radius:4px;")
        self.pushButton.setFont(QFont("华文中宋", 11))
        self.pushButton.setText("确认")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.close_popupwindow)

        self.app = QApplication(sys.argv)
        self.show()

    def close_popupwindow(self):
        self.close()
        self.app.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = UiMainWindow(fail_message)
    # t = RoundImage('./Asset/new_icons/close.png')
    # t.show()
    app.exec_()
