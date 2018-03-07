FROM btparker/pyimagesearch-opencv-ubuntu
MAINTAINER Tyler Parker <btylerparker@gmail.com>

WORKDIR /tmp
COPY ./apt_requirements.txt .
RUN apt-get update && \
    apt-get install -y $(cat apt_requirements.txt)
COPY ./requirements.txt .
RUN pip --no-cache-dir install -r ./requirements.txt

COPY . /koh
ENV PYTHONPATH /koh/src/:$PYTHONPATH
ENV PATH /koh/bin/:$PATH
WORKDIR /koh
