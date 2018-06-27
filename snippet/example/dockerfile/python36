# Python 3.6 Dockerfile

# Builder
FROM centos:7 as builder
LABEL maintainer "xgfone@126.com"

ENV ROOT=/root

RUN yum groupinstall -y 'Development Tools'
RUN yum install -y openssl-devel zlib-devel sqlite-devel readline-devel wget

# Install Python 3.6
RUN wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz -P /root
RUN tar xf $ROOT/Python-3.6.5.tgz -C $ROOT
WORKDIR $ROOT/Python-3.6.5
RUN ./configure --enable-optimizations
RUN make install

# Update pip3
RUN pip3 install --upgrade pip


# Python 3.6 Image
FROM centos:7

ENV ROOT=/root

RUN yum install -y wget curl tcpdump net-tools telnet vim nc mtr strace ltrace lsof htop iotop
RUN yum install -y openssl zlib sqlite readline

COPY --from=builder /usr/local/bin/python3* /usr/local/bin/
COPY --from=builder /usr/local/include/python3.6m /usr/local/include/python3.6m
COPY --from=builder /usr/local/lib/python3.6 /usr/local/lib/python3.6
COPY --from=builder /usr/local/share/man/man1/python3.6* /usr/local/share/man/man1/
COPY --from=builder /usr/local/bin/pip3* /usr/local/bin/

# Reset the work directory.
WORKDIR $ROOT
