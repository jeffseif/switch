#! /bin/bash


CONFIG_PATH='./config.json' ;
DELAY_SECONDS='86400' ; # 1 Day


while true ; do
    clear ;
    date ;
    ./cli ifttt \
        --verbose \
        --verbose \
        -c "${CONFIG_PATH}" ;
    sleep "${DELAY_SECONDS}" ;
done
