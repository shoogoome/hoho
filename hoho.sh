#!/bin/bash

basepath=$(cd `dirname $0`; pwd)'/images'
case $1 in
    "build")
    # server
    docker build -t hoho-server ${basepath}'/server'
    docker build -t hoho-mysql ${basepath}'/mysql'
    docker build -t hoho-redis ${basepath}'/redis'
    docker build -t hoho-redis-secondary ${basepath}'/hoho-redis-secondary'
    docker build -t hoho-web ${basepath}'/web'
    ;;
    "up")
    if [ $2 == "dev" ]
    then
        docker stack deploy --compose-file docker-stack-dev.yml 'hoho'
    else
        docker stack deploy --compose-file docker-stack.yml 'hoho'
    fi
    ;;
    "down")
    docker stack rm 'hoho'
    ;;
    "ps")
    docker stack ps 'hoho'
    ;;
    "service")
    docker stack services 'hoho'
    ;;
    "update")
    zip -r hoho.zip LittlePigHoHo
    scp hoho.zip root@39.108.229.132:/root/hoho
    rm -rf hoho.zip
    ;;
    "pass")
    zip -r LittlePigHoHo.zip /Users/lzl/Documents/project/LittlePigHoHo /Users/lzl/Documents/project/redis-cluster
    scp LittlePigHoHo.zip root@39.108.229.132:/root
    rm -rf LittlePigHoHo.zip
esac 