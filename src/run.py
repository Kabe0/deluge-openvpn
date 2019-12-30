import subprocess
import os

if not os.path.exists("~/.config/deluge"):
    os.makedirs("~/.config/deluge")

DEL_UID = os.getenv("DEL_UID", 1000)
DEL_GID = os.getenv("DEL_GID", 1000)

if DEL_UID != 1000:
    subprocess.run(["/usr/sbin/usermod", "-u", f"{DEL_UID}", "deluge"])
if DEL_GID != 1000:
    subprocess.run(["/usr/sbin/groupmod", "-g", f"{DEL_GID}", "deluge"])

webCmd = ["su", "deluge", "-c", "/usr/bin/deluge-web"]
webPort = os.getenv("WEB_PORT", None)

if webPort:
    webCmd.append("-p")
    webCmd.append(webPort)

subprocess.Popen(webCmd)
subprocess.Popen(["su", "deluge", "-c", "/usr/bin/deluged"])
