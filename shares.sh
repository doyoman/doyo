#!/usr/bin/env bash

rm /ql/log/code/*.log

wait 1s

task /ql/repo/doyoman_doyo/code.sh

wait 1s

sed -i "1i\#!/usr/bin/env bash"/ql/log/code/*.log

