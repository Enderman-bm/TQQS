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

# 执行主函数
main

        apt-get update
        apt-get install -y ffmpeg
        # 再次检查是否安装成功
        if ! command -v ffmpeg &> /dev/null; then
            echo "ffmpeg安装失败，请手动安装"
            exit 1
        else
            echo "ffmpeg安装成功"
        fi
        echo "ffmpeg已安装"
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
        echo "Python已安装"
}

# 执行检查
check_ffmpeg
check_python

echo "所有依赖检查完成，开始下载主程序......"

#!/bin/bash

# 用户可自定义的两个下载源（请在此处填入实际的网站域名）
SOURCE1="http://ecs-121-36-241-42.compute.hwclouds-dns.com"
SOURCE2="https://file.uhsea.com"

# 要下载的文件路径（请在此处填入实际的文件路径）
FILE_PATH1="/d/%E8%93%9D%E5%A5%8F%E4%BA%91-%E8%B5%84%E6%BA%90%E7%AB%99%E4%B8%BB%E5%8A%9B%E5%86%9B/QQS.zip?sign=aNltwhppPRowB3qWZuwIno9DotyTUTY17sxwVArCgXc=:0"
FILE_PATH2="/2506/5e5eb8e3e13920438986b1dbbde4812b91.zip"

# 获取延迟时间（单位：毫秒）
get_latency() {
    local host
    # 从URL中提取主机名
    host=$(echo "$1" | awk -F/ '{print $3}')
    
    # 执行ping测试并提取延迟
    ping -c 1 "$host" | awk -F'=' '/time=/ {print $NF}' | awk '{print $1}' 2>/dev/null
}

# 获取两个源的延迟
LATENCY1=$(get_latency "$SOURCE1")
LATENCY2=$(get_latency "$SOURCE2")

# 检查是否获取到有效延迟
if [ -z "$LATENCY1" ]; then
    LATENCY1=9999
fi

if [ -z "$LATENCY2" ]; then
    LATENCY2=9999
fi

# 比较延迟并选择最佳源
if [ "$LATENCY1" -lt "$LATENCY2" ]; then
    SELECTED_SOURCE="$SOURCE1"
    SELECTED_PATH="$FILE_PATH1"
    echo "选择源1 (延迟: ${LATENCY1}ms < 源2: ${LATENCY2}ms)"
else
    SELECTED_SOURCE="$SOURCE2"
    SELECTED_PATH="$FILE_PATH2"
    echo "选择源2 (延迟: ${LATENCY2}ms < 源1: ${LATENCY1}ms)"
fi

# 执行下载
DOWNLOAD_URL="${SELECTED_SOURCE}${SELECTED_PATH}"
echo "开始下载: $DOWNLOAD_URL"
curl -O "$DOWNLOAD_URL"

# 检查下载结果
if [ $? -eq 0 ]; then
    echo "下载成功完成"
else
    echo "下载失败，请检查网络连接或URL"
fi
