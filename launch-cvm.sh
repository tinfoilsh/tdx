#!/bin/bash

# export KERNEL_FILE=/home/shadeform/cvmimage-v0.3.0/tinfoil-inference-v0.3.0.vmlinuz
# export INITRD_FILE=/home/shadeform/cvmimage-v0.3.0/tinfoil-inference-v0.3.0.initrd
# export IMAGE_FILE=/home/shadeform/cvmimage-v0.3.0/tinfoil-inference-v0.3.0.raw

stty intr '^]'

export KERNEL_FILE=/home/shadeform/prodimg/tinfoil-inference-v0.4.0.vmlinuz
export INITRD_FILE=/home/shadeform/prodimg/tinfoil-inference-v0.4.0.initrd
export IMAGE_FILE=/home/shadeform/prodimg/tinfoil-inference-v0.4.0.raw
# IMAGE_FILE=/home/shadeform/tdx/guest-tools/image/tdx-guest-ubuntu-24.04-generic.qcow2.llama3
./guest-tools/run_td_direct --image $IMAGE_FILE --gpus '*' --foreground

stty intr '^c'
