# 串口下发音频项目
## 介绍

给老高使用的项目，通过rs485串口的方式，将wma音频发送给语音播放设备。
需要ffmpeg.exe文件，请自行下载。
## 打包exe文件

### 方式1：

在项目主目录执行如下命令，打包成exe可以执行文件。

```powershell
pyinstaller -F -w -n sender.exe --i ui/icon/s.ico main.py
```

更详细的方式（由auto-py-to-exe.exe 配置生成）：

```
pyinstaller --noconfirm --onefile --windowed --icon "D:\UV\vsProject\soundsender\ui\icon\s.ico" --name "sound-sender" --log-level "INFO" --add-binary "D:\UV\vsProject\soundsender\lib\ffmpeg.exe;."  "D:\UV\vsProject\soundsender\main.py"
```

### 方式2：

```
auto-py-to-exe.exe 
```

![image](https://raw.githubusercontent.com/rogetsun/pic-space/main/picgo-img/202408191253518.png)

![image-1](https://raw.githubusercontent.com/rogetsun/pic-space/main/picgo-img/202408191256328.png)
