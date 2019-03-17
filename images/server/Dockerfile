FROM ubuntu:16.04
MAINTAINER 121

RUN sed -i 's/http:\/\/archive\.ubuntu\.com\/ubuntu\//http:\/\/mirrors\.ustc\.edu\.cn\/ubuntu\//g' /etc/apt/sources.list 

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 \
    python3-pip \
    supervisor iputils-ping  \
    vim mysql-client
COPY requirements.txt /tmp/
RUN pip3 install -i https://pypi.douban.com/simple -r /tmp/requirements.txt

# hoho配置
COPY HoHo.conf /etc/supervisor/conf.d/
# 数据库自动备份
COPY backups.py /
COPY backups.conf /etc/supervisor/conf.d/

EXPOSE 8000
ENV LANG zh_CN.UTF-8
CMD [ "supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf" ]

