import os
import subprocess
import time
import urllib.request
import sys
import json
import tty
import termios
import shutil

# ================== 配置与国际化 ==================
config_path = os.path.expanduser('~/.tqqs_config')
strings = {
    'zh': {
        'main_title': "------<<Termux Black MIDI Toolbox v1.4>>------",
        'main_choices': ["MIDI工具箱", "MIDI转音频", "合并音视频", "语言设置", "退出程序"],
        'sub_title': "------<<TQQS Termux Toolbox v1.4>>------",
        'sub_choices': ["下载MIDI", "选择MIDI并渲染", "关于脚本", "返回上级界面"],
        'download_title': "---<<下载MIDI>>---",
        'download_choices': ["默认测试MIDI", "更多MIDI", "自定义链接", "返回上级界面"],
        'render_resolution': "---<<选择渲染分辨率>>---",
        'render_fps': "---<<选择帧率>>---",
        'render_ppb': "---<<选择音符长度(数值越小越慢)>>---",
        'render_keyh': "---<<选择键盘高度(推荐：140)>>---",
        'about': "------<<TQQS Termux Toolbox v1.4>>------\n脚本作者：黑乐谱末影君\n版本：v1.4",
        'exit': "感谢使用，再见！",
        'invalid_choice': "无效选项，请重新输入",
        'no_midi': "MIDI文件夹为空，请先下载MIDI文件",
        'select_midi': "---<<MIDI选择>>---",
        'back': "返回上级界面",
        'custom': "自定义",
        'confirm_exit': "确定退出？(Y/N)",
        'lang_switch': "语言切换成功！",
        'resolution_options': [
            "1,3840x2160 (4K)", "2,2560x1440 (2K)", "3,1920x1080 (1080p)",
            "4,1280x720 (720p)", "5,自定义分辨率"
        ],
        'fps_options': ["1,60 fps", "2,45 fps", "3,30 fps", "4,15 fps", "5,自定义帧率"],
        'ppb_options': [
            "1,520 ppb", "2,480 ppb", "3,440 ppb", 
            "4,400 ppb", "5,自定义音符长度"
        ],
        'keyh_options': [
            "1,180", "2,160", "3,140", 
            "4,120", "5,自定义键盘高度"
        ],
        'download_success': "下载成功: {}",
        'download_fail': "下载失败: {}",
        'render_start': "\n开始渲染...",
        'render_success': "\n渲染成功完成！",
        'render_fail': "\n渲染失败，错误代码: {}",
        'render_path': "视频已保存至: {}",
        'invalid_number': "请输入有效数字",
        'enter_url': "请输入MIDI文件链接: ",
        'enter_filename': "请输入保存文件名: ",
        'width': "宽度: ",
        'height': "高度: ",
        'fps_input': "帧率: ",
        'ppb_input': "每拍音符长度(px): ",
        'keyh_input': "键盘高度: ",
        'use_arrow': "\n使用↑↓键选择，Enter确认，或输入数字",
        'enter_choice': "\n请输入选项: ",
        'press_enter': "按Enter键返回...",
        'language_settings': "---<<语言设置>>---",
        # 新增字符串
        'convert_title': "---<<转换MIDI到音频>>---",
        'select_sf2': "---<<选择音色库>>---",
        'download_sf2': "正在下载音色库...",
        'sf2_download_success': "音色库下载成功",
        'sf2_download_fail': "音色库下载失败",
        'converting': "转换中...",
        'convert_success': "转换成功！",
        'convert_fail': "转换失败，错误代码: {}",
        'audio_path': "音频文件已保存至: {}",
        'installing_fluidsynth': "正在安装fluidsynth...",
        'fluidsynth_not_found': "未找到fluidsynth，正在安装...",
        'merge_title': "---<<合并音视频>>---",
        'no_video': "视频文件夹为空，请先渲染视频",
        'no_audio': "音频文件夹为空，请先转换音频",
        'select_video': "---<<选择视频文件>>---",
        'select_audio': "---<<选择音频文件>>---",
        'merging': "合并中...",
        'merge_success': "合并成功完成！",
        'merge_fail': "合并失败，错误代码: {}",
        'merge_path': "视频已保存至: {}",
        'ffmpeg_not_found': "未找到FFmpeg，正在安装...",
        'installing_ffmpeg': "正在安装FFmpeg...",
        'move_final': "是否将final_video中的文件移动到/sdcard？(y/n): ",
        'move_success': "文件已成功移动到/sdcard",
        'move_fail': "文件移动失败: {}"
    },
    'en': {
        'main_title': "------<<Termux Black MIDI Toolbox v1.4>>------",
        'main_choices': ["MIDI Toolkit", "MIDI to Audio", "Merge Audio/Video", "Language", "Exit"],
        'sub_title': "------<<TQQS Termux Toolbox v1.4>>------",
        'sub_choices': ["Download MIDI", "Select MIDI & Render", "About Script", "Back to Main Menu"],
        'download_title': "---<<Download MIDI>>---",
        'download_choices': ["Default Test MIDI", "More MIDI", "Custom URL", "Back to Menu"],
        'render_resolution': "---<<Render Resolution>>---",
        'render_fps': "---<<Frame Rate>>---",
        'render_ppb': "---<<Note Length (Smaller is slower)>>---",
        'render_keyh': "---<<Keyboard Height (Recommended: 140)>>---",
        'about': "------<<TQQS Termux Toolbox v1.4>>------\nAuthor: Enderman-bm\nVersion: v1.4",
        'exit': "Thanks for using, goodbye!",
        'invalid_choice': "Invalid option, please try again",
        'no_midi': "MIDI folder is empty, please download first",
        'select_midi': "---<<MIDI Selection>>---",
        'back': "Back to Previous",
        'custom': "Custom",
        'confirm_exit': "Confirm exit? (Y/N)",
        'lang_switch': "Language switched successfully!",
        'resolution_options': [
            "3840x2160 (4K)", "2560x1440 (2K)", "1920x1080 (1080p)",
            "1280x720 (720p)", "Custom Resolution"
        ],
        'fps_options': ["60 fps", "45 fps", "30 fps", "15 fps", "Custom FPS"],
        'ppb_options': [
            "520 ppb", "480 ppb", "440 ppb", 
            "400 ppb", "Custom Note Length"
        ],
        'keyh_options': [
            "180", "160", "140", 
            "120", "Custom Keyboard Height"
        ],
        'download_success': "Download successful: {}",
        'download_fail': "Download failed: {}",
        'render_start': "\nStarting render...",
        'render_success': "\nRender completed successfully!",
        'render_fail': "\nRender failed, error code: {}",
        'render_path': "Video saved to: {}",
        'invalid_number': "Please enter a valid number",
        'enter_url': "Enter MIDI URL: ",
        'enter_filename': "Enter filename: ",
        'width': "Width: ",
        'height': "Height: ",
        'fps_input': "FPS: ",
        'ppb_input': "Pixels per beat: ",
        'keyh_input': "Keyboard height: ",
        'use_arrow': "\nUse ↑↓ to navigate, Enter to confirm",
        'enter_choice': "\nEnter choice: ",
        'press_enter': "Press Enter to return...",
        'language_settings': "---<<Language Settings>>---",
        # New strings
        'convert_title': "---<<Convert MIDI to Audio>>---",
        'select_sf2': "---<<Select SoundFont>>---",
        'download_sf2': "Downloading SoundFont...",
        'sf2_download_success': "SoundFont downloaded successfully",
        'sf2_download_fail': "SoundFont download failed",
        'converting': "Converting...",
        'convert_success': "Conversion succeeded!",
        'convert_fail': "Conversion failed, error code: {}",
        'audio_path': "Audio saved to: {}",
        'installing_fluidsynth': "Installing fluidsynth...",
        'fluidsynth_not_found': "Fluidsynth not found, installing...",
        'merge_title': "---<<Merge Audio/Video>>---",
        'no_video': "Video folder is empty, please render video first",
        'no_audio': "Audio folder is empty, please convert audio first",
        'select_video': "---<<Select Video File>>---",
        'select_audio': "---<<Select Audio File>>---",
        'merging': "Merging...",
        'merge_success': "Merge completed successfully!",
        'merge_fail': "Merge failed, error code: {}",
        'merge_path': "File saved to: {}",
        'ffmpeg_not_found': "FFmpeg not found, installing...",
        'installing_ffmpeg': "Installing FFmpeg...",
        'move_final': "Move files to /sdcard? (y/n): ",
        'move_success': "Files successfully moved to /sdcard",
        'move_fail': "Failed to move files: {}"
    }
}

# 加载语言配置
def load_config():
    global lang
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            lang = config.get('lang', 'zh')
    else:
        lang = 'zh'
# 保存语言配置
def save_config():
    with open(config_path, 'w') as f:
        json.dump({'lang': lang}, f)
# 初始化语言
load_config()

# ================== 核心功能函数 ==================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
def expand_path(path):
    return os.path.expanduser(path)
def get_key():
    """获取单个键盘输入，支持方向键"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch += sys.stdin.read(2)
            if ch == '\x1b[A':
                return 'UP'
            elif ch == '\x1b[B':
                return 'DOWN'
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
def draw_box(text):
    """绘制带边框的标题"""
    lines = text.split('\n')
    width = max(len(line) for line in lines)
    print('┌' + '─' * (width + 2) + '┐')
    for line in lines:
        print('│ ' + line.ljust(width) + ' │')
    print('└' + '─' * (width + 2) + '┘')
def navigate_menu(options, title_key, parent_strings=strings):
    """通用菜单导航系统"""
    current = 0
    while True:
        clear_screen()
        draw_box(parent_strings[lang][title_key])
        print(parent_strings[lang]['use_arrow'])
        for i, option in enumerate(options):
            prefix = "  > " if i == current else "    "
            print(f"{prefix}{option}")
        key = get_key()
        if key == 'UP':
            current = (current - 1) % len(options)
        elif key == 'DOWN':
            current = (current + 1) % len(options)
        elif key == '\r' or key == '\n':
            return current
        else:
            if key.isdigit() and 1 <= int(key) <= len(options):
                return int(key) - 1

# ================== MIDI下载模块 ==================
def download_midi():
    midi_dir = "input_MIDI"
    if not os.path.exists(midi_dir):
        os.makedirs(midi_dir)
    options = strings[lang]['download_choices']
    while True:
        choice = navigate_menu(options, 'download_title')
        if choice == 0:  # 默认测试MIDI
            url = "https://endermanbili.obs.cn-east-3.myhuaweicloud.com/TBMB%E4%B8%8B%E8%BD%BD%E6%BA%90/demo_midi.mid "
            filename = "demo_midi.mid"
            save_path = os.path.join(midi_dir, filename)
            try:
                urllib.request.urlretrieve(url, save_path)
                print(strings[lang]['download_success'].format(filename))
            except Exception as e:
                print(strings[lang]['download_fail'].format(str(e)))
            time.sleep(2)
        elif choice == 1:  # 更多MIDI
            clear_screen()
            draw_box("更多MIDI" if lang == 'zh' else "More MIDI")
            print("功能尚未实现" if lang == 'zh' else "Not implemented yet")
            input(strings[lang]['press_enter'])
        elif choice == 2:  # 自定义下载
            clear_screen()
            draw_box("自定义下载" if lang == 'zh' else "Custom Download")
            url = input(strings[lang]['enter_url']).strip()
            filename = input(strings[lang]['enter_filename']).strip()
            if not filename.endswith('.mid'):
                filename += '.mid'
            save_path = os.path.join(midi_dir, filename)
            try:
                urllib.request.urlretrieve(url, save_path)
                print(strings[lang]['download_success'].format(filename))
            except Exception as e:
                print(strings[lang]['download_fail'].format(str(e)))
            time.sleep(2)
        elif choice == 3:  # 返回
            return

# ================== MIDI选择模块 ==================
def list_midi_files():
    midi_dir = "input_MIDI"
    if not os.path.exists(midi_dir) or not os.listdir(midi_dir):
        print(strings[lang]['no_midi'])
        time.sleep(2)
        return None
    files = [f for f in os.listdir(midi_dir) if f.endswith('.mid')]
    return files
def select_midi():
    files = list_midi_files()
    if not files:
        return None
    options = files + [strings[lang]['back']]
    while True:
        clear_screen()
        draw_box(strings[lang]['select_midi'])
        choice = navigate_menu(options, 'select_midi')
        if choice == len(files):  # 返回
            return None
        elif 0 <= choice < len(files):
            return os.path.join("input_MIDI", files[choice])

# ================== 参数设置模块 ==================
def get_resolution():
    options = strings[lang]['resolution_options']
    choice = navigate_menu(options, 'render_resolution')
    if choice == 0: return 3840, 2160
    elif choice == 1: return 2560, 1440
    elif choice == 2: return 1920, 1080
    elif choice == 3: return 1280, 720
    elif choice == 4:
        clear_screen()
        draw_box("自定义分辨率" if lang == 'zh' else "Custom Resolution")
        try:
            width = int(input(strings[lang]['width']).strip())
            height = int(input(strings[lang]['height']).strip())
            return width, height
        except ValueError:
            print(strings[lang]['invalid_number'])
            time.sleep(1)
            return get_resolution()
def get_fps():
    options = strings[lang]['fps_options']
    choice = navigate_menu(options, 'render_fps')
    if choice == 0: return 60
    elif choice == 1: return 45
    elif choice == 2: return 30
    elif choice == 3: return 15
    elif choice == 4:
        clear_screen()
        draw_box("自定义帧率" if lang == 'zh' else "Custom FPS")
        try:
            return int(input(strings[lang]['fps_input']).strip())
        except ValueError:
            print(strings[lang]['invalid_number'])
            time.sleep(1)
            return get_fps()
def get_ppb():
    options = strings[lang]['ppb_options']
    choice = navigate_menu(options, 'render_ppb')
    if choice == 0: return 520
    elif choice == 1: return 480
    elif choice == 2: return 440
    elif choice == 3: return 400
    elif choice == 4:
        clear_screen()
        draw_box("自定义音符长度" if lang == 'zh' else "Custom Note Length")
        try:
            return int(input(strings[lang]['ppb_input']).strip())
        except ValueError:
            print(strings[lang]['invalid_number'])
            time.sleep(1)
            return get_ppb()
def get_keyh():
    options = strings[lang]['keyh_options']
    choice = navigate_menu(options, 'render_keyh')
    if choice == 0: return 180
    elif choice == 1: return 160
    elif choice == 2: return 140
    elif choice == 3: return 120
    elif choice == 4:
        clear_screen()
        draw_box("自定义键盘高度" if lang == 'zh' else "Custom Keyboard Height")
        try:
            return int(input(strings[lang]['keyh_input']).strip())
        except ValueError:
            print(strings[lang]['invalid_number'])
            time.sleep(1)
            return get_keyh()

# ================== 渲染模块 ==================
def render_midi():
    midi_path = select_midi()
    if not midi_path:
        return
    width, height = get_resolution()
    fps = get_fps()
    ppb = get_ppb()
    keyh = get_keyh()
    video_dir = "output_video"
    if not os.path.exists(video_dir):
        os.makedirs(video_dir)
    video_name = os.path.basename(midi_path).replace('.mid', '.mp4')
    video_path = os.path.join(video_dir, video_name)
    qqs_path = expand_path("~/TQQS/bin/QQS")
    if not os.path.exists(qqs_path):
        print(f"错误：未找到QQS程序，请确保路径存在: {qqs_path}")
        print("请检查TQQS是否安装在 ~/TQQS/bin/ 目录下")
        time.sleep(3)
        return
    cmd = [
        qqs_path,
        f'-mid={midi_path}',
        f'-vid={video_path}',
        f'-wei={width}',
        f'-hei={height}',
        f'-fps={fps}',
        f'-ppb={ppb}',
        f'-keyh={keyh}'
    ]
    print(strings[lang]['render_start'])
    print("渲染命令: " + " ".join(cmd))
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        for line in process.stdout:
            print(line, end='')
        process.wait()
        if process.returncode == 0:
            print(strings[lang]['render_success'])
        else:
            print(strings[lang]['render_fail'].format(process.returncode))
    except Exception as e:
        print(f"执行错误: {str(e)}")
    print(strings[lang]['render_path'].format(video_path))
    # 请求用户是否移动文件到外部
    source_dir = os.path.expanduser("~/TQQS/output_video")
    target_dir = "/sdcard/moved_video"
    # 如果目标文件夹不存在，则创建
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"目标文件夹 {target_dir} 不存在，已创建。")
    # 用户确认
    response = input(f"是否将 {source_dir} 中的  mp4 文件移动到 {target_dir}？(y/n): ").strip().lower()
    if response == 'y':
        # 执行移动命令
        os.system(f'mv "{source_dir}"/*.mp4 "{target_dir}"')
        # 清空原目录内容
        os.system(f'rm -rf "{source_dir}"/*')
        print("文件已成功移动并清空原目录。")
    else:
        print("操作已取消。")
    print("5秒后返回主菜单..." if lang == 'zh' else "Return to main menu in 5 seconds...")
    time.sleep(5)

# ================== 辅助功能 ==================
def about_script():
    clear_screen()
    draw_box(strings[lang]['about'])
    input(strings[lang]['press_enter'])
def switch_language():
    global lang
    options = ["中文", "English"]
    choice = navigate_menu(options, 'language_settings')
    lang = 'zh' if choice == 0 else 'en'
    save_config()
    print(strings[lang]['lang_switch'])
    time.sleep(1)

# ================== MIDI转音频功能 ==================
def check_fluidsynth():
    """检查fluidsynth是否安装"""
    return shutil.which('fluidsynth') is not None

def install_fluidsynth():
    """安装fluidsynth"""
    clear_screen()
    draw_box(strings[lang]['installing_fluidsynth'])
    try:
        subprocess.run(['pkg', 'install', '-y', 'fluidsynth'], check=True)
    except subprocess.CalledProcessError as e:
        print(strings[lang]['fluidsynth_not_found'])
        time.sleep(2)
        return False
    return True

def manage_soundfonts():
    """管理音色库"""
    sf2_dir = os.path.expanduser("~/TQQS/input_sf2")
    if not os.path.exists(sf2_dir):
        os.makedirs(sf2_dir)
    
    sf2_files = [f for f in os.listdir(sf2_dir) if f.endswith('.sf2')]
    
    if not sf2_files:
        # 下载默认音色库
        default_sf2_url = "https://endermanbili.obs.cn-east-3.myhuaweicloud.com/TBMB%E4%B8%8B%E8%BD%BD%E6%BA%90/Yamaha%20C7%20Piano.sf2 "
        default_sf2_path = os.path.join(sf2_dir, "Yamaha C7 Piano.sf2")
        clear_screen()
        draw_box(strings[lang]['download_sf2'])
        try:
            urllib.request.urlretrieve(default_sf2_url, default_sf2_path)
            print(strings[lang]['sf2_download_success'])
            sf2_files = [os.path.basename(default_sf2_path)]
        except Exception as e:
            print(strings[lang]['sf2_download_fail'].format(str(e)))
            time.sleep(2)
            return None
    
    return sf2_dir, sf2_files

def select_soundfont(sf2_dir, sf2_files):
    """选择音色库"""
    options = sf2_files + [strings[lang]['back']]
    while True:
        clear_screen()
        draw_box(strings[lang]['select_sf2'])
        choice = navigate_menu(options, 'select_sf2')
        if choice == len(sf2_files):  # 返回
            return None
        elif 0 <= choice < len(sf2_files):
            return os.path.join(sf2_dir, sf2_files[choice])

def convert_midi_to_audio():
    """转换MIDI到音频"""
    if not check_fluidsynth():
        if not install_fluidsynth():
            input(strings[lang]['press_enter'])
            return
    
    sf2_info = manage_soundfonts()
    if not sf2_info:
        input(strings[lang]['press_enter'])
        return
    
    sf2_dir, sf2_files = sf2_info
    selected_sf2 = select_soundfont(sf2_dir, sf2_files)
    if not selected_sf2:
        return
    
    midi_path = select_midi()
    if not midi_path:
        return
    
    output_dir = os.path.expanduser("~/TQQS/output_audio")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_name = os.path.basename(midi_path).replace('.mid', '.wav')
    output_path = os.path.join(output_dir, output_name)
    
    cmd = [
        'fluidsynth',
        '-ni', selected_sf2,
        midi_path,
        '-F', output_path,
        '-r', '44100'
    ]
    
    clear_screen()
    draw_box(strings[lang]['convert_title'])
    print(strings[lang]['converting'])
    print("转换命令: " + " ".join(cmd))
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        for line in process.stdout:
            print(line, end='')
        process.wait()
        
        if process.returncode == 0:
            print(strings[lang]['convert_success'])
        else:
            print(strings[lang]['convert_fail'].format(process.returncode))
    except Exception as e:
        print(f"执行错误: {str(e)}")
    
    print(strings[lang]['audio_path'].format(output_path))
    input(strings[lang]['press_enter'])

# ================== 音视频合并功能 ==================
def check_ffmpeg():
    """检查FFmpeg是否安装"""
    return shutil.which('ffmpeg') is not None

def install_ffmpeg():
    """安装FFmpeg"""
    clear_screen()
    draw_box(strings[lang]['installing_ffmpeg'])
    try:
        subprocess.run(['pkg', 'install', '-y', 'ffmpeg'], check=True)
    except subprocess.CalledProcessError:
        print(strings[lang]['ffmpeg_not_found'])
        time.sleep(2)
        return False
    return True

def list_files(directory, extension):
    """列出指定目录中的文件"""
    if not os.path.exists(directory):
        return []
    return [f for f in os.listdir(directory) if f.endswith(extension)]

def select_file(directory, extension, title_key):
    """选择文件"""
    files = list_files(directory, extension)
    if not files:
        print(strings[lang]['no_video' if extension == '.mp4' else 'no_audio'])
        time.sleep(2)
        return None
    
    options = files + [strings[lang]['back']]
    while True:
        clear_screen()
        draw_box(strings[lang][title_key])
        choice = navigate_menu(options, title_key)
        if choice == len(files):  # 返回
            return None
        elif 0 <= choice < len(files):
            return os.path.join(directory, files[choice])

def merge_audio_video():
    """合并音视频"""
    if not check_ffmpeg():
        if not install_ffmpeg():
            input(strings[lang]['press_enter'])
            return
    
    video_dir = os.path.expanduser("~/TQQS/bin/output_video")
    audio_dir = os.path.expanduser("~/TQQS/output_audio")
    final_dir = os.path.expanduser("~/TQQS/final_video")
    
    # 检查文件夹是否为空
    if not list_files(video_dir, '.mp4'):
        print(strings[lang]['no_video'])
        time.sleep(2)
        return
    if not list_files(audio_dir, '.wav'):
        print(strings[lang]['no_audio'])
        time.sleep(2)
        return
    
    # 选择视频文件
    video_path = select_file(video_dir, '.mp4', 'select_video')
    if not video_path:
        return
    
    # 选择音频文件
    audio_path = select_file(audio_dir, '.wav', 'select_audio')
    if not audio_path:
        return
    
    # 创建final_video目录
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)
    
    # 构建输出路径
    video_name = os.path.basename(video_path)
    output_name = os.path.splitext(video_name)[0] + "_merged.mp4"
    output_path = os.path.join(final_dir, output_name)
    
    # 构建FFmpeg命令
    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        '-shortest', output_path
    ]
    
    clear_screen()
    draw_box(strings[lang]['merge_title'])
    print(strings[lang]['merging'])
    print("合并命令: " + " ".join(cmd))
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        for line in process.stdout:
            print(line, end='')
        process.wait()
        if process.returncode == 0:
            print(strings[lang]['merge_success'])
        else:
            print(strings[lang]['merge_fail'].format(process.returncode))
            return
    except Exception as e:
        print(f"执行错误: {str(e)}")
        return
    
    print(strings[lang]['merge_path'].format(output_path))
    
    # 询问是否移动到/sdcard
    response = input(strings[lang]['move_final']).strip().lower()
    if response == 'y':
        try:
            # 移动文件
            shutil.move(output_path, "/sdcard")
            print(strings[lang]['move_success'])
        except Exception as e:
            print(strings[lang]['move_fail'].format(str(e)))
    else:
        print("操作已取消。" if lang == 'zh' else "Operation cancelled.")
    
    input(strings[lang]['press_enter'])

# ================== 主程序 ==================
def main():
    while True:
        clear_screen()
        draw_box(strings[lang]['main_title'])
        main_choices = strings[lang]['main_choices']
        choice = navigate_menu(main_choices, 'main_title')
        
        if choice == 0:
            # 进入子功能：MIDI 工具箱
            while True:
                clear_screen()
                draw_box(strings[lang]['sub_title'])
                sub_choices = strings[lang]['sub_choices']
                sub_choice = navigate_menu(sub_choices, 'sub_title')
                if sub_choice == 0:
                    download_midi()
                elif sub_choice == 1:
                    render_midi()
                elif sub_choice == 2:
                    about_script()
                elif sub_choice == 3:
                    break  # 返回主菜单
        elif choice == 1:
            convert_midi_to_audio()
        elif choice == 2:
            merge_audio_video()
        elif choice == 3:
            switch_language()
        elif choice == 4:
            print(strings[lang]['exit'])
            break

if __name__ == "__main__":
    main()