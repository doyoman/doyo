#!/bin/sh

if ! grep -qi 'alpine' /etc/os-release; then
    echo "此脚本仅支持 Alpine Linux，当前系统不支持。"
    exit 1
fi

echo "当前系统为 Alpine Linux，继续执行脚本..."

apk update
apk add jq

ARCH=$(uname -m)
case $ARCH in
    x86_64)
        ARCH_TAG="amd64"
        ;;
    i386)
        ARCH_TAG="386"
        ;;
    arm64)
        ARCH_TAG="arm64"
        ;;
    *)
        echo "不支持的架构: $ARCH"
        exit 1
        ;;
esac

LATEST_TAG=$(curl -s https://api.github.com/repos/MetaCubeX/mihomo/releases/latest | jq -r .tag_name)

if [ -z "$LATEST_TAG" ]; then
    echo "无法获取最新的 tag"
    exit 1
fi

echo "最新的 tag: $LATEST_TAG"

wget -O /tmp/mihomo.gz https://github.com/MetaCubeX/mihomo/releases/download/$LATEST_TAG/mihomo-linux-$ARCH_TAG-compatible-go120-$LATEST_TAG.gz
gzip -d /tmp/mihomo.gz
mv mihomo /usr/bin/mihomo
chmod +x /usr/bin/mihomo

mihomo -v
if [ $? -ne 0 ]; then
    echo "mihomo安装出错。请重试！"
    exit 1
fi

wget -O /etc/init.d/mihomo https://raw.githubusercontent.com/doyoman/doyo/refs/heads/main/mihomo/init.d/mihomo
chmod +x /etc/init.d/mihomo

if [ $? -ne 0 ]; then
    echo "init.d 脚本安装出错。请重试！"
    exit 1
fi

rc-update add mihomo default
rc-status | grep mihomo

echo "现在把你的 mihomo 配置文件(config.yaml)放到 /etc/mihomo/ 路径下，然后用以下命令启动\n /etc/init.d/mihomo start\n 即可享用！"