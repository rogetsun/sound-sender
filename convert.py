import ffmpeg, subprocess, platform
from pydub import AudioSegment
from pydub.utils import mediainfo

def wav_to_wma(input_file, output_file=None, audio_bitrate="24k", log_func=None):
    """
    使用ffmpeg将WAV文件转换为WMA文件。

    参数:
    input_file (str): 输入的WAV文件路径。
    output_file (str, optional): 输出的WMA文件路径。默认为None，此时将使用输入文件的名称（去掉.wav后缀）并添加.wma后缀。
    audio_bitrate (str, optional): 音频比特率。默认为'16k'。

    返回:
    None

    Raises:
    ValueError: 如果输入文件不是WAV文件。
    """
    if not input_file.endswith(".wav"):
        raise ValueError("输入文件必须是WAV文件。")

    if not output_file:
        output_file = input_file[:-4] + ".wma"

    try:
        cmd = get_ffmpeg_cmd()
        if not cmd:
            raise FileNotFoundError("ffmpeg not found in PATH or current directory.")
        input = (
            ffmpeg.input(input_file)
            .output(output_file, acodec="wmav2", audio_bitrate=audio_bitrate)
            .overwrite_output()
            .run(
                cmd=cmd,
                overwrite_output=True,
                capture_stdout=subprocess.PIPE,
                capture_stderr=subprocess.PIPE,
                quiet=True,
            )
        )

        # # 构建FFmpeg命令的参数数组
        # args = [
        #     cmd,
        #     "-i",
        #     input_file,
        #     "-c:a",
        #     "wmav2",
        #     "-b:a",
        #     audio_bitrate,
        #     "-y",
        #     output_file,
        # ]
        # if log_func:
        #     log_str = " ".join(args)
        #     log_func(f"执行命令: {log_str}")
        # # 使用subprocess执行命令
        # if platform.system() == "Windows":
        #     log_func("Windows系统，使用CREATE_NO_WINDOW创建子进程")
        #     result = subprocess.Popen(
        #         args,
        #         stdout=subprocess.PIPE,
        #         stderr=subprocess.PIPE,
        #         universal_newlines=True,
        #         creationflags=subprocess.CREATE_NO_WINDOW,
        #         shell=False
        #     )
        # else:
        #     log_func("非Windows系统，使用shell=False创建子进程")
        #     result = subprocess.run(
        #         args,
        #         stdout=subprocess.PIPE,
        #         stderr=subprocess.PIPE,
        #         universal_newlines=True,
        #         shell=False,
        #     )

    except ffmpeg.Error as e:
        print(f"转换失败: {e}")
    except FileNotFoundError:
        print("ffmpeg not found in PATH.")
    except ValueError as e:
        print(f"转换失败: {e}")


def wav_to_mp3(input_file, output_file=None, audio_bitrate="24k", log_func=None):
    """
    使用pydub将wav文件转换为mp3文件
    """
    if not input_file.endswith(".wav"):
        raise ValueError("输入文件必须是WAV文件。")

    if not output_file:
        output_file = input_file[:-4] + ".mp3"

    # 转换wav文件为mp3文件
    sound = AudioSegment.from_file(input_file, "wav")
    sound.export(output_file, format="mp3", bitrate=audio_bitrate)


def wav_to_aac(input_file, output_file=None, audio_bitrate="24k", log_func=None):
    """
    使用ffmpeg将wav文件转换为aac文件
    """
    if not input_file.endswith(".wav"):
        raise ValueError("输入文件必须是WAV文件。")

    if not output_file:
        output_file = input_file[:-4] + ".aac"

    try:
        cmd = get_ffmpeg_cmd()
        if not cmd:
            raise FileNotFoundError("ffmpeg not found in PATH or current directory.")
        input = (
            ffmpeg.input(input_file)
            .output(output_file, acodec="aac", audio_bitrate=audio_bitrate)
            .overwrite_output()
            .run(
                cmd=cmd,
                overwrite_output=True,
                capture_stdout=subprocess.PIPE,
                capture_stderr=subprocess.PIPE,
                quiet=True,
            )
        )

    except ffmpeg.Error as e:
        print(f"转换失败: {e}")
    except FileNotFoundError:
        print("ffmpeg not found in PATH.")
    except ValueError as e:
        print(f"转换失败: {e}")


def get_ffmpeg_cmd():

    # 假设我们想要查找的ffmpeg.exe在系统PATH中
    # 根据操作系统构建ffmpeg命令
    if platform.system() == "Windows":
        ffmpeg_command = ["ffmpeg", "-version"]
    else:
        # 假设在Linux或Mac上，ffmpeg可能安装在/usr/bin或/usr/local/bin等位置
        # 你可以根据你的安装位置调整这个命令
        ffmpeg_command = ["ffmpeg", "-version"]

    if execute_command(ffmpeg_command):
        return ffmpeg_command[0]
    elif execute_command(["./ffmpeg", "-version"]):
        return "./ffmpeg"

    return None


def execute_command(command):

    try:
        # 尝试执行ffmpeg命令
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=False,
        )
        return True  # 如果命令成功执行，返回True
    except subprocess.CalledProcessError as e:
        # 如果ffmpeg命令执行失败（例如，找不到命令），则打印错误信息并返回False
        # print(f"Error executing ffmpeg: {e}")
        return False
    except FileNotFoundError:
        # 如果ffmpeg命令不存在于PATH中，将引发FileNotFoundError
        # print("ffmpeg not found in PATH.")
        return False

# 压缩mp3文件
def compress_mp3(input_file, output_file=None, bitrate="24k", log_func=None):
    """
    使用ffmpeg将mp3文件压缩到指定比特率。

    参数:
    input_file (str): 输入的MP3文件路径。
    output_file (str, optional): 输出的MP3文件路径。默认为None，此时将使用输入文件的名称（去掉.mp3后缀）并添加.mp3后缀。
    bitrate (str, optional): 压缩比特率。默认为'24k'。

    返回:
    None

    Raises:
    ValueError: 如果输入文件不是MP3文件。
    """
    postfix = input_file[-4:].lower()
    if not  postfix.endswith(".mp3") :
        raise ValueError("输入文件必须是MP3文件。")

    if not output_file:
        output_file = input_file[:-4] + f"-{bitrate}.mp3"

    try:
        cmd = get_ffmpeg_cmd()
        if not cmd:
            raise FileNotFoundError("ffmpeg not found in PATH or current directory.")
        input = (
            ffmpeg.input(input_file)
            .output(output_file, acodec="libmp3lame", audio_bitrate=bitrate)
            .overwrite_output()
            .run(
                cmd=cmd,
                overwrite_output=True,
                capture_stdout=subprocess.PIPE,
                capture_stderr=subprocess.PIPE,
                quiet=True,
            )
        )

    except ffmpeg.Error as e:
        print(f"压缩失败: {e}")
    except FileNotFoundError:
        print("ffmpeg not found in PATH.")
    except ValueError as e:
        print(f"压缩失败: {e}")

def get_audio_info(file_name):
    """
    获取音频文件的信息。

    参数:
    file_name (str): 音频文件路径。

    返回:
    dict: 音频文件的信息。
    """
    info = mediainfo(file_name)
    return info

if __name__ == "__main__":
    audio_file = "D:/Downloads/test8.mp3"
    print(f"音频文件信息：{audio_file}")
    info = get_audio_info(audio_file)
    # json格式化打印info
    import json
    print(json.dumps(info, indent=4))
    print()
    
    bitrate="8k"
    input_file = "D:/UV/Music/灵便音频转换器/24-3.wav"
    output_file = input_file[:-4] + f"-{bitrate}.mp3"
    
    if get_ffmpeg_cmd():
        print("ffmpeg is available.")
    else:
        print("ffmpeg is not available.")

    wav_to_mp3(input_file=input_file,output_file=output_file,audio_bitrate=bitrate,log_func=print)
    
    bitrate="8k"
    input_mp3_file = "D:/UV/Music/灵便音频转换器/24-5.MP3"
    # output file 名字为input_mp3_file的文件名加上压缩比特率+mp3后缀
    output_mp3_file = input_mp3_file[:-4] + f"-{bitrate}.mp3"
    # compress_mp3(input_mp3_file, output_file=output_mp3_file, bitrate=bitrate, log_func=print)