#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
查询app路径
"""

import os

def find_app(folder_path):
    app_path = ''
    for file in os.listdir(folder_path):
        if file.startswith('app_'):
            app_path = os.path.join(folder_path,file)
            print 'app路径:{}'.format(app_path)
            break
    return app_path
