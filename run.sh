#!/data/data/com.termux/files/usr/bin/bash

echo "注意：本脚本是为TERMUX定制的自动化脚本，在其它系统上安装termios库时会出错，故不要使用。"
sleep 5

# 检查当前目录下是否有bin目录和QQS程序
if [ -d "bin" ] && [ -f "bin/QQS" ]; then
    echo "检测到已存在bin目录和QQS程序，跳过安装过程，直接运行。"
    python tqqs_toolbox.py
    exit 0
else if [ -d "bin" ]; then
    echo "文件补全中，请稍后。。。。。。"
    download_and_extract() {
    # 用户可自定义的两个下载源
    SOURCE1="http://121.36.241.42"
    SOURCE2="https://file.uhsea.com"

    # 要下载的文件路径
    FILE_PATH1=":5255/d/%E8%93%9D%E5%A5%8F%E4%BA%91-%E8%B5%84%E6%BA%90%E7%AB%99%E4%B8%BB%E5%8A%9B%E5%86%9B/QQS.zip?sign=aNltwhppPRowB3qWZuwIno9DotyTUTY17sxwVArCgXc=:0"
    FILE_PATH2="/2506/5e5eb8e3e13920438986b1dbbde4812b91.zip"

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
    curl "$DOWNLOAD_URL" -o "5e5eb8e3e13920438986b1dbbde4812b91.zip"

    # 检查下载结果
    if [ $? -eq 0 ]; then
        echo "下载成功完成"
    else
        echo "下载失败，请检查网络连接(不然就是UP的链接挂了)"
        exit 1
    fi
    }
    exit 0
    fi
fi

# 更换APT源的主函数
change_apt_source() {
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
        "https://mirrors.tuna.tsinghua.edu.cn/termux/apt/termux-main/"
        "https://mirrors.bfsu.edu.cn/termux/apt/termux-main/"
        "https://mirrors.ustc.edu.cn/termux/apt/termux-main/"
        "https://mirrors.nju.edu.cn/termux/apt/termux-main/"
        "https://mirrors.aliyun.com/termux/apt/termux-main/"
    )
    
    # 显示菜单
    PS3="请使用方向键选择(1-${#sources[@]})，回车确认: "
    select opt in "${sources[@]}" "取消更换"; do
        case $REPLY in
            [1-5])
                echo "正在更换为: ${sources[$((REPLY-1))]}"
                change_source "${urls[$((REPLY-1))]}"
                echo "更换完成，开始更新索引。"
                apt update -y && apt upgrade -y
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

# 检查当前源是否为国内源
check_source() {
    local current_source
    current_source=$(grep -oP '(?<=^deb ).*' "$PREFIX/etc/apt/sources.list" | head -1)
    
    # 国内源列表
    local mirrors=(
        "https://mirrors.tuna.tsinghua.edu.cn/termux/apt/termux-main/"
        "https://mirrors.bfsu.edu.cn/termux/apt/termux-main/"
        "https://mirrors.ustc.edu.cn/termux/apt/termux-main/"
        "https://mirrors.nju.edu.cn/termux/apt/termux-main/"
        "https://mirrors.aliyun.com/termux/apt/termux-main/"
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

# 检查并安装ffmpeg
check_ffmpeg() {
    if ! command -v ffmpeg &> /dev/null; then
        echo "ffmpeg未安装，正在尝试安装..."
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
        # 再次检查是否安装成功
        if ! command -v python &> /dev/null; then
            echo "Python3安装失败，请手动安装"
            exit 1
        else
            echo "Python安装成功，开始安装程序依赖"
            apt install python3-pip -y
            pip config set global.index-url https://mirrors.aliyun.com/pypi/simple
        fi
    else
        echo "Python已安装"
    fi
}

# 获取延迟时间（单位：毫秒）
get_latency() {
    local host
    # 从URL中提取主机名
    host=$(echo "$1" | awk -F/ '{print $3}')
    
    # 执行ping测试并提取延迟
    ping -c 1 "$host" | awk -F'=' '/time=/ {print $NF}' | awk '{print $1}' 2>/dev/null
}

# 检查并安装zip和unzip工具
check_zip_tools() {
    if ! command -v zip &> /dev/null; then
        echo "检测到zip工具未安装，正在安装..."
        apt-get update
        apt-get install -y zip
        echo "zip工具安装完成"
    else
        echo "zip工具已安装"
    fi

    if ! command -v unzip &> /dev/null; then
        echo "检测到unzip工具未安装，正在安装..."
        apt-get update
        apt-get install -y unzip
        echo "unzip工具安装完成"
    else
        echo "unzip工具已安装"
    fi
}

# 处理ZIP文件
process_zip_file() {
    local zip_file="5e5eb8e3e13920438986b1dbbde4812b91.zip"
    
    if [ ! -f "$zip_file" ]; then
        echo "未找到ZIP文件: $zip_file"
        return 1
    fi
    
    echo "检测到ZIP文件: $zip_file"
    
    # 创建bin目录
    if [ ! -d "bin" ]; then
        echo "创建bin目录..."
        mkdir bin
    fi
    
    # 解压文件到bin目录
    echo "正在解压文件到bin目录..."
    unzip -q "$zip_file" -d bin/
    
    # 检查解压结果
    if [ $? -ne 0 ]; then
        echo "解压失败，请检查ZIP文件是否损坏"
        return 1
    fi
    
    # 删除原始ZIP文件
    echo "删除原始ZIP文件..."
    rm -f "$zip_file"
    
    # 验证文件是否已删除
    if [ -f "$zip_file" ]; then
        echo "警告: 未能成功删除ZIP文件"
        return 1
    fi
    
    echo "操作完成: ZIP文件已解压到bin目录并删除"
}

# 下载和解压主程序
download_and_extract() {
    # 用户可自定义的两个下载源
    SOURCE1="http://121.36.241.42"
    SOURCE2="https://file.uhsea.com"

    # 要下载的文件路径
    FILE_PATH1=":5255/d/%E8%93%9D%E5%A5%8F%E4%BA%91-%E8%B5%84%E6%BA%90%E7%AB%99%E4%B8%BB%E5%8A%9B%E5%86%9B/QQS.zip?sign=aNltwhppPRowB3qWZuwIno9DotyTUTY17sxwVArCgXc=:0"
    FILE_PATH2="/2506/5e5eb8e3e13920438986b1dbbde4812b91.zip"

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
    curl "$DOWNLOAD_URL" -o "5e5eb8e3e13920438986b1dbbde4812b91.zip"

    # 检查下载结果
    if [ $? -eq 0 ]; then
        echo "下载成功完成"
    else
        echo "下载失败，请检查网络连接(不然就是UP的链接挂了)"
        exit 1
    fi

    # 检查并安装zip工具
    check_zip_tools

    # 处理ZIP文件
    process_zip_file
}

# 主安装流程
echo "开始安装过程..."
change_apt_source
check_ffmpeg
check_python
download_and_extract

# 链接主程序
chmod +x run.sh
cp run.sh run

# 创建链接以便快速启动程序
ln -l run $PREFIX/bin

# 赋予运行权限并启动
cd bin
chmod +x QQS
./QQS
python ../tqqs_toolbox.py
