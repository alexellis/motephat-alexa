FROM resin/rpi-raspbian
MAINTAINER alexellis2@gmail.com

RUN apt-get update \
    && apt-get install git python-dev python-pip gcc \
    && git clone https://github.com/pimoroni/mote-phat \
    && pip install flask \
    && cd mote-phat/library && python setup.py install \
    && apt-get -qy remove python-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/
RUN mkdir /root/alexa/
WORKDIR /root/alexa/
COPY mote.py .
COPY app.py .
EXPOSE 5000

CMD ["python", "./app.py"]
