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
aarch64)
    ARCH_TAG="arm64"
    ;;
*)
    echo "不支持的架构: $ARCH"
    exit 1
    ;;
esac

if [ -z "$1" ]; then
    echo "自定义 GitHub 反代 url 不存在，将直连GitHub。"
else
    if [[ "$1" == */ ]]; then
        PROXY_URL=$1
    else
        PROXY_URL="$1/"
    fi
    echo "自定义 GitHub 反代 url：$PROXY_URL"
fi

LATEST_TAG=$(wget -qO- https://api.github.com/repos/MetaCubeX/mihomo/releases/latest | jq -r .tag_name)

if [ -z "$LATEST_TAG" ]; then
    LATEST_TAG="v1.19.0"
    echo "无法获取最新的 tag，采用默认 tag：$LATEST_TAG"
else
    echo "获取到最新的 tag: $LATEST_TAG"
fi

MIHOMO_PKG=mihomo-linux-$ARCH_TAG-compatible-go120-$LATEST_TAG

rm -rf /tmp/mihomo*
wget -O /tmp/$MIHOMO_PKG.gz ${PROXY_URL}https://github.com/MetaCubeX/mihomo/releases/download/$LATEST_TAG/$MIHOMO_PKG.gz
if [ $? -ne 0 ]; then
    echo -e "mihomo安装出错。或许是你的网络环境不行，使用 GitHub 反代运行脚本试试！只需在脚本后增加反代url参数即可！\n免费公共反代：\nhttps://gh-proxy.com/"
    exit 1
fi

gzip -d /tmp/$MIHOMO_PKG.gz
mv /tmp/$MIHOMO_PKG /usr/bin/mihomo
chmod +x /usr/bin/mihomo
rm -rf /tmp/mihomo*
mihomo -v

wget -O /etc/init.d/mihomo ${PROXY_URL}https://raw.githubusercontent.com/doyoman/doyo/refs/heads/main/mihomo/init.d/mihomo
if [ $? -ne 0 ]; then
    echo -e "init.d 脚本安装出错。或许是你的网络环境不行，使用 GitHub 反代运行脚本试试！只需在脚本后增加反代url参数即可！\n免费公共反代：\nhttps://gh-proxy.com/"
    exit 1
fi

chmod +x /etc/init.d/mihomo

rc-update add mihomo default
rc-status | grep mihomo

echo -e "现在把你的 mihomo 配置文件(config.yaml)放到 /etc/mihomo/ 路径下，然后用以下命令启动\n /etc/init.d/mihomo start\n即可享用！"
