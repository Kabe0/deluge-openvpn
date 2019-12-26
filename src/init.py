import os
import subprocess

print('Initializing Container')

if os.getenv('VPN_ENABLE', True):

    config = os.getenv("VPN_CONFIG", "/config/config.ovpn")     # Provided configuration details (mandatory)
    auth = os.getenv("VPN_AUTH")                                # Provided file security
    cmd = ["openvpn", "--script-security", "2", "--up", "/usr/bin/up.sh"]

    if not os.path.exists(config):
        raise Exception(f"{config} path not found. Please ensure the file exists before enabling VPN_ENABLE environment variable.")

    cmd.append("--config")
    cmd.append(config)

    if auth:
        cmd.append("--auth-user-pass")
        cmd.append(auth)

    subprocess.run(cmd)
else:
    subprocess.run(["/usr/bin/python3", "/usr/bin/run.py"])
