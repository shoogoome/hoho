#!/bin/bash

basepath=$(cd `dirname $0`; pwd)'/images'
case $1 in
    "build")
    # web
    docker build -t hoho-web ${basepath}'/web'
    # server
    docker build -t hoho-server ${basepath}'/server'
    # mysql
    docker build -t hoho-mysql ${basepath}'/mysql'
    # redis
    docker build -t hoho-redis ${basepath}'/redis'
    # redis-secondary
    docker build -t hoho-redis-secondary ${basepath}'/redis-secondary'
    ;;
    "up")
    docker stack deploy --compose-file docker-stack.yml 'hoho'
    ;;
    "down")
    docker stack rm 'hoho'
    ;;
    "ps")
    docker stack ps 'hoho'
    ;;
    "service")
    docker stack service 'hoho'
esac 