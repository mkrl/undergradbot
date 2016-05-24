# -*- coding: utf-8 -*-
import cfg
import telebot
import dbaser
import tools
import shelve
import feedparser
from cfg import slocal
from cfg import glocal
from telebot import types
import random

bot = telebot.TeleBot(cfg.token)


@bot.message_handler(commands=['start']) #building a new client
def send_welcome(message):
    bot.reply_to(message, "Filling in a database...")
    s = shelve.open(slocal)
    s[str(message.chat.id)] = 0
    wat = s[str(message.chat.id)]
    print(wat)
    bot.send_message(message.chat.id, 'Got it, pal! Your ID is '+str(message.chat.id)+'. Now lets get it started.')    
    s.close()

@bot.message_handler(commands=['help']) #general help
def send_welcome(message):
    bot.send_message(message.chat.id, "Hi! They call me IMEI bot and I'm able to deliver your today's schedule here, tell you some usefull stuff and more! \n Commands: \n \n */help* - shows this page \n */register* - Tell me your group number \n */today* - Your today's schedule and how much time do you have till a lesson starts. \n *???* ", parse_mode="Markdown")
    
#GENERAL STATUS CHECK SQLS                          <= unused!
# UPDATE GROUP set gid=X where client = chat.id
# UPDATE STATUS set status=X where client = chat.id
# SELECT status FROM STATUS where  client = chat.id
# SELECT gid FROM GROUP where  client = chat.id
# INSERT INTO STATUS (client,status) \
#      VALUES (chat.id, x)

@bot.message_handler(commands=['unicode'])
def register(message):
	bot.send_message(message.chat.id, "Zdarova! Попробую объясниться на русском языке.") 

 

@bot.message_handler(commands=['register']) 
def register(message):
  bot.send_message(message.chat.id, "Please state your group number (looks something like 2xxx). Only available for 2321 for now though.")
  s = shelve.open(slocal)
  s[str(message.chat.id)] = 1
  ass = s[str(message.chat.id)]
  print(ass)
  
#  match = re.match('2[1-5][1-5][1-5]', group, flags=0)
#  if len(match)>0 :
#        bot.send_message(message.chat.id, "Invalid group number, please register again.")
#  else : 
#  with shelve.open(slocal) as storage:
#  storage[str(chat_id)] = group
#  bot.send_message(message.chat.id, "Group updated successfully. Yours is "+group)

@bot.message_handler(regexp="2[1-5][1-5][1-5]")
def handle_message(message):
  s = shelve.open(slocal)
  if  s[str(message.chat.id)] == 1:
    group = ''
    gs = shelve.open(glocal)
    group = message.text
    gs[str(message.chat.id)] = group
    bot.send_message(message.chat.id, "Group updated successfully. Yours is "+group)
    gs.close()
  s[str(message.chat.id)] = 2 
  pens =  s[str(message.chat.id)]
  print(pens)
  s.close()



@bot.message_handler(commands=['today'])
def give_today(message):
	s = shelve.open(slocal)
	if  s[str(message.chat.id)] == 1 or s[str(message.chat.id)] == 0:
		bot.send_message(message.chat.id, "Please register first. Type /register to start.")
		s.close()
	else:
		text=''
		gs = shelve.open(glocal)
		grp = gs[str(message.chat.id)]
		dbaser.cur.execute("SELECT schedule.stime, schedule.room, lessons.lessname, lessons.teachname, schedule.etime FROM schedule INNER JOIN lessons WHERE  schedule.lessid=lessons.lessid AND schedule.gid=? ORDER BY schedule.stime ASC", (grp,))
		for row in dbaser.cur:
			temp = tools.tohrs(row[0]) + " *"+str(row[2])+"*" + "\n Room no. " + str(row[1]) + "\n" + str(row[3]) + "\n"
			text = text + temp
		bot.send_message(message.chat.id, text, parse_mode="Markdown")
		gs.close()

@bot.message_handler(commands=['news'])
def btns(message):
	# markup = types.ReplyKeyboardMarkup(row_width=1)
	# itembtn1 = types.KeyboardButton('Ещё новости')
	# itembtn2 = types.KeyboardButton('Подробнее')
	# markup.add(itembtn1, itembtn2)
	# tb.send_message(chat_id, "Parsing lastest ISU news...", reply_markup=markup)
	bot.send_message(message.chat.id, "Parsing lastest news...") 
	d = feedparser.parse('http://feed.exileed.com/vk/feed/irkutskuniversity/?only_admin=1&at=1')
	msg=''
	for i in range(len(d.entries)):	
		tit=d.entries[i].title
		link=d.entries[i].link
		msg=msg+'>>> <a href="'+link+'">'+tit+'</a> \n'
		if i==8:												#until pagdination is added, only first 8 entries
			break
	bot.send_message(message.chat.id, msg, parse_mode="HTML")
		
@bot.message_handler(commands=['fact']) #random math fact
def facts(message):
	bot.send_message(message.chat.id, random.choice(tools.facts))
		
if __name__ == '__main__':
     bot.polling(none_stop=True)