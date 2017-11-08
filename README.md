# [Unsupported] python-zeromq-pubsub
Microservice oriented starter project using ZeroMQ sockets and publish/subscribe pattern for distributed applications.  

The basic idea is to simplify the ZeroMQ interface by wrapping the publish/subscribe details and providing a standardize message format as it arrives to the subscriber.  The internal transport can be defined via configuration file fed to the process manager.  The serialized data protocol is currently [MessagePack](http://msgpack.org/) not JSON, since it's leaner.

I think one can get a lot of mileage from the pub/sub pattern.  It supports complex network topologies with the ability to filter and buffer data in between nodes.

After using a few different frameworks, I've come to realize that I will probably continuing using different frameworks as everything evolves.  The microservice approach, as well as using a framework agnostic middleware like ZeroMQ, better facilitates this philosophy because each service just acts like an independent networked (TCP or IPC) node.  So, for example, all the CPU-bound tasks can be done in Python, and all the web serving tasks in Node, or every permutation you can think of.  There may be no good reason to throw away good code just because it's not written in a hip new language.   

This repo is also my experiment with Docker.  Besides all the obvious benefits of Docker, utilizing the (Docker) image also simplifies the dependency setup required to run everything.

# Installation
- Install [Docker](https://docs.docker.com/installation/)
- Install [Git](http://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- Git clone this repo `git clone https://github.com/ianwcarlson/python-zeromq-pubsub` in your development directory
- Then start the Docker daemon `boot2docker start` if you're using boot2docker.  You may need to export the environment variables when prompted.  You can add them your ~/.bashrc in Linux or ~/.bash_profile in Mac.  The image is built for x86_64 architecture.  
- Then `docker pull ianwcarlson/python-nodejs-zeromq:0.0.4`, which should download the built image.  This may take a few minutes if it's your first time downloading the Ubuntu 14.04 base image.
- To run the container you'll need mount the project root directory on your host to the /usr/local/ in the container.  Something like `docker run --rm=true -i -t -v <path to project root>:/usr/local ianwcarlson/python-nodejs-zeromq:0.0.4 python3 /usr/local/test/testZeroMQInterface.py`.  I like to remove the stopped container when it's done via the `--rm=true` option for development.  Ideally you'd want to spin a multiple containers for each major process, but then I think you can only use TCP sockets instead of IPC.  

Once boot2docker is running correctly, you can run the example geofencing app with the following command: 
`docker run --rm=true -p 3698:3698 ianwcarlson/geofencing-demo:0.0.1 python3 /usr/local/examples/geofencing/main.py` and open a browser up to <boot2docker ip>:3698.  The boot2docker ip can be found via `boot2docker ip` command.

Project is still a work in process in my spare time as I'm evaluating ZeroMQ.  I noticed a few quirks already with ZeroMQ.  If the publisher starts spamming messages right away, then all or most are lost.  I think the messages won't get buffered until ZeroMQ has established a connection.  By initially waiting a few seconds, I've been able to reliably send/receive all messages.

