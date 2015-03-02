FROM ianwcarlson/python-nodejs-zeromq:0.0.4
ADD ./ /usr/local/
RUN cd $EXAMPLE_DIR/ && npm install && gulp build
