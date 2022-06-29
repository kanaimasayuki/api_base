#    API_BASE用のdockerfile
#    (C) Masayuki Kanai 2022/02/22

FROM ubuntu:focal

RUN DEBIAN_FRONTEND=noninteractive &&\
    apt update --fix-missing &&\
    apt upgrade -y  &&\
    apt install -y --no-install-recommends \
        apt-utils \
        locales \
        tzdata &&\
    ln -fs /usr/share/zoneinfo/Asia/Tokyo /etc/localtime &&\
    dpkg-reconfigure --frontend noninteractive tzdata &&\
    locale-gen ja_JP.UTF-8 &&\
    localedef -f UTF-8 -i ja_JP ja_JP.utf8

ENV LANG=ja_JP.UTF-8 \
    LANGUAGE=ja_JP:ja \
    LC_ALL=ja_JP.UTF-8 \
    TERM=screen-256color

RUN apt update && apt install -y --no-install-recommends --fix-missing \
    vim \
    python3-apt \
    sudo \
    curl \
    cron \
    python3 \
    python3-pip &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

WORKDIR /data/project
COPY requirements.txt /data/project
RUN pip install -r requirements.txt && rm -r ~/.cache/pip

CMD ["python3","api.py"]