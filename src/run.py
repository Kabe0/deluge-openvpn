import subprocess
import os

webComd = ["/usr/bin/deluge-web"]
webPort = os.getenv("WEB_PORT", None)

if webPort:
    webComd.append("-p")
    webComd.append(webPort)

subprocess.Popen(webComd)
subprocess.Popen(["/usr/bin/deluged"])
