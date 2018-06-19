FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential git vim curl
#RUN pip3 install --upgrade pip && pip3 install --no-binary :all:  --no-cache-dir cython

COPY requirements.txt .
RUN pip3 install -r requirements.txt

