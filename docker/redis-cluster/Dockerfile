FROM ubuntu:focal

RUN apt-get update && apt-get install -y build-essential wget \
  && wget https://download.redis.io/releases/redis-6.2.6.tar.gz \
  && tar xzf redis-6.2.6.tar.gz \
  && cd redis-6.2.6 && make && make install \
  && cd .. \
  && rm redis-6.2.6.tar.gz \
  && rm -r redis-6.2.6 \
  && apt-get remove -y build-essential wget 

WORKDIR redis-conf

COPY redis_cluster.conf .
COPY hosts2ip.sh .

ENTRYPOINT ["redis-server"]
