# Koh - The Face Stealer

The face scraping tool, not the infamous spirit from Avatar.

## Features

Identity-centric face datasets.

* Initialize a face dataset with a single image
* Scrape single image sources for the face
* Process video for some criteria of face collection
* Slice and dice collected data

## Initializing Face Dataset



## Building Environment

Follow this link:

[Running GUIs with Docker on Mac OSX](https://cntnr.io/running-guis-with-docker-on-mac-os-x-a14df6a76efc)

Installation:

`brew install socat`

`brew install xquartz`

Build Docker image:

`docker build -t koh .`

## Running Environment

Run this in a separate terminal to 'expose' display:

`socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"$DISPLAY\"`

```shell
export LOCAL_IP=`ifconfig en0 | grep -oE  "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" | head -1`
```

Run Docker image (while in koh repo):

```shell
docker run -it --rm \
	-v `pwd`:/koh \
	-e DISPLAY=$LOCAL_IP \
	koh /bin/bash
```
