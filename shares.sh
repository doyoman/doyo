#!/usr/bin/env bash

rm /ql/log/code/*.log

wait

task /ql/repo/doyoman_doyo/code.sh

wait

sed -i "1i\#!/usr/bin/env bash" /ql/log/code/*.log

