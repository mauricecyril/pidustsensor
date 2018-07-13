#!/bin/sh

curl https://get.pimoroni.com/i2c | bash
cd ~


git clone https://github.com/pimoroni/bme680
cd bme680/library

sudo python3 setup.py install
