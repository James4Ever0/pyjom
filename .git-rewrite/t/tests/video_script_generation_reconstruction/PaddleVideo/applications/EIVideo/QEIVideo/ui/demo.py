# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/zhanghongji/PycharmProjects/EIVideo/resources/QT/demo.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 486)
        MainWindow.setMinimumSize(QtCore.QSize(800, 486))
        MainWindow.setMaximumSize(QtCore.QSize(800, 486))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.video_frame = QtWidgets.QFrame(self.centralwidget)
        self.video_frame.setGeometry(QtCore.QRect(20, 20, 761, 361))
        self.video_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.video_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.video_frame.setObjectName("video_frame")
        self.graphicsView = QtWidgets.QGraphicsView(self.video_frame)
        self.graphicsView.setGeometry(QtCore.QRect(0, 0, 761, 321))
        self.graphicsView.setObjectName("graphicsView")
        self.frame_2 = QtWidgets.QFrame(self.video_frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 320, 761, 41))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.frame_2)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 761, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.open_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.open_btn.setObjectName("open_btn")
        self.horizontalLayout.addWidget(self.open_btn)
        self.save_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.save_btn.setObjectName("save_btn")
        self.horizontalLayout.addWidget(self.save_btn)
        self.horizontalSlider = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.select_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.select_btn.setObjectName("select_btn")
        self.horizontalLayout.addWidget(self.select_btn)
        self.clean_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.clean_btn.setObjectName("clean_btn")
        self.horizontalLayout.addWidget(self.clean_btn)
        self.start_btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.start_btn.setObjectName("start_btn")
        self.horizontalLayout.addWidget(self.start_btn)
        self.draw_frame = QtWidgets.QFrame(self.video_frame)
        self.draw_frame.setGeometry(QtCore.QRect(0, 10, 751, 301))
        self.draw_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.draw_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.draw_frame.setObjectName("draw_frame")
        self.menu_tab = QtWidgets.QTabWidget(self.centralwidget)
        self.menu_tab.setGeometry(QtCore.QRect(20, 380, 761, 81))
        self.menu_tab.setObjectName("menu_tab")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.act_label = QtWidgets.QLabel(self.tab)
        self.act_label.setEnabled(True)
        self.act_label.setGeometry(QtCore.QRect(10, 30, 71, 21))
        self.act_label.setObjectName("act_label")
        self.act_info_label = QtWidgets.QLabel(self.tab)
        self.act_info_label.setEnabled(True)
        self.act_info_label.setGeometry(QtCore.QRect(80, 30, 81, 21))
        self.act_info_label.setObjectName("act_info_label")
        self.act_progressbar = QtWidgets.QProgressBar(self.tab)
        self.act_progressbar.setGeometry(QtCore.QRect(170, 32, 521, 21))
        self.act_progressbar.setProperty("value", 24)
        self.act_progressbar.setObjectName("act_progressbar")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setEnabled(True)
        self.label_3.setGeometry(QtCore.QRect(680, 30, 60, 21))
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.menu_tab.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.menu_tab.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.menu_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open_btn.setText(_translate("MainWindow", "打开视频"))
        self.save_btn.setText(_translate("MainWindow", "保存标注"))
        self.select_btn.setText(_translate("MainWindow", "选择目标"))
        self.clean_btn.setText(_translate("MainWindow", "清空目标"))
        self.start_btn.setText(_translate("MainWindow", "开始推理"))
        self.act_label.setText(_translate("MainWindow", "当前状态："))
        self.act_info_label.setText(_translate("MainWindow", "-------------"))
        self.label_3.setText(_translate("MainWindow", "12%"))
        self.menu_tab.setTabText(self.menu_tab.indexOf(self.tab), _translate("MainWindow", "状态"))
        self.menu_tab.setTabText(self.menu_tab.indexOf(self.tab_2), _translate("MainWindow", "属性配置"))
