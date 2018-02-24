#!/usr/bin/env python3
#encoding: utf-8

import re
import cgi
import json
import datetime
import cgitb; cgitb.enable()
from production.sql import DataBase
from production.config import cfgfile, readCfg
# Create instance of FieldStorage
form = cgi.FieldStorage()

print("Content-Type: text/html")
print("")

# Get data from fields
mac = form.getvalue('a')
firmware_version = form.getvalue('b')
script_version = form.getvalue('c')

pattern_mac = re.compile(
    '[0-9a-zA-Z:]+', re.X
    )
pattern_fw_version = re.compile(
    '[0-9a-zA-Z-]+', re.X
    )
pattern_sp_version = re.compile(
    '[0-9a-z.]+', re.X
    )

def find_mac(mac):
    macList = database.run(
        'select', 'mac_list',
        ['mac_address', 'Download_link', 'script_version']
        )
    for i in macList:
        if i[0] == mac:
            return json.dumps({'Download_link' : i[1],'script_version' : i[2]})
    else:
        return 'No mac address.'

def save(mac, firmware_version, script_version):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    database.run('create', 'mac_save', [
        {"name": "time", "type": "datetime"},
        {"name": "mac_address", "type": "VARCHAR(150)"},
        {"name": "firmware_version", "type": "VARCHAR(64)"},
        {"name": "script_version", "type": "VARCHAR(64)"},
    ], 'PRIMARY KEY(`time`)')
    result = database.run(
        'insert', 'mac_save',
        ['time', 'mac_address', 'firmware_version', 'script_version'],
        [now, mac, firmware_version, script_version]
    )
    if result:
        print('Upload information successfully.')
    else:
        print('Upload information failed')


if __name__ == '__main__':
    db = readCfg(cfgfile)['DataBase']
    database = DataBase(db)
    database.connect()
    if mac is None:
        print ('Write right MAC address')
        exit()
    elif firmware_version is None or script_version is None:
        firmware_version = ''
        script_version = ''
    match_mac = re.match(pattern_mac, mac)
    match_fw_version = re.match(pattern_fw_version, firmware_version)
    match_sp_version = re.match(pattern_sp_version, script_version)
    if match_mac and match_fw_version and match_sp_version is not None:
        save(mac, firmware_version, script_version)
    else:
        print(find_mac(mac))
    database.commit()
    database.disconnect()