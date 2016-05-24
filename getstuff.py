# -*- coding: utf-8 -*-
# this file is being used for testing puropses
import cfg
import telebot
import dbaser
import random
import tools
import shelve
from cfg import slocal
from cfg import glocal

# !text = 'Выводим кириллицу в консоль. С трудом, ё! К сожалению, в терминале не всё корректно отображается.'
# print(text)

# septime=[]
# time=[]
# dbaser.cur.execute("SELECT schedule.stime, schedule.room, lessons.lessname, lessons.teachname, schedule.etime FROM schedule INNER JOIN lessons WHERE  schedule.lessid=lessons.lessid AND schedule.gid=2321 ORDER BY schedule.stime ASC")
# for row in dbaser.cur:
	# time.append(row[0])
	# time.append(row[4])
# septime=tools.separate(time,2)

# for i in septime.len:

import feedparser
d = feedparser.parse('http://feed.exileed.com/vk/feed/irkutskuniversity/?only_admin=1&at=1')
msg=d['feed']['title']


#dont forget to close cur with dbaser.cur.close!!

#
#dbaser.cur.execute('SELECT schedule.stime, schedule.room, lessons.lessname, lessons.teachname FROM schedule INNER JOIN lessons WHERE  schedule.lessid=lessons.lessid AND schedule.gid=2321 ORDER BY schedule.stime ASC')
#text = ''
#for row in dbaser.cur:
#   temp = ("At " + str(row[0]) + " in room no. " + str(row[1]) + "\n takes place " + str(row[2]) + ". \nThe teacher name is " + str(row[3]) + "\n \n")
#   text = text + temp
#print text;
#dbaser.con.close()

#    dbaser.cur.execute('SELECT schedule.stime, schedule.room, lessons.lessname, lessons.teachname FROM schedule INNER JOIN lessons WHERE  schedule.lessid=lessons.lessid AND schedule.gid=2321 ORDER BY schedule.stime ASC')
#    for row in dbaser.cur:
#        temp="At ", row[0], "in room no. ", row[1], "takes place", row[2], " The teachers name is ", row[3]'
#        text=text+" "+temp
#    dbaser.con.close()
#print(text)