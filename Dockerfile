FROM ubuntu:18.04

ENV TZ=Asia/Shanghai \
    PYTHONIOENCODING=utf-8

WORKDIR /app

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' > /etc/timezone

RUN apt-get update \
    && apt-get install -y apt-utils \
    && apt-get install -y python3 \
    && apt-get install -y python3-pip \
    && apt-get install -y wget \
    && apt-get install -y unzip  \
    && pip3 install requests \
    && pip3 install pydes

RUN wget https://github.com/daimiaopeng/IthomeQianDao/archive/refs/heads/master.zip \
    && unzip master.zip     

CMD [ "python3", "/app/IthomeQianDao-master/run.py" ]
