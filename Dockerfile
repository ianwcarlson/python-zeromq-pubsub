# Should install Ubuntu Core
FROM ubuntu:14.04

# Need a better way to generate keys
ENV SRC_DIR /usr/local/src
ENV EXAMPLE_DIR /usr/local/examples/geofencing/webServer
RUN LEAFLET leaflet-0.7.3

# Base packages
RUN apt-get update
RUN apt-get install -y python3 libzmq3-dev python3-zmq python3-pip
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN mkdir -p $SRC_DIR/

RUN pip3 install msgpack-python nose
RUN pip3 install jsonschema 

# To run examples
RUN pip3 install gpxpy
# Install pre 0.10 Node because zmq package needs it
# Node compiler needs python2.x
RUN apt-get install -y python wget build-essential
RUN wget http://nodejs.org/dist/v0.10.30/node-v0.10.30.tar.gz
RUN tar -xvf node-v0.10.30.tar.gz
RUN cd node-v0.10.30 && ./configure && make && make install

RUN cd $EXAMPLE_DIR/ && npm install

#RUN apt-get install -y node



