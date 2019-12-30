FROM ubuntu:18.04

LABEL maintainer="kabe0"

# environment settings
ARG DEBIAN_FRONTEND="noninteractive"
ENV HOME="/config"

ENV WEB_PORT=8112
ENV DEL_PORT=58846
ENV DEL_UID=1000
ENV DEL_GID=1000

ENV VPN_DNS="8.8.8.8,8.8.4.4"
ENV VPN_ENABLE=True
ENV VPN_CONFIG="/config/config.ovpn"
ENV VPN_AUTH="/config/auth.conf"
ENV USE_UFW=False


# add repo and install qbitorrent
RUN \
 apt-get update && \
 apt-get install -y \
 software-properties-common --no-install-recommends && \
 LC_ALL=C.UTF-8 add-apt-repository -y ppa:deadsnakes/ppa && \
 apt-get update && \
 apt-get install -y \
	python3 python3-pip ufw openvpn deluged deluge-web deluge-console && \
	# Dev tools nano dnsutils iputils-ping lsof
 python3 -m pip install netifaces netaddr pyufw psutil && \
 apt-get clean && \
 rm -rf \
  /tmp/* \
  /var/lib/apt/lists/* \
  /var/tmp/* && \
 apt-get autoremove && \
 apt-get clean && \
 apt-get purge -y \
    software-properties-common && \
 useradd -m -d $HOME deluge

# ports and volumes
EXPOSE 8112 6881/udp
VOLUME /config /downloads
COPY init.py up.sh up.py run.py /usr/bin/

CMD /usr/bin/python3 /usr/bin/init.py
