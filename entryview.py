# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 15:51:06 2018

@author: paho
"""
# Try it:
#https://stackoverflow.com/questions/38707331/does-peewee-support-interaction-with-mysql-views

from peewee import *
import entry

db = SqliteDatabase('ebus_turku.db')

class EntryView(Entry):
    def __init__(entryview):
        self.entryviewtable = entryview
    
    class Meta:
        db_table = self.entryviewtable