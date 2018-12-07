#!/usr/bin/env python
# -*- coding: utf-8 -*-


import subprocess
subprocess.call('pip install pipreqs',shell=True)
subprocess.call('pipreqs --force ./',shell=True)
subprocess.call('pip install -r requirements.txt',shell=True)