FROM ubuntu:16.04
MAINTAINER 121

RUN sed -i 's/http:\/\/archive\.ubuntu\.com\/ubuntu\//http:\/\/mirrors\.163\.com\/ubuntu\//g' /etc/apt/sources.list 
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y nfs-kernel-server runit inotify-tools vim

RUN mkdir exports
RUN echo '/exports *(rw,sync,no_subtree_check,fsid=0,no_root_squash)' >> /etc/exports

RUN exportfs -r
RUN service rpcbind start

CMD ["service",  "nfs-kernel-server", "start"]