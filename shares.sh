#!/usr/bin/env bash

rm /ql/log/code/*.log

. /ql/repo/doyoman_doyo/code.sh

sed -i "1i\#!/usr/bin/env bash"/ql/log/code/*.log

