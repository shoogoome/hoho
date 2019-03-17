FROM nginx:1.13
MAINTAINER 121

WORKDIR /etc/nginx/conf.d
RUN mkdir certificate

COPY HoHoNginx.conf .
COPY ./certificate/www.r-share.cn.key ./certificate
COPY ./certificate/www.r-share.cn.pem ./certificate

