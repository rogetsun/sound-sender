# Form implementation generated from reading ui file 'uvmainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 727)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(900, 665))
        MainWindow.setMaximumSize(QtCore.QSize(900, 11111))
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(1, 1))
        self.centralwidget.setMaximumSize(QtCore.QSize(11111111, 11111111))
        self.centralwidget.setObjectName("centralwidget")
        self.line_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(0, 190, 901, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")
        self.groupBox1 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox1.setGeometry(QtCore.QRect(11, 11, 881, 90))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox1.sizePolicy().hasHeightForWidth())
        self.groupBox1.setSizePolicy(sizePolicy)
        self.groupBox1.setAutoFillBackground(True)
        self.groupBox1.setObjectName("groupBox1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comBox = QtWidgets.QComboBox(parent=self.groupBox1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comBox.sizePolicy().hasHeightForWidth())
        self.comBox.setSizePolicy(sizePolicy)
        self.comBox.setObjectName("comBox")
        self.comBox.addItem("")
        self.comBox.addItem("")
        self.comBox.addItem("")
        self.comBox.addItem("")
        self.comBox.addItem("")
        self.comBox.addItem("")
        self.comBox.addItem("")
        self.comBox.addItem("")
        self.comBox.addItem("")
        self.comBox.addItem("")
        self.comBox.addItem("")
        self.comBox.addItem("")
        self.horizontalLayout.addWidget(self.comBox)
        self.freshCom = QtWidgets.QPushButton(parent=self.groupBox1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.freshCom.sizePolicy().hasHeightForWidth())
        self.freshCom.setSizePolicy(sizePolicy)
        self.freshCom.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.freshCom.setObjectName("freshCom")
        self.horizontalLayout.addWidget(self.freshCom)
        self.serialOptBtn = QtWidgets.QPushButton(parent=self.groupBox1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serialOptBtn.sizePolicy().hasHeightForWidth())
        self.serialOptBtn.setSizePolicy(sizePolicy)
        self.serialOptBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.serialOptBtn.setObjectName("serialOptBtn")
        self.horizontalLayout.addWidget(self.serialOptBtn)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.groupBox1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(60, 60))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.baudrateBox = QtWidgets.QComboBox(parent=self.groupBox1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.baudrateBox.sizePolicy().hasHeightForWidth())
        self.baudrateBox.setSizePolicy(sizePolicy)
        self.baudrateBox.setObjectName("baudrateBox")
        self.baudrateBox.addItem("")
        self.baudrateBox.addItem("")
        self.baudrateBox.addItem("")
        self.baudrateBox.addItem("")
        self.baudrateBox.addItem("")
        self.gridLayout.addWidget(self.baudrateBox, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.groupBox1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMaximumSize(QtCore.QSize(60, 60))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout)
        self.groupBox2 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox2.setGeometry(QtCore.QRect(11, 107, 881, 71))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox2.sizePolicy().hasHeightForWidth())
        self.groupBox2.setSizePolicy(sizePolicy)
        self.groupBox2.setAutoFillBackground(True)
        self.groupBox2.setObjectName("groupBox2")
        self.layoutWidget = QtWidgets.QWidget(parent=self.groupBox2)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 861, 26))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.wmaFileTxt = QtWidgets.QLabel(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wmaFileTxt.sizePolicy().hasHeightForWidth())
        self.wmaFileTxt.setSizePolicy(sizePolicy)
        self.wmaFileTxt.setObjectName("wmaFileTxt")
        self.gridLayout_2.addWidget(self.wmaFileTxt, 0, 1, 1, 1)
        self.wmaFileButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wmaFileButton.sizePolicy().hasHeightForWidth())
        self.wmaFileButton.setSizePolicy(sizePolicy)
        self.wmaFileButton.setMinimumSize(QtCore.QSize(108, 0))
        self.wmaFileButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.wmaFileButton.setMouseTracking(False)
        self.wmaFileButton.setTabletTracking(False)
        self.wmaFileButton.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.wmaFileButton.setAutoFillBackground(False)
        self.wmaFileButton.setObjectName("wmaFileButton")
        self.gridLayout_2.addWidget(self.wmaFileButton, 0, 0, 1, 1)
        self.recordBtn = QtWidgets.QPushButton(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.recordBtn.sizePolicy().hasHeightForWidth())
        self.recordBtn.setSizePolicy(sizePolicy)
        self.recordBtn.setObjectName("recordBtn")
        self.gridLayout_2.addWidget(self.recordBtn, 0, 2, 1, 1)
        self.listLog = QtWidgets.QListWidget(parent=self.centralwidget)
        self.listLog.setGeometry(QtCore.QRect(0, 250, 901, 451))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listLog.sizePolicy().hasHeightForWidth())
        self.listLog.setSizePolicy(sizePolicy)
        self.listLog.setMaximumSize(QtCore.QSize(16777215, 16666666))
        self.listLog.setAutoFillBackground(False)
        self.listLog.setObjectName("listLog")
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 210, 200, 26))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(parent=self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.sendDurationBox = QtWidgets.QComboBox(parent=self.layoutWidget1)
        self.sendDurationBox.setObjectName("sendDurationBox")
        self.sendDurationBox.addItem("")
        self.sendDurationBox.addItem("")
        self.sendDurationBox.addItem("")
        self.sendDurationBox.addItem("")
        self.sendDurationBox.addItem("")
        self.sendDurationBox.addItem("")
        self.sendDurationBox.addItem("")
        self.horizontalLayout_3.addWidget(self.sendDurationBox)
        self.sendButton = QtWidgets.QPushButton(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sendButton.sizePolicy().hasHeightForWidth())
        self.sendButton.setSizePolicy(sizePolicy)
        self.sendButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.sendButton.setMouseTracking(False)
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout_3.addWidget(self.sendButton)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox1.setTitle(_translate("MainWindow", "串口设置"))
        self.comBox.setItemText(0, _translate("MainWindow", "COM1"))
        self.comBox.setItemText(1, _translate("MainWindow", "COM2"))
        self.comBox.setItemText(2, _translate("MainWindow", "COM3"))
        self.comBox.setItemText(3, _translate("MainWindow", "COM4"))
        self.comBox.setItemText(4, _translate("MainWindow", "COM5"))
        self.comBox.setItemText(5, _translate("MainWindow", "COM6"))
        self.comBox.setItemText(6, _translate("MainWindow", "COM7"))
        self.comBox.setItemText(7, _translate("MainWindow", "COM8"))
        self.comBox.setItemText(8, _translate("MainWindow", "COM9"))
        self.comBox.setItemText(9, _translate("MainWindow", "COM10"))
        self.comBox.setItemText(10, _translate("MainWindow", "COM11"))
        self.comBox.setItemText(11, _translate("MainWindow", "COM12"))
        self.freshCom.setText(_translate("MainWindow", "刷新串口列表"))
        self.serialOptBtn.setText(_translate("MainWindow", "打开串口"))
        self.label.setText(_translate("MainWindow", "波特率"))
        self.baudrateBox.setCurrentText(_translate("MainWindow", "9600"))
        self.baudrateBox.setItemText(0, _translate("MainWindow", "9600"))
        self.baudrateBox.setItemText(1, _translate("MainWindow", "19200"))
        self.baudrateBox.setItemText(2, _translate("MainWindow", "38400"))
        self.baudrateBox.setItemText(3, _translate("MainWindow", "57600"))
        self.baudrateBox.setItemText(4, _translate("MainWindow", "115200"))
        self.label_2.setText(_translate("MainWindow", "COM口"))
        self.groupBox2.setTitle(_translate("MainWindow", "音频"))
        self.wmaFileTxt.setText(_translate("MainWindow", "请选择WAV/WMA/MP3音频文件"))
        self.wmaFileButton.setText(_translate("MainWindow", "选择音频文件"))
        self.recordBtn.setText(_translate("MainWindow", "录制音频"))
        self.label_3.setText(_translate("MainWindow", "发送间隔"))
        self.sendDurationBox.setItemText(0, _translate("MainWindow", "1ms"))
        self.sendDurationBox.setItemText(1, _translate("MainWindow", "5ms"))
        self.sendDurationBox.setItemText(2, _translate("MainWindow", "10ms"))
        self.sendDurationBox.setItemText(3, _translate("MainWindow", "15ms"))
        self.sendDurationBox.setItemText(4, _translate("MainWindow", "20ms"))
        self.sendDurationBox.setItemText(5, _translate("MainWindow", "50ms"))
        self.sendDurationBox.setItemText(6, _translate("MainWindow", "100ms"))
        self.sendButton.setText(_translate("MainWindow", "开始发送"))
