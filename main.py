import time, sys
from ui import ui_tool
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QObject
import serial.tools.list_ports_windows
from ui.uvmainwindow import Ui_MainWindow
import serial
import serial.tools.list_ports
import logging
import logging.config
import os

# 录音
from ui.record_dialog import Ui_Dialog
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import re
import convert

# 获取当前系统的默认字符集
encoding = sys.getfilesystemencoding()
print(f"系统默认字符集：{encoding}")
# 获取配置好的logger
logger = logging.getLogger("myapp")
# 设置日志同时打印到file和console。file打印方式为追加模式，console打印方式为覆盖模式

fileh = logging.FileHandler(
    filename="soundsender.log",
    mode="a",
    encoding=encoding,
    delay=False,
)
fileh.setFormatter(
    logging.Formatter(
        "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
    )
)

logger.addHandler(fileh)

console = logging.StreamHandler()
console.setFormatter(
    logging.Formatter(
        "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
    )
)
logger.addHandler(console)


log_level = logging.DEBUG  # 默认级别

logger.setLevel(log_level)

# 现在你可以使用logger来记录日志了
logger.info("程序启动")
logger.info(f"日志等级：{log_level}")


## SendFileWindow 类继承 Ui_MainWindow 类
## 实现了选择文件按钮的点击事件，以及发送按钮的点击事件
class SendFileWindow(Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        super().setupUi(self.window)
        self.window.setWindowTitle("Sound Sender")
        self.window.show()
        self.wmaFile = None
        self.wmaFileButton.clicked.connect(self.on_select_wma_clicked)
        self.sendButton.clicked.connect(self.sendFile)
        self.freshCom.clicked.connect(self.update_com)
        self.serialOptBtn.clicked.connect(self.optCom)
        # 设置baudrateBox 默认选中115200 ，默认波特率为115200
        self.baudrateBox.setCurrentIndex(self.baudrateBox.findText("115200"))
        # 设置发送时间间隔 默认选中10ms
        self.sendDurationBox.setCurrentIndex(self.sendDurationBox.findText("10ms"))
        self.listLog.clear()
        self.statusbar.showMessage("Ready")
        self.available_ports = []
        self.available_ports_json = {}
        # 给available_ports 添加从1到16个COM口字典信息{"port":"COM1"}
        for i in range(1, 25):
            port = {"port": f"COM{i}", "desc": "", "hwid": ""}
            self.available_ports.append(port)
            self.available_ports_json[f"COM{i}"] = port
        self.update_com()

        # 串口连接对象
        self.ser = None
        self.print("软件虚拟的串口，刚创建完，需要重启电脑才能获取。")

        # 录音窗口Ui_Dialog初始化
        self.record_dialog = QDialog()
        self.record_dialog_ui = Ui_Dialog()

        self.record_dialog_ui.setupUi(self.record_dialog)
        self.recordBtn.clicked.connect(self.show_record_dialog)

        # 按钮事件信号处理
        self.record_dialog_ui.recCancalBtn.clicked.connect(self.record_dialog.close)
        self.record_dialog_ui.recSaveBtn.clicked.connect(self.saveRecord)
        self.record_dialog_ui.recResetBtn.clicked.connect(self.reset_record)

        self.record_dialog_ui.startRecordBtn.clicked.connect(self.startRecord)
        self.record_dialog_ui.stopRecordBtn.clicked.connect(self.stopRecord)
        self.record_dialog_ui.playRecordBtn.clicked.connect(self.play_record_wav)

        # 声音放大silder处理
        def wav_large_silder_changed(value):
            self.record_dialog_ui.wavLargeInput.setText(f"{value}")

        # 声音放大input处理，让silder和input同步
        def wav_large_input_changed(value):

            # value 是用户输入的，有可能是100，有可能是100%，我要拿到int_value是100,str_value是100%，
            # 用正则表达式，现拿到用户输入的纯数字，过滤掉非数字字符
            pattern = re.compile(r"[^\d]+")
            str_value = pattern.sub("", value)
            int_value = int(str_value)
            # 处理完后，int_value 就是用户输入的纯数字，可以用来设置wav_large_silder的值
            self.record_dialog_ui.wavLargeSilder.setValue(int_value)
            self.record_dialog_ui.wavLargeInput.setText(str_value)

        self.record_dialog_ui.wavLargeSilder.valueChanged.connect(
            wav_large_silder_changed
        )

        # 窗口icon处理

        self.window.setWindowIcon(ui_tool.base64_to_icon(ui_tool.S_PNG_BASE64))
        self.record_dialog.setWindowIcon(ui_tool.base64_to_icon(ui_tool.S_PNG_BASE64))

        # 清空录音音频数据
        self.record_wav_data = None

    def show_record_dialog(self):
        # sd 获取音频设备
        self.reset_record()
        self.refresh_sound_device()
        self.record_dialog.show()

    # 开始录音, 并生成录制的音频数据到self.record_wav_data
    def startRecord(self):
        self.record_wav_data = np.array([])

        def record_data_info_callback(msg):
            # 设置recInfoLabel 显示录音信息
            self.record_dialog_ui.recInfoLabel.setText(msg)

        self.print("准备开始录音")
        # 使用soundDevice模块录音
        # 获取录音参数
        try:
            sample_rate = self.record_dialog_ui.wavSampleRateComBox.currentText()
            channels = self.record_dialog_ui.wavChannelComBox.currentText()
            device_index = self.record_dialog_ui.wavDeviceListComBox.currentIndex()
            self.print(f"开始录音，采样率：{sample_rate}, 声道：{channels}, 设备索引：{device_index}")
            # 录音线程
            self.record_worker = RecordWorker(
                record_dialog_ui=self.record_dialog_ui,
                log_func=self.print,
                record_data_info_callback=record_data_info_callback,
                sampleRate=int(sample_rate),
                channels=int(channels),
                device_index=device_index,
            )
            self.record_worker.record()
            self.record_dialog_ui.recCancalBtn.setDisabled(False)
            self.record_dialog_ui.recResetBtn.setDisabled(True)
            self.record_dialog_ui.startRecordBtn.setDisabled(True)
            self.record_dialog_ui.stopRecordBtn.setDisabled(False)
            self.record_dialog_ui.playRecordBtn.setDisabled(True)
            self.record_dialog_ui.recParamGroup.setDisabled(True)
        except Exception as e:
            self.print(f"录音失败, 请确定录音设备是否正常，错误信息：{e}")
            self.reset_record()

    # 停止录音，并生成录制的音频数据到self.record_wav_data
    def stopRecord(self):
        self.print("停止录音")
        self.record_wav_data = self.record_worker.stop_recording()
        # 从record_dialog_ui.wavLargeInput 获取当前声音放大倍数

        wav_large_value = self.record_dialog_ui.wavLargeInput.text()
        pattern = re.compile(r"[^\d]+")
        str_value = pattern.sub("", wav_large_value)
        int_value = int(str_value)
        # 把record_wav_data 声音放大2倍
        self.print(F"声音放大倍数：{int_value}%")
        self.record_wav_data = self.record_wav_data * int_value / 100
        self.record_wav_data = np.clip(self.record_wav_data, -1, 1)
        # 显示录音信息
        self.print(f"录音数据生成完成：{self.record_dialog_ui.recInfoLabel.text()}")
        # 播放 录音的音频
        # self.play_record_wav(self.record_wav_data)
        self.record_dialog_ui.recSaveBtn.setDisabled(False)
        self.record_dialog_ui.recCancalBtn.setDisabled(False)
        self.record_dialog_ui.recResetBtn.setDisabled(False)
        self.record_dialog_ui.startRecordBtn.setDisabled(False)
        self.record_dialog_ui.stopRecordBtn.setDisabled(True)
        self.record_dialog_ui.playRecordBtn.setDisabled(False)

    def refresh_sound_device(self):
        devices = sd.query_devices()
        self.record_dialog_ui.wavDeviceListComBox.clear()
        # 填充设备列表
        for device in devices:
            self.record_dialog_ui.wavDeviceListComBox.addItem(device["name"])

    def reset_record(self):
        self.refresh_sound_device()
        self.record_dialog_ui.recSaveBtn.setDisabled(True)
        self.record_dialog_ui.recCancalBtn.setDisabled(False)
        self.record_dialog_ui.recResetBtn.setDisabled(True)
        self.record_dialog_ui.startRecordBtn.setDisabled(False)
        self.record_dialog_ui.stopRecordBtn.setDisabled(True)
        self.record_dialog_ui.playRecordBtn.setDisabled(True)
        self.record_dialog_ui.recParamGroup.setDisabled(False)
        self.record_wav_data = None

    def play_record_wav(self):
        # 使用soundDevice模块播放录音的音频,并获取播放进度时间
        sd.stop()
        sd.play(
            self.record_wav_data,
            int(self.record_dialog_ui.wavSampleRateComBox.currentText())
        )

    def saveRecord(self):
        # 调用QFileDialog保存self.record_wav_data到文件
        fileName, _ = QFileDialog.getSaveFileName(
            None, "Save Recording", "", "WAV Files (*.wav)"
        )
        if fileName:
            try:
                # 保存录音数据到文件
                sd.stop()
                wav_data_int16 = np.int16(self.record_wav_data * 32767)
                wav.write(
                    fileName,
                    int(self.record_dialog_ui.wavSampleRateComBox.currentText()),
                    wav_data_int16,
                )
                # 打印录音WAV文件保存最终信息，并输出文件大小，单位kb
                wav_file_size = os.path.getsize(fileName)
                self.print(
                    f"原始录音文件保存到 {fileName}, 大小：{wav_file_size / 1024:.2f}KB"
                )

                # 判断当前日志等级是否小于等于DEBUG，如果是，则压缩保存WMA格式文件
                if logger.level > logging.DEBUG:
                    self.print("非调试模式，跳过压缩wma格式")
                    pass
                else:
                    # 压缩保存波特率参数
                    audio_bitrate = "24k"
                    # 转换为更小的WMA格式文件
                    wma_file_name = fileName.replace(".wav", ".wma")
                    self.print(
                        f"开始转换 {fileName} 到 {wma_file_name}，audio_bitrate = {audio_bitrate}"
                    )
                    convert.wav_to_wma(
                        fileName,
                        wma_file_name,
                        audio_bitrate=audio_bitrate,
                        log_func=self.print,
                    )
                    # 打印WMA文件保存最终信息，并获取wma文件大小，单位kb，并计算两个文件大小减少了多少百分比
                    self.print(
                        f"转换 {fileName}({wav_file_size/1024:.2f}KB) 到 {wma_file_name}({os.path.getsize(wma_file_name)/1024:.2f}KB) 完成，文件缩小了 {100 - os.path.getsize(wma_file_name)/wav_file_size*100:.2f}%"
                    )

                mp3_file_name = fileName.replace(".wav", ".mp3")
                audio_bitrate = "8k"
                self.print(
                    f"开始转换 {fileName} 到 {mp3_file_name}，audio_bitrate = {audio_bitrate}"
                )
                convert.wav_to_mp3(
                    fileName,
                    mp3_file_name,
                    audio_bitrate=audio_bitrate,
                    log_func=self.print,
                )
                self.print(
                    f"转换 {fileName}({wav_file_size/1024:.2f}KB) 到 {mp3_file_name}({os.path.getsize(mp3_file_name)/1024:.2f}KB) 完成，文件缩小了 {100 - os.path.getsize(mp3_file_name)/wav_file_size*100:.2f}%"
                )
                self.wmaFile = mp3_file_name
                self.wmaFileTxt.setText(mp3_file_name)
                aac_file_name = fileName.replace(".wav", ".aac")
                self.print(
                    f"开始转换 {fileName} 到 {aac_file_name}，audio_bitrate = {audio_bitrate}"
                )
                convert.wav_to_aac(fileName, aac_file_name,audio_bitrate=audio_bitrate, log_func=self.print)
                self.print(
                    f"转换 {fileName}({wav_file_size/1024:.2f}KB) 到 {aac_file_name}({os.path.getsize(aac_file_name)/1024:.2f}KB) 完成，文件缩小了 {100 - os.path.getsize(aac_file_name)/wav_file_size*100:.2f}%"
                )
                self.record_dialog.close()
            except Exception as e:
                # 打印报错详细信息
                self.print(
                    f"录音文件保存失败, 请检查文件路径是否正确，ffmpeg是否安装正确，错误信息：{e}"
                )

    # 获取当前电脑可用串口信息，并先删除combox的旧选项，再添加新的选项
    def update_com(self):
        # 将鼠标样式变为等待样式
        self.setCursorIng()
        # 获取当前电脑可用串口信息，并返回串口信息的字典列表
        available_ports = []
        # available_ports.extend(self.try_to_get_com_name())
        available_ports.extend(self.get_available_ports())
        self.update_com_show(available_ports)
        # 鼠标样式恢复
        self.setCursorArrow()
        self.print("更新串口列表信息完成")

    def update_com_show(self, available_ports=None):
        self.comBox.clear()

        # 根据available_ports 更新self.available_ports_json中对应port的desc 和 hwid信息
        if available_ports is not None:  # 如果available_ports不为空，则更新
            for port in available_ports:
                if port["port"] in self.available_ports_json:
                    self.available_ports_json[port["port"]]["desc"] = port["desc"]
                    self.available_ports_json[port["port"]]["hwid"] = port["hwid"]

        # 添加串口信息到combox
        if self.available_ports is not None:
            for port in self.available_ports:
                self.comBox.addItem(f"{port['port']}: {port['desc']}")

    def try_to_get_com_name(self):
        try_ports = []
        for port in self.available_ports:
            try:
                ser = serial.Serial(port["port"], 9600, timeout=0.5)
                self.print(f"尝试打开了串口 {port['port']}, {ser}")
                if ser.is_open:
                    try_ports.append(
                        {"port": port["port"], "desc": "可连接", "hwid": ""}
                    )
                    ser.close()
            except:
                pass
        return try_ports

    # 获取当前电脑的可用串口信息，并返回串口信息的字典列表
    def get_available_ports(self):
        ports = serial.tools.list_ports_windows.comports()

        available_ports = []
        for port, desc, hwid in sorted(ports):
            # 生成串口信息字典
            available_ports.append({"port": port, "desc": desc, "hwid": hwid})
            self.print(f"{port}: {desc} 【{hwid}】")
        return available_ports

    ## 打开选择文件对话框，用于让用户选择一个wma文件，并返回文件完整路径
    def on_select_wma_clicked(self):
        # 打开文件选择对话框，并获取文件路径，文件只能选择wav或wma格式，如果self.wmaFile不为空，则打开此文件目录
        fileName, _ = QFileDialog.getOpenFileName(
            None,
            "Select WMA/WAV/MP3 File",
            self.wmaFile if self.wmaFile else "/",
            "WAV/WMA/MP3 Files (*.wav *.wma *.mp3)",
        )

        # 检查文件是否被选中
        if fileName:
            self.wmaFile = fileName
            self.wmaFileTxt.setText(fileName)
            self.print(f"Selected file: {fileName}")
            from scipy.io import wavfile
            if fileName.endswith(".wav"):
                rate, data = wavfile.read(fileName)
                self.print(f"wav file rate: {rate}, data shape: {data.shape}")
            
        else:
            self.print("No file selected.")

    def openCom(self):
        ## 串口名称为self.comBox的值
        portIdx = self.comBox.currentIndex()
        port = self.available_ports[portIdx]["port"]
        baudrate = self.baudrateBox.currentText()  # 根据设备要求设置波特率
        self.print(f"串口: {port}, 波特率: {baudrate}")
        # 打开串口
        try:
            ser = serial.Serial(port, baudrate, timeout=1)
            # print ser attr
            # 打印ser的开始位 停止位 校验位 奇偶校验位
            self.print(f"serial.bytesize: {ser.bytesize}")
            self.print(f"serial.stopbits: {ser.stopbits}")
            self.print(f"serial.parity: {ser.parity}")
            self.print(f"serial.xonxoff: {ser.xonxoff}")
            self.print(f"serial.rtscts: {ser.rtscts}")
            self.print(f"serial.dsrdtr: {ser.dsrdtr}")
            self.print(f"serial.inter_byte_timeout: {ser.inter_byte_timeout}")

            self.print(f"serial.name: {ser.name}")
            self.print(f"serial.is_open: {ser.is_open}")
            self.print(f"serial.baudrate: {ser.baudrate}")

            self.print(f"serial.timeout: {ser.timeout}")
            self.print(f"serial.write_timeout: {ser.write_timeout}")
            self.ser = ser

            self.comBox.setDisabled(True)
            self.baudrateBox.setDisabled(True)
            self.serialOptBtn.setText("关闭串口")
            self.freshCom.setDisabled(True)
            self.print(f"串口 {port} 已打开")
            # 设置按钮serialOptBtn样式字体颜色位蓝色
            self.serialOptBtn.setStyleSheet("color: #ab5657")
        except serial.SerialException as e:
            self.print(f"无法打开串口 {port}: {e}")
            return

    def closeCom(self):
        if self.ser is not None and self.ser.is_open:
            self.ser.close()
            self.print(f"关闭串口 {self.ser.name}")
            self.ser = None
            self.comBox.setDisabled(False)
            self.baudrateBox.setDisabled(False)
            self.serialOptBtn.setText("打开串口")
            self.freshCom.setDisabled(False)
            self.serialOptBtn.setStyleSheet("color: #222222")

    def optCom(self):
        if self.ser is not None and self.ser.is_open:
            self.closeCom()
        else:
            self.openCom()

    def stopSendFile(self):
        if hasattr(self, "sender") and self.sender.runThread.isRunning():
            self.sender.stop()
        self.sendButton.setText("开始发送")
        self.sendButton.setStyleSheet("color: #222222")
        self.groupBox2.setDisabled(False)
        return

    def sendFile(self):
        if self.ser is None or not self.ser.is_open:
            self.print("串口未打开，请先选择对应串口打开！")
            return

        # 判断self有sender属性，且在运行中，则停止发送
        if hasattr(self, "sender") and self.sender.runThread.isRunning():
            self.stopSendFile()
            self.print("停止发送")
            return

        # try catch 语句，用于捕获异常，并把异常内容打印出来
        try:
            self.print("send file: ", self.wmaFile)
            if self.wmaFile:
                ## 读取文件内容、计算文件大小、判断是否有文件读取权限
                with open(self.wmaFile, "rb") as f:
                    data = f.read()
                    # 打印文件大小，单位kb，2位小数
                    self.print(f"文件[{f.name}]大小: {len(data) / 1024:.2f} KB")
                    # 获取发送时间间隔 send_duration
                    # self.sendDurationBox.text()为10ms， 用正则表达式取出数字，转换为int
                    send_duration = int(
                        re.findall(r"\d+", self.sendDurationBox.currentText())[0]
                    )

                    # 计算发送数据包的数量，并计算每个数据包的大小
                    # 启动发送线程，开始发送文件，并把文件内容作为参数传递给发送线程
                    self.sender = Sender(
                        self.ser,
                        data,
                        send_duration,
                        self.debug,
                        self.print,
                        self.stopSendFile,
                    )
                    self.sender.start()
                    self.sendButton.setText("停止发送")
                    self.sendButton.setStyleSheet("color: #ab5657")
                    self.groupBox2.setDisabled(True)
            else:
                self.print("No file selected.")
        except Exception as e:
            self.print(f"Error: {e}")

    # 设置鼠标样式为等待样式
    def setCursorIng(self):
        self.window.setCursor(Qt.CursorShape.WaitCursor)

    # 设置鼠标样式为箭头样式
    def setCursorArrow(self):
        self.window.setCursor(Qt.CursorShape.ArrowCursor)

    def print(self, *args):
        # 将入参拼接成字符串
        msg = " ".join(map(str, args))
        logger.info(msg)
        msg = f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}] {msg}"
        self.listLog.addItem(msg)
        self.statusbar.showMessage(msg)

    def debug(self, *args):
        msg = " ".join(map(str, args))
        logger.debug(msg)
        self.statusbar.showMessage(msg)

    def exec(self):
        sys.exit(self.app.exec())


# 录制音频独立线程类
class RecordWorker(QObject):
    # record_data = np.array([])  # 录音数据
    record_data = []  # 录音数据
    record_data_info = pyqtSignal(str)  # 用于传递录音数据汇总信息
    log_data = pyqtSignal(str)  # 信号，用于传递日志信息
    runThread = None
    recording_finished = None
    record_data_info_callback = None
    start_time = None
    skip_record_sec = 5  # 录音时，跳过前4秒，防止麦克风启动时的杂音

    # 构造函数, record_finished_callback为录音结束后的回调函数,必须传入
    def __init__(
        self,
        record_dialog_ui,
        log_func,
        record_data_info_callback,
        device_index=0,
        sampleRate=8000,
        channels=1,
    ):
        super().__init__()

        self.runThread = QThread()
        self.moveToThread(self.runThread)
        self.stream = None
        self.record_dialog_ui = record_dialog_ui
        self.record_data_info_callback = record_data_info_callback
        self.sampleRate = sampleRate
        self.channels = channels
        self.device_index = device_index

        self.record_data_info.connect(self.record_data_info_callback)
        # 如果存在log_func,则连接log_data信号
        if log_func:
            self.log_data.connect(log_func)

    def record(self):
        # 开始录音流
        self.print(f"录音设备：{sd.query_devices(self.device_index)}")
        self.print(f"开始获取录音数据流,参数：device_index={self.device_index}, sampleRate={self.sampleRate}, channels={self.channels}")
        self.stream = sd.InputStream(
            device=self.device_index,
            samplerate=self.sampleRate,
            channels=self.channels,
            callback=self.audio_callback,
            dtype="float32",
        )
        self.start_time = time.time()
        self.print(
            f"录音开始时间 {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}"
        )
        self.stream.start()
        self.record_data_info.emit("准备开始录音.")

    def audio_callback(self, indata, frames, _, status):
        if status:
            self.print(status)

        
        # indata是一个numpy数组，包含录制的音频数据
        self.record_data = np.append(self.record_data, indata)
        # self.record_data.append(indata)
        # 前4秒特殊处理，防止麦克风启动时的杂音
        if time.time() - self.start_time < self.skip_record_sec:
            # 取当前时间毫秒数，整除100，获取百位毫秒数值。

            # 比如当前时间为12:34:56.789，则百位毫秒数值为7
            ms = int(time.time()*10 % 10)  # 取百位数值
            r = ""
            if ms % 4 == 0:
                # 每100毫秒，打印一次当前时间
                r = "-"
            elif ms % 4 == 1:
                r = "\\"
            elif ms % 4 == 2:
                r = "|"
            elif ms % 4 == 3:
                r = "/"

            self.record_data_info.emit(f"准备开始录音.{r}")
        else :
            # 计算得到已录音的数据大小，单位bytes
            # data_size = sum(len(chunk) for chunk in self.record_data)
            data_size = self.record_data.nbytes
            # 计算data_time，单位秒
            data_time = time.time() - self.start_time - self.skip_record_sec
            # 发送信号，汇总已录音的数据信息
            self.record_data_info.emit(
                f"已录音: {data_time:.2f} 秒，{data_size / 1024:.2f} KB"
            )

    def stop_recording(self):
        self.print("停止录音数据获取")
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        if hasattr(self, "runThread") and self.runThread.isRunning():
            self.runThread.quit()  # 发送退出信号
            self.runThread.wait(2000)

        # return np.concatenate(self.record_data, axis=0)
        return self.record_data

    # 打印日志信息，通过发出信号，让主窗口打印出来
    def print(self, *args):

        # 将入参拼接成字符串
        msg = " ".join(map(str, args))
        self.log_data.emit(msg)


# 定义一个发送数据的线程类
class Sender(QObject):
    data_ready = pyqtSignal(str)  # 假设我们发送的数据是 str 类型
    ser = None
    data = None
    runThread = None
    running = False

    def __init__(
        self, ser, data, send_duration, debug_func, print_func, send_finish_func
    ):
        super().__init__()
        # 在这里初始化你的网络连接或其他资源
        self.ser = ser
        self.data = data
        self.runThread = QThread()
        self.moveToThread(self.runThread)
        self.runThread.started.connect(self.run)
        self.data_ready.connect(debug_func)
        self.print_func = print_func
        self.send_finish_func = send_finish_func
        self.send_duration = send_duration
        self.chunk_size = 256  # 每次发送的数据块大小

    def run(self):
        # 在这里读取和发送网络数据
        self.writeBinary(self.data)
        # 当数据准备好时，发出信号

    def start(self):
        self.runThread.start()
        self.running = True

    def stop(self):
        self.running = False
        self.runThread.quit()
        # 等待最多2秒，确保线程退出
        self.runThread.wait(2000)

    # 确保线程退出
    def __del__(self):
        self.stop()

    def writeBinary(self, data):

        if self.ser is None or not self.ser.is_open:
            self.print("串口未打开，请先选择对应串口打开！")
            return

        chunk_size = self.chunk_size  # 每次发送的数据块大小

        # 要发送的二进制数据
        binary_data = data

        # 发送二进制数据
        try:
            self.print_func(
                f"开始发送文件，准备分块（{chunk_size}bytes）写入缓冲区，时间间隔：{self.send_duration}ms，总数据长度: {len(binary_data) / 1024:.2f} KB"
            )

            # 发送数据，每次发送CHUNK_SIZE字节
            offset = 0
            while self.running and offset < len(binary_data):
                chunk = binary_data[offset : offset + chunk_size]
                # 打印发送的数据的16进制字符串
                logger.debug(f"发送数据: {chunk.hex()}")
                self.ser.write(chunk)

                # 等待发送缓冲区中的数据被清空
                while self.running and self.ser.out_waiting:
                    # 这里可以添加一些延时来避免过度轮询
                    time.sleep(self.send_duration / 1000)  # 延时10ms

                offset += len(chunk)

                # 打印发送的数据字节信息，发送百分比，已发送多少/总共多少，单位Bytes
                self.print(
                    f"已发送百分比: {offset / len(binary_data) * 100:.2f} %，[{offset / 1024:.2f} KB / {len(binary_data) / 1024:.2f} KB]"
                )

            # 打印发送完成后的汇总信息
            if offset == len(binary_data):
                self.print_func(
                    f"发送完成：100%，总数据长度: {len(binary_data) / 1024:.2f} KB"
                )

        except serial.SerialException as e:
            self.print(f"发送数据时出错: {e}")
        finally:
            self.send_finish_func()

    # 打印日志信息，通过发出信号，让主窗口打印出来
    def print(self, *args):

        # 将入参拼接成字符串
        msg = " ".join(map(str, args))
        self.data_ready.emit(msg)


if __name__ == "__main__":
    from PyQt6.QtCore import QDir

    QDir.addSearchPath("ui", "ui/icon")
    ui_tool = SendFileWindow()
    ui_tool.exec()
