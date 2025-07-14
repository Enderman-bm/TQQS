import os
import subprocess
import time
import urllib.request
import sys
import json
import tty
import termios

# ================== 配置与国际化 ==================
config_path = os.path.expanduser('~/.tqqs_config')

strings = {
    'zh': {
        'main_title': "------<<Termux Black MIDI Toolbox v1.0>>------",
        'main_choices': ["MIDI工具箱", "其他功能1", "其他功能2", "语言设置", "退出程序"],
        'sub_title': "------<<TQQS Termux Toolbox v1.0>>------",
        'sub_choices': ["下载MIDI", "选择MIDI并渲染", "关于脚本", "返回上级界面"],
        'download_title': "---<<下载MIDI>>---",
        'download_choices': ["默认测试MIDI", "更多MIDI", "自定义链接", "返回上级界面"],
        'render_resolution': "---<<选择渲染分辨率>>---",
        'render_fps': "---<<选择渲染帧率>>---",
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
            "3840x2160 (4K)", "2560x1440 (2K)", "1920x1080 (1080p)",
            "1280x720 (720p)", "自定义分辨率"
        ],
        'fps_options': ["60 fps", "45 fps", "30 fps", "15 fps", "自定义帧率"],
        'ppb_options': [
            "520 ppb", "480 ppb", "440 ppb", 
            "400 ppb", "自定义音符长度"
        ],
        'keyh_options': [
            "180", "160", "140", 
            "120", "自定义键盘高度"
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
        'language_settings': "---<<语言设置>>---"
    },
    'en': {
        'main_title': "------<<Termux Black MIDI Toolbox v1.0>>------",
        'main_choices': ["MIDI Toolkit", "Feature 1", "Feature 2", "Language", "Exit"],
        'sub_title': "------<<TQQS Termux Toolbox v1.0>>------",
        'sub_choices': ["Download MIDI", "Select MIDI & Render", "About Script", "Back to Main Menu"],
        'download_title': "---<<Download MIDI>>---",
        'download_choices': ["Default Test MIDI", "More MIDI", "Custom URL", "Back to Menu"],
        'render_resolution': "---<<Render Resolution>>---",
        'render_fps': "---<<Frame Rate>>---",
        'render_ppb': "---<<Note Length (Smaller is slower)>>---",
        'render_keyh': "---<<Keyboard Height (Recommended: 140)>>---",
        'about': "------<<TQQS Termux Toolbox v1.4>>------\nAuthor: Hei Yuepu\nVersion: v1.4",
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
        'language_settings': "---<<Language Settings>>---"
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
            url = "https://file.uhsea.com/2507/60bdcc6676d4ba0d09fc335d5468dca2EP.mid "
            filename = "demo_shanghai_teahouse.mid"
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
            print("功能开发中..." if lang == 'zh' else "Feature under development...")
            time.sleep(2)
        
        elif choice == 2:
            print("功能开发中..." if lang == 'zh' else "Feature under development...")
            time.sleep(2)
        
        elif choice == 3:
            switch_language()
        
        elif choice == 4:
            print(strings[lang]['exit'])
            break

if __name__ == "__main__":
    main()