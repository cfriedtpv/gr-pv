title: The Per Vices OOT Module
brief: Python and GRC Bindings for Per Vices' version of UHD USRP Blocks
tags: # Tags are arbitrary, but look at CGRAN what other authors are using
  - sdr
author:
  - Christopher Friedt <chris.f@pervices.com>
copyright_owner:
  - Copyright Owner Per Vices Corporation
license: GPLv3
repo: https://github.com/pervices/gr-pv
website: https://www.pervices.com
#icon: <icon_url> # Put a URL to a square image here that will be used as an icon on CGRAN
---
git clone https://github.com/pervices/gr-pv
mkdir -p gr-pv-build
cd gr-pv-build
cmake -DCMAKE_INSTALL_PREFIX=/usr ../gr-pv
make
make DESTDIR=${PWD}/../gr-pv-install install
