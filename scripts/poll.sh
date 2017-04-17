#! /bin/bash


CONFIG_PATH='./config.json' ;
DELAY_SECONDS='300' ; # 5 Minutes


while true ; do
    clear ;
    date ;
    ./cli all \
        -c "${CONFIG_PATH}" ;
    sleep "${DELAY_SECONDS}" ;
done
