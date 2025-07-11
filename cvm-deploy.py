#!/usr/bin/env python3

import os
import json
import hashlib
import requests
import base64
from pathlib import Path
import yaml

debug = True

repo = "tinfoilsh/confidential-llama3-3-70b-fp8"
external_config = {
    "domain": "example.com"
}

url = f"https://api.github.com/repos/{repo}/releases/latest"
response = requests.get(url)
response.raise_for_status()
latest_release = response.json()["tag_name"]

deployment_dir = Path("deployments") / repo.replace("/", "-") / latest_release
deployment_dir.mkdir(parents=True, exist_ok=True)
deployment_json = deployment_dir / "tinfoil-deployment.json"

if not deployment_json.exists():
    url = f"https://github.com/{repo}/releases/download/{latest_release}/tinfoil-deployment.json"
    response = requests.get(url)
    response.raise_for_status()
    deployment_json.write_bytes(response.content)

with open(deployment_json) as f:
    deployment_data = json.load(f)

with open(deployment_dir / "external-config.yml", "w") as f:
    yaml.dump(external_config, f)

config_yml = deployment_dir / "config.yml"
config_content = base64.b64decode(deployment_data["config"])
config_yml.write_bytes(config_content)

cmdline = deployment_data["cmdline"]
expected_hash = next(h.split("=")[1] for h in cmdline.split() if h.startswith("tinfoil-config-hash="))

with open(config_yml, 'rb') as f:
    actual_hash = hashlib.sha256(f.read()).hexdigest()
if expected_hash != actual_hash:
    print("Config hash mismatch")
    exit(1)
print("Config hash matches", actual_hash)

with open(config_yml) as f:
    config = yaml.safe_load(f)
cvm_version = config["cvm-version"]

if debug:
    print("---- WARNING: DEBUG MODE ----")
    cmdline += " tinfoil-debug=on"

home = Path.home()
prodimg = home / "prodimg"
os.environ.update({
    "KERNEL_FILE": str(prodimg / f"tinfoil-inference-v{cvm_version}.vmlinuz"),
    "INITRD_FILE": str(prodimg / f"tinfoil-inference-v{cvm_version}.initrd"),
    "TD_IMG": str(prodimg / f"tinfoil-inference-v{cvm_version}.raw"),
    "CONFIG_DIR": str(deployment_dir),
    "MEMORY": str(config["memory"]),
    "CPUS": str(config["cpus"]),
    "CMDLINE": cmdline,
})

cmd = f"guest-tools/run_td_direct"

model_disks = []
for model in config["models"]:
    print(f"Adding model disk: {model['repo']}")
    disk = f"/opt/tinfoil/modelpack/output/{model['repo'].replace('@', '/')}.mpk"
    model_disks.append(disk)
    if not os.path.exists(disk):
        print(f"Model disk {disk} not found")
        exit(1)

os.environ.update({"MODEL_DISKS": ",".join(model_disks)})

if config["gpus"] == "full":
    cmd += " --gpus '*'"
else:
    print("WARNING: GPUs not specified")

print(cmd)
os.system(cmd)
