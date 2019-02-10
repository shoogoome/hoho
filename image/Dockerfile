FROM ubuntu:16.04
MAINTAINER 121

RUN sed -i 's/http:\/\/archive\.ubuntu\.com\/ubuntu\//http:\/\/mirrors\.163\.com\/ubuntu\//g' /etc/apt/sources.list 
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 \
    python3-pip \
    supervisor \
    vim 
COPY requirements.txt /tmp/
RUN pip3 install -i https://pypi.douban.com/simple -r /tmp/requirements.txt

RUN echo "nameserver 114.114.114.114" >> /etc/resolve.conf

COPY HoHo.conf /etc/supervisor/conf.d/
EXPOSE 8000
ENV LANG zh_CN.UTF-8
# COPY init.py /root/
CMD [ "supervisord", "-n", "-c", "/etc/supervisor/supervisord.conf" ]

