# Should install Ubuntu Core
FROM ubuntu:14.04

# Need a better way to generate keys
ENV SVN_SRV http://linux01.stolarhorizon.com/svn/
ENV SVN_REPO gradSW/trunk/
ENV EMG_REPO emg/pythonPostProcess
ENV SRC_DIR /usr/local/src

# Base packages
RUN apt-get update
RUN apt-get install -y subversion wget build-essential #openssh-server
RUN apt-get install -y python3 #python3-setuptools

RUN apt-get install -y libzmq3 python3-zmq
RUN mkdir -p $SRC_DIR/scripts
#ADD ./src/ $SRC_DIR/

#RUN mkdir /var/run/sshd
#RUN echo 'root:screencast' | chpasswd
#RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
#RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

#ENV NOTVISIBLE "in users profile"
#RUN echo "export VISIBLE=now" >> /etc/profile

#EXPOSE 22
#CMD ["/usr/sbin/sshd", "-D"]


# Build and install ZeroMQ
#RUN wget http://download.zeromq.org/zeromq-4.1.0-rc1.tar.gz
#RUN tar zxf zeromq-4.1.0-rc1.tar.gz
#RUN cd zeromq-4.1.0 && ./configure && make -j4 && make install

#RUN cd $SRC_DIR && svn checkout $SVN_SRV/$EMG_REPO --username $SVN_USER --password $SVN_PASS --non-interactive
#RUN cd $SRC_DIR && svn checkout $SVN_SRV/$GRADSW_REPO --username $SVN_USER --password $SVN_PASS --non-interactive

