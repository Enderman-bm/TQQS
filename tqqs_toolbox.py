import os
import subprocess
import time
import urllib.request
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def expand_path(path):
    """扩展包含波浪号的路径"""
    return os.path.expanduser(path)
    
def download_midi():
    midi_dir = "input_MIDI"
    if not os.path.exists(midi_dir):
        os.makedirs(midi_dir)
    
    while True:
        clear_screen()
        print("---<<下载MIDI>>---")
        print("1，默认测试MIDI")
        print("2，更多MIDI")
        print("3，自定义链接")
        print("q，返回上级界面")
        
        choice = input("请选择: ").strip()
        
        if choice == '1':
            url = "https://file.uhsea.com/2507/60bdcc6676d4ba0d09fc335d5468dca2EP.mid"
            filename = "demo_shanghai_teahouse.mid"
            save_path = os.path.join(midi_dir, filename)
            
            try:
                urllib.request.urlretrieve(url, save_path)
                print(f"下载成功: {filename}")
            except Exception as e:
                print(f"下载失败: {str(e)}")
            time.sleep(2)
        
        elif choice == '2':
            clear_screen()
            print("---<<更多MIDI>>---")
            print("功能尚未实现")
            print("q，返回上级界面")
            input("按回车键返回...")
        
        elif choice == '3':
            clear_screen()
            print("---<<自定义下载>>---")
            url = input("请输入MIDI文件链接: ").strip()
            filename = input("请输入保存文件名: ").strip()
            
            if not filename.endswith('.mid'):
                filename += '.mid'
            
            save_path = os.path.join(midi_dir, filename)
            
            try:
                urllib.request.urlretrieve(url, save_path)
                print(f"下载成功: {filename}")
            except Exception as e:
                print(f"下载失败: {str(e)}")
            time.sleep(2)
        
        elif choice.lower() == 'q':
            return

def list_midi_files():
    midi_dir = "MIDI"
    if not os.path.exists(midi_dir) or not os.listdir(midi_dir):
        print("MIDI文件夹为空，请先下载MIDI文件")
        time.sleep(2)
        return None
    
    files = [f for f in os.listdir(midi_dir) if f.endswith('.mid')]
    return files

def select_midi():
    files = list_midi_files()
    if not files:
        return None
    
    while True:
        clear_screen()
        print("---<<MIDI选择>>---")
        for i, file in enumerate(files, 1):
            print(f"{i}，{file}")
        print("q，返回上级界面")
        
        choice = input("请选择MIDI文件: ").strip()
        
        if choice.lower() == 'q':
            return None
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(files):
                return os.path.join("MIDI", files[index])
        except ValueError:
            pass
        
        print("无效选择，请重试")
        time.sleep(1)

def get_resolution():
    while True:
        clear_screen()
        print("---<<选择渲染分辨率>>---")
        print("1，3840x2160 (4K)")
        print("2，2560x1440 (2K)")
        print("3，1920x1080 (1080p)")
        print("4，1280x720 (720p)")
        print("5，自定义")
        
        choice = input("请选择: ").strip()
        
        if choice == '1':
            return 3840, 2160
        elif choice == '2':
            return 2560, 1440
        elif choice == '3':
            return 1920, 1080
        elif choice == '4':
            return 1280, 720
        elif choice == '5':
            clear_screen()
            print("---<<自定义分辨率>>---")
            try:
                width = int(input("宽度: ").strip())
                height = int(input("高度: ").strip())
                return width, height
            except ValueError:
                print("请输入有效数字")
                time.sleep(1)
        else:
            print("无效选择，请重试")
            time.sleep(1)

def get_fps():
    while True:
        clear_screen()
        print("---<<选择渲染帧率>>---")
        print("1，60 fps")
        print("2，45 fps")
        print("3，30 fps")
        print("4，15 fps")
        print("5，自定义")
        
        choice = input("请选择: ").strip()
        
        if choice == '1':
            return 60
        elif choice == '2':
            return 45
        elif choice == '3':
            return 30
        elif choice == '4':
            return 15
        elif choice == '5':
            clear_screen()
            print("---<<自定义帧率>>---")
            try:
                fps = int(input("帧率: ").strip())
                return fps
            except ValueError:
                print("请输入有效数字")
                time.sleep(1)
        else:
            print("无效选择，请重试")
            time.sleep(1)

def get_ppb():
    while True:
        clear_screen()
        print("---<<选择音符长度(数值越小越慢)>>---")
        print("1，520 ppb")
        print("2，480 ppb")
        print("3，440 ppb")
        print("4，400 ppb")
        print("5，自定义")
        
        choice = input("请选择: ").strip()
        
        if choice == '1':
            return 520
        elif choice == '2':
            return 480
        elif choice == '3':
            return 440
        elif choice == '4':
            return 400
        elif choice == '5':
            clear_screen()
            print("---<<自定义音符长度>>---")
            try:
                ppb = int(input("每拍音符长度(px): ").strip())
                return ppb
            except ValueError:
                print("请输入有效数字")
                time.sleep(1)
        else:
            print("无效选择，请重试")
            time.sleep(1)

def get_keyh():
    while True:
        clear_screen()
        print("---<<选择键盘高度(推荐：140)>>---")
        print("1，180")
        print("2，160")
        print("3，140")
        print("4，120")
        print("5，自定义")
        
        choice = input("请选择: ").strip()
        
        if choice == '1':
            return 180
        elif choice == '2':
            return 160
        elif choice == '3':
            return 140
        elif choice == '4':
            return 120
        elif choice == '5':
            clear_screen()
            print("---<<自定义键盘高度>>---")
            try:
                keyh = int(input("键盘高度: ").strip())
                return keyh
            except ValueError:
                print("请输入有效数字")
                time.sleep(1)
        else:
            print("无效选择，请重试")
            time.sleep(1)

def render_midi():
    midi_path = select_midi()
    if not midi_path:
        return
    
    width, height = get_resolution()
    fps = get_fps()
    ppb = get_ppb()
    keyh = get_keyh()
    
    video_dir = "optput_video"
    if not os.path.exists(video_dir):
        os.makedirs(video_dir)
    
    video_name = os.path.basename(midi_path).replace('.mid', '.mp4')
    video_path = os.path.join(video_dir, video_name)
  
    # 修复路径问题：使用expanduser扩展波浪号路径
    qqs_path = expand_path("~/TQQS/bin/QQS")
    
    # 检查文件是否存在
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
    
    print("\n开始渲染...")
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
            print("\n渲染成功完成！")
        else:
            print(f"\n渲染失败，错误代码: {process.returncode}")
    except Exception as e:
        print(f"执行错误: {str(e)}")
    
    print("视频已保存至:", video_path)
    print("5秒后返回主菜单...")
    time.sleep(5)

def about_script():
    clear_screen()
    print("------<<TQQS Termux Toolbox v1.0>>------")
    print("脚本作者：黑乐谱末影君")
    print("版本：v1.4")
    input("\n按任意键返回上级界面...")

def main():
    while True:
        clear_screen()
        print("------<<TQQS Termux Toolbox v1.0>>------")
        print("1，下载MIDI")
        print("2，选择MIDI并且渲染")
        print("3，关于脚本")
        print("q，退出程序")
        
        choice = input("\n请输入选项: ").strip()
        
        if choice == '1':
            download_midi()
        elif choice == '2':
            render_midi()
        elif choice == '3':
            about_script()
        elif choice.lower() == 'q':
            print("感谢使用，再见！")
            break
        else:
            print("无效选项，请重新输入")
            time.sleep(1)

if __name__ == "__main__":
    main()
