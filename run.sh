#!/data/data/com.termux/files/usr/bin/bash

# 检查并安装ffmpeg
check_ffmpeg() {
    if ! command -v ffmpeg &> /dev/null; then
        echo "ffmpeg未安装，正在尝试安装..."
    fi
# 检查当前源是否为国内源
check_source() {
    local current_source
    current_source=$(grep -oP '(?<=^deb ).*' "$PREFIX/etc/apt/sources.list" | head -1)
    
    # 国内源列表
    local mirrors=(
        "mirrors.tuna.tsinghua.edu.cn/termux"
        "mirrors.bfsu.edu.cn/termux"
        "mirrors.ustc.edu.cn/termux"
        "mirrors.nju.edu.cn/termux"
        "mirrors.aliyun.com/termux"
    )
    
    for mirror in "${mirrors[@]}"; do
        if [[ "$current_source" == *"$mirror"* ]]; then
            return 0
        fi
    done
    return 1
}

# 更换APT源
change_source() {
    local selected_source="$1"
    echo "备份原源文件为 sources.list.bak"
    cp "$PREFIX/etc/apt/sources.list" "$PREFIX/etc/apt/sources.list.bak"
    
    echo "deb $selected_source stable main" > "$PREFIX/etc/apt/sources.list"
    echo "已更换为: $selected_source"
}

# 主函数
main() {
    # 检查是否为国内源
    if check_source; then
        echo "当前APT源已经是国内源，无需更换"
        return 0
    fi

    echo "检测到当前APT源非国内源，建议更换"
    echo "请选择国内镜像源："

    # 源选项数组
    local sources=(
        "清华大学源 - https://mirrors.tuna.tsinghua.edu.cn/termux"
        "北京外国语大学源 - https://mirrors.bfsu.edu.cn/termux"
        "中国科学技术大学源 - https://mirrors.ustc.edu.cn/termux"
        "南京大学源 - https://mirrors.nju.edu.cn/termux"
        "阿里云源 - https://mirrors.aliyun.com/termux"
    )
    
    # 对应的URL
    local urls=(
        "https://mirrors.tuna.tsinghua.edu.cn/termux"
        "https://mirrors.bfsu.edu.cn/termux"
        "https://mirrors.ustc.edu.cn/termux"
        "https://mirrors.nju.edu.cn/termux"
        "https://mirrors.aliyun.com/termux"
    )
    
    # 显示菜单
    PS3="请使用方向键选择(1-${#sources[@]})，回车确认: "
    select opt in "${sources[@]}" "取消更换"; do
        case $REPLY in
            [1-5])
                echo "正在更换为: ${sources[$((REPLY-1))]}"
                change_source "${urls[$((REPLY-1))]}"
                echo "更换完成，建议稍后运行 pkg update 更新索引"
                break
                ;;
            6)
                echo "取消更换APT源"
                break
                ;;
            *)
                echo "无效选择，请重新输入"
                ;;
        esac
    done
}
        
        apt-get update
        apt-get install -y ffmpeg
        # 再次检查是否安装成功
        if ! command -v ffmpeg &> /dev/null; then
            echo "ffmpeg安装失败，请手动安装"
            exit 1
        else
            echo "ffmpeg安装成功"
        fi
    else
        echo "ffmpeg已安装"
    fi
}

# 检查并安装python
check_python() {
    if ! command -v python &> /dev/null; then
        echo "Python3未安装，正在尝试安装..."
        apt-get update
        apt-get install -y python
    fi
        
        # 再次检查是否安装成功
        if ! command -v python &> /dev/null; then
            echo "Python3安装失败，请手动安装"
            exit 1
        else
            echo "Python安装成功"
        fi
    else
        echo "Python已安装"
    fi
}

# 执行检查
check_ffmpeg
check_python

echo "所有依赖检查完成，进入主程序......"
