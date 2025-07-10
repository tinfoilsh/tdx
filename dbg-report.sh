#!/bin/bash
set -ex

uname -a
dkms status
cat /proc/cmdline 
apt-cache policy linux-image-6.8.0-62-generic
apt-cache policy nvidia-driver-570-open
apt-cache policy nvidia-fabricmanager-570
journalctl -u nvidia-fabricmanager --no-pager | tail -n 20
lsb_release -a
cat /etc/apt/sources.list.d/kobuk-team-ubuntu-tdx-release-noble.sources 
lspci | grep -i nvidia
nvidia-smi

# check lkca