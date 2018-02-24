# -*- coding: utf-8; -*-

import os

cfgfile = os.path.join(os.environ.get('VIRTUAL_ENV') or '/', 'etc/production.conf')

def readCfg(filename):
    import configparser
    config = configparser.ConfigParser(interpolation=None)
    config.read(filename, encoding="utf8")
    return config