# -*- coding: utf-8 -*-
import sqlite3
import cfg

con = sqlite3.connect(cfg.dbase, check_same_thread=False)
cur = con.cursor()




