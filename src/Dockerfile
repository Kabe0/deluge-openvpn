FROM ubuntu:18.04

LABEL maintainer="kabe0"

# environment settings
ARG DEBIAN_FRONTEND="noninteractive"
ENV HOME="/config"
ENV DNS="8.8.8.8,8.8.4.4"

ENV WEB_PORT=8112

ENV VPN_ENABLE=true
ENV VPN_CONFIG="/config/config.ovpn"
ENV VPN_AUTH="/config/auth.conf"

# add repo and install qbitorrent
RUN \
 echo "***** add qbitorrent repositories ****" && \
 apt-get update && \
 apt-get install -y \
 software-properties-common --no-install-recommends && \
 LC_ALL=C.UTF-8 add-apt-repository -y ppa:deadsnakes/ppa && \
 apt-get update && \
 apt-get install -y \
	python3 python3-pip ufw openvpn deluged deluge-web deluge-console && \
	# Dev tools nano dnsutils iputils-ping lsof
 echo "**** cleanup ****" && \
 apt-get clean && \
 python3 -m pip install netifaces netaddr pyufw psutil && \
 rm -rf \
  /tmp/* \
  /var/lib/apt/lists/* \
  /var/tmp/* && \
 apt-get autoremove && \
 apt-get clean && \
 apt-get purge -y \
    software-properties-common

# ports and volumes
EXPOSE 8112 6881/udp
VOLUME /config /downloads
COPY init.py up.sh up.py run.py /usr/bin/

CMD /usr/bin/python3 /usr/bin/init.py
