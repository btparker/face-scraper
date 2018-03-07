FROM btparker/pyimagesearch-opencv-ubuntu
MAINTAINER Tyler Parker <btylerparker@gmail.com>

WORKDIR /koh
COPY ./requirements.txt .
RUN pip --no-cache-dir install -r ./requirements.txt

COPY . /koh
ENV PYTHONPATH /koh/src/:$PYTHONPATH
WORKDIR /koh
