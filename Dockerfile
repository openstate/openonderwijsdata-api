FROM ubuntu:16.04
MAINTAINER Open State Foundation <developers@openstate.eu>

# Use bash as default shell
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

RUN apt-get update \
    && apt-get install -y \
        make \
        libtiff5-dev \
        libxml2-dev \
        libxslt1-dev \
        libssl-dev \
        libffi-dev \
        libjpeg8-dev \
        liblcms2-dev \
        zlib1g-dev \
        libfreetype6-dev \
        python-software-properties \
        software-properties-common \
        openjdk-8-jre-headless \
        python-dev \
        python-setuptools \
        python-pip \
        npm \
        nodejs-legacy \
        supervisor \
        git \
        curl \
        wget

# Set Dutch locale, needed to parse Dutch time data
RUN locale-gen nl_NL.UTF-8

#Set Timezone
RUN echo "Europe/Amsterdam" > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata

# Install Elasticsearch
ENV ES_VERSION 1.2.1
RUN wget https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-${ES_VERSION}.deb
RUN dpkg -i elasticsearch-${ES_VERSION}.deb > /dev/null
RUN service elasticsearch start
RUN rm elasticsearch-${ES_VERSION}.deb

WORKDIR /opt/ood
RUN pip install pip --upgrade

# Temporarily add files on the host to the container
# as it contains files needed to finish the base installation
ADD . /opt/ood

# Install Python requirements
RUN pip install -r requirements.txt

RUN npm install -g bower

# Initialize
RUN service elasticsearch start \
    && sleep 10 \
    && ./manage.py elasticsearch create_indexes es_mappings/

# Delete all files again
RUN find . -delete

CMD /opt/ood/start.sh
