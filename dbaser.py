import sqlite3
import cfg

con = sqlite3.connect(cfg.dbase, check_same_thread=False)
cur = con.cursor()





#z=input('')
#h=z/3600 
#m=z%3600/60 
#s=z%3600%60

#print '%i:%i:%i' % (h, m, s)
