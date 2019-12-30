import subprocess
import os

if not os.path.exists("~/.config/deluge"):
    os.makedirs("~/.config/deluge")

webCmd = ["su", "deluge", "-c", "/usr/bin/deluge-web"]
webPort = os.getenv("WEB_PORT", None)

if webPort:
    webCmd.append("-p")
    webCmd.append(webPort)

subprocess.Popen(webCmd)
subprocess.Popen(["su", "deluge", "-c", "/usr/bin/deluged"])
