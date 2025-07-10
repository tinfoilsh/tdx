#!/bin/bash

sudo pkill socat
stty raw -echo intr '^]'
socat -,raw,echo=0 UNIX-CONNECT:/tmp/tdx-guest-console
reset
