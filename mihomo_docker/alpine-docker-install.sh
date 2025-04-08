#!/usr/bin/sh

ARCH_TAG="arm64"

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

MIHOMO_PKG=mihomo-linux-$ARCH_TAG-$LATEST_TAG

rm -rf /tmp/mihomo*
wget -O /tmp/$MIHOMO_PKG.gz ${PROXY_URL}https://github.com/MetaCubeX/mihomo/releases/download/$LATEST_TAG/$MIHOMO_PKG.gz
if [ $? -ne 0 ]; then
    echo -e "mihomo下载出错。"
    exit 1
fi

MIHOMO_BIN="./bin"
if [ ! -d "$MIHOMO_BIN" ]; then
    mkdir -p "$MIHOMO_BIN"
    echo "文件夹 $MIHOMO_BIN 已创建。"
else
    echo "文件夹 $MIHOMO_BIN 已存在。"
fi

gzip -d /tmp/$MIHOMO_PKG.gz
mv /tmp/$MIHOMO_PKG ./bin/mihomo
chmod +x ./bin/mihomo
rm -rf /tmp/mihomo*

MIHOMO_DIR="./data"
if [ ! -d "$MIHOMO_DIR" ]; then
    mkdir -p "$MIHOMO_DIR"
    echo "文件夹 $MIHOMO_DIR 已创建。"
else
    echo "文件夹 $MIHOMO_DIR 已存在。"
fi
wget -O $MIHOMO_DIR/config.yaml ${PROXY_URL}https://raw.githubusercontent.com/MetaCubeX/Meta-Docs/refs/heads/main/docs/example/mrs
if [ $? -ne 0 ]; then
    echo -e "config.yaml 下载失败。"
fi

UI_TAG=$(wget -qO- https://api.github.com/repos/MetaCubeX/metacubexd/releases/latest | jq -r .tag_name)
if [ -z "$UI_TAG" ]; then
    UI_TAG="v1.152.0"
    echo "无法获取最新的 UI tag，采用默认 tag：$UI_TAG"
else
    echo "获取到最新的 UI tag: $UI_TAG"
fi

UI_DIR="$MIHOMO_DIR/ui"
if [ ! -d "$UI_DIR" ]; then
    mkdir -p "$UI_DIR"
    echo "文件夹 $UI_DIR 已创建。"
else
    echo "文件夹 $UI_DIR 已存在。"
fi
wget -O /tmp/compressed-dist.tgz ${PROXY_URL}https://github.com/MetaCubeX/metacubexd/releases/download/${UI_TAG}/compressed-dist.tgz
if [ $? -ne 0 ]; then
    echo -e "metacubexd ui 下载失败。"
else
    tar -zxf /tmp/compressed-dist.tgz -C $UI_DIR
    echo "metacubexd ui 下载完成！"
    rm /tmp/compressed-dist.tgz
fi

echo -e "over~"
