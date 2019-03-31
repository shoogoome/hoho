#!/bin/bash
case $1 in
    "up")
    docker-compose up -d
    ;;
    "build")
    docker-compose build
    ;;
    "down")
    docker-compose down
    ;;
    "restart")
    docker-compose restart
    ;;
    "manage")
    docker-compose exec server python3 /root/LittlePigHoHo/manage.py ${@:2}
    ;;
    "supervisor")
    docker-compose exec server supervisorctl ${@:2}
    ;;
    "bash")
    docker-compose exec $2 bash 
    ;;
    "logs")
    docker-compose logs --tail=10 -f
    ;;
    "update")
    zip -r hoho.zip LittlePigHoHo
    scp hoho.zip root@39.108.229.132:/root/hoho
    rm -rf hoho.zip
    ;;
    "collect")
    docker-compose exec server python3 /root/LittlePigHoHo/manage.py collectstatic
esac
