import os
import re
import subprocess
import socket
import netifaces
import netaddr
import pyufw
import pprint

# Based on the following documentation
# https://www.linode.com/docs/networking/vpn/vpn-firewall-killswitch-for-linux-and-macos-clients/

# Used for some of the print outputs
pp = pprint.PrettyPrinter(indent=4)

dnss = os.getenv('DNS', '8.8.8.8,8.8.4.4').split(",")

addrs = netifaces.ifaddresses('eth0')
ipinfo = addrs[socket.AF_INET][0]
address = ipinfo['addr']
netmask = ipinfo['netmask']

# Create ip object and get 
dockeraddress = netaddr.IPNetwork('%s/%s' % (address, netmask))

vpnname = None
vpnport = None

# Find the matching remote config in the config.ovpn file.
for line in open('/config/config.ovpn'):
    match = re.search('remote\s*([\w.-]*)\s*(\d*)', line)
    if match:
        vpnname = match.group(1)
        vpnport = match.group(2)
        break

# Configure the UFW default details
pyufw.reset(True)
pyufw.default("deny", "deny", "allow")
pyufw.add("allow in on tun0")
pyufw.add("allow out on tun0")

# Set the DNS configs
with open("/etc/resolv.conf", "w") as myfile:
    myfile.truncate()
    for dns in dnss:
        myfile.write(f"nameserver {dns}\n")
    myfile.close()

# Assign the docker cidr to the firewall
pyufw.add(f"allow in to {dockeraddress.cidr}")
pyufw.add(f"allow out to {dockeraddress.cidr}")

print(vpnname)
# Grab all the domain ip addresses
result = socket.getaddrinfo(vpnname, None, socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_IP, socket.AI_CANONNAME)
list = [x[4][0] for x in result]

# Assign each IP to the UFW firewall list
for vpnip in list:
    pyufw.add(f"allow out on eth0 to {vpnip} port {vpnport}")
    pyufw.add(f"allow in on eth0 from {vpnip} port {vpnport}")

# Turn on the firewall
pyufw.enable()
pp.pprint(pyufw.status())

# Run the processes
subprocess.Popen(["/usr/bin/python3", "/usr/bin/run.py"])