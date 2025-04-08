#!/bin/sh

APP="/app"
if [ $(ls -A "$APP" | wc -l) -eq 0 ]; then
    cp -r /opt/data/* /app/
    echo "$APP 已复制"
fi

MIHOMO_UI="/app/ui"
if [ ! -d "$MIHOMO_UI" ]; then
    cp -r /opt/data/ui /app/ui
    echo "$MIHOMO_UI 已复制"
fi

/usr/bin/mihomo -d /app