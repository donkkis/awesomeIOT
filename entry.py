# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 13:52:49 2018

@author: paho
"""

from peewee import *

db = SqliteDatabase('ebus_turku.db')

class Entry(Model):
    timestamp = DateTimeField()
    timecluster_rough = DateTimeField()
    timecluster_dense = CharField()
    weekday = CharField()
    location = CharField()
    datanode = CharField()
    unit = CharField()
    value = CharField()
    
    class Meta:
        database = db
        #Trailing comma!
        #http://docs.peewee-orm.com/en/latest/peewee/models.html#indexes-and-constraints
        #indexes = (
        #        (('timestamp', 'location', 'datanode'), True),
        #        )