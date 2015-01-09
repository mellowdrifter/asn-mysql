#!/usr/bin/python

import MySQLdb
import sys
import time
import re
import urllib2
import ConfigParser

url = 'http://bgp.potaroo.net/cidr/autnums.html'
new = 0
today = time.strftime("%Y-%m-%d")
db_name = Config.get('database', 'db_name')
db_user  = Config.get('database', 'db_user')
db_password = Config.get('database', 'db_password')
db_location = Config.get('database', 'db_location')

print "Downloading"
content = urllib2.urlopen(url).read()

print "Download complete"

as_list = new_list = re.findall(r'AS(\d+)\s*</a> (.*),(.{2})', content)

db = MySQLdb.connect(location, db_user, db_password, db_name)
cursor = db.cursor()

def create_sql(multicreate):
    with db:
        sql = '''INSERT INTO ASN(AS_NUM, AS_NAME, LOCALE, QUERIED, CHANGED) \
                    VALUES (%s, %s, %s, %s, %s)'''
        cursor.executemany(sql, multicreate)

with db:
    multicreate = []
    print "Checking..."
    for AS in as_list:
        multicreate.append((int(AS[0].strip()), AS[1].strip(), AS[2].strip(), 0, today))
    print "Checked, updataing now..."
    create_sql(multicreate)

print "New AS: " + str(new)
