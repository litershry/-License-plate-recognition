from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import read_pic
import car_color
import numpy as np
import cv2 as cv
class picture(QWidget):
    def __init__(self):
        # 长 6.5 宽 4 图片 长2.9 宽1.8 间距0.2 0.1 车牌定位长2.7 宽0.7 间距0.3 0.1  车牌定位与形态学处理间距0.35  ×20倍
        super(picture, self).__init__()
        self.resize(1300, 780)
        self.setWindowTitle("车牌识别系统")

        self.imgName = 0

        self.img=np.ndarray(())

        self.colors = np.ndarray(())
        
        self.label_1 = QLabel(self)
        self.label_1.setFixedSize(580, 620)
        self.label_1.move(30, 20)
        self.label_1.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )

        self.label_2 = QLabel(self) #车牌定位结果图
        self.label_2.setFixedSize(590,150)
        self.label_2.move(680,20)
        self.label_2.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )

       
        self.label_3 = QLabel(self) #车牌颜色图
        self.label_3.setFixedSize(590,150)
        self.label_3.move(680,230)
        self.label_3.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )

        self.label_4 = QLabel(self) # 汽车类型图
        self.label_4.setFixedSize(200,140)
        self.label_4.move(680,500)
        self.label_4.setStyleSheet("QLabel{background:white;}"
                                  "QLabel{font-size:10px;font-weight:bold;font-family:宋体;}"
                                  )
        self.label_5=QLabel(self)
        self.label_5.setFixedSize(590,150)
        self.label_5.move(900,130)
        self.label_5.setText("车牌定位结果")
        self.label_5.setStyleSheet("QLabel{font-size:24px;color:black;font-weight:bold;font-family:宋体;}")

        self.label_6=QLabel(self)
        self.label_6.setFixedSize(150,70)
        self.label_6.move(245,650)
        self.label_6.setText("车辆照片")
        self.label_6.setStyleSheet("QLabel{font-size:24px;color:black;font-weight:bold;font-family:宋体;}")

        self.label_7=QLabel(self)
        self.label_7.setFixedSize(150,70)
        self.label_7.move(920,375)
        self.label_7.setText("车牌颜色")
        self.label_7.setStyleSheet("QLabel{font-size:24px;color:black;font-weight:bold;font-family:宋体;}")

        self.label_8=QLabel(self)
        self.label_8.setFixedSize(150,70)
        self.label_8.move(732,650)
        self.label_8.setText("车辆类型")
        self.label_8.setStyleSheet("QLabel{font-size:24px;color:black;font-weight:bold;font-family:宋体;}")


        btn_1 = QPushButton(self)
        btn_1.setText("打开图片")
        btn_1.setGeometry(950,550,250,40) #（x坐标，y坐标，宽，高）
        btn_1.clicked.connect(self.openimage)

        btn_2 =QPushButton(self)
        btn_2.setText("车牌检测")
        btn_2.setGeometry(950,620,250,40)
        btn_2.clicked.connect(self.train) #这里添加车牌识别的算法
        btn_2.clicked.connect(self.color)

        btn_3 =QPushButton(self)
        btn_3.setText("退出系统")
        btn_3.setGeometry(950,690,250,40)
        btn_3.clicked.connect(self.onClick_Button) #这里添加关闭pyqt的算法


    def openimage(self): # 打开图片
        self.imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(self.imgName).scaled(self.label_1.width(), self.label_1.height())
        self.label_1.setPixmap(jpg)


    def onClick_Button(self):  # 退出系统
        #获得Button
        sender = self.sender()
        #输出button文本
        print(sender.text())
        app = QApplication.instance()
        #退出应用程序
        app.quit()


    def refreshShow(self):
        # 提取图像的尺寸和通道, 用于将opencv下的image转换成Qimage
        height, width, channel = self.img.shape
        bytesPerLine = 3 * width
        self.qImg = QImage(self.img.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
 
        # 将Qimage显示出来
        self.label_2.setPixmap(QPixmap.fromImage(self.qImg))


    def train(self):

        self.img =read_pic.rec_car(self.imgName)

        self.refreshShow()


      
    def color(self):
        self.colors = car_color.color(self.img)
        
        if (self.colors == 'blue'):
            QtWidgets.QApplication.processEvents()
            self.label_3.setStyleSheet("QLabel{background:blue;}"
                                 "QLabel{font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )
            self.label_4.setText("一般类别车")
            self.label_4.setStyleSheet("QLabel{font-size:40px;color:blue;font-weight:bold;font-family:宋体;}")
        elif (self.colors == 'yellow'):
            QtWidgets.QApplication.processEvents()
            self.label_3.setStyleSheet("QLabel{background:yellow;}"
                                 "QLabel{font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )
            self.label_4.setText("特殊用途车")
            self.label_4.setStyleSheet("QLabel{font-size:40px;color:yellow;font-weight:bold;font-family:宋体;}")
        elif (self.colors == 'green'):
            QtWidgets.QApplication.processEvents()
            self.label_3.setStyleSheet("QLabel{background:green;}"
                                 "QLabel{font-size:10px;font-weight:bold;font-family:宋体;}"
                                 )
            self.label_4.setText("新能源汽车")
            self.label_4.setStyleSheet("QLabel{font-size:40px;color:green;font-weight:bold;font-family:宋体;}")
