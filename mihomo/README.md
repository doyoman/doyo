## Alpine Linux 安装 mihomo

### 直连 github 安装 mihomo
```bash
wget -O - https://raw.githubusercontent.com/doyoman/doyo/refs/heads/main/mihomo/alpine-install.sh | sh
```

### 反代 github 安装 mihomo
```bash
wget -O - https://gh-proxy.com/https://raw.githubusercontent.com/doyoman/doyo/refs/heads/main/mihomo/alpine-install.sh | sh -s https://gh-proxy.com/
```

### mihomo 命令
``` bash
# 启动 mihomo
/etc/init.d/mihomo start
# 停止 mihomo
/etc/init.d/mihomo stop
# 重启 mihomo
/etc/init.d/mihomo restart
```