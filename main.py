#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
from max.run import main_run

cmd = sys.argv.pop(1)

if cmd in ["max"]:
    main_run()

else:
   print("Miss debugging type.", "RED")

