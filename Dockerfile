# Should install Ubuntu Core
FROM ubuntu:14.04

# Need a better way to generate keys
ENV SRC_DIR /usr/local/src

# Base packages
RUN apt-get update
RUN apt-get install -y python3 libzmq3 python3-zmq python3-pip
RUN mkdir -p $SRC_DIR/

RUN pip3 install msgpack-python nose



