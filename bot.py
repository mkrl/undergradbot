# -*- coding: utf-8 -*-
import cfg
import telebot
import dbaser
import random
import tools
import shelve
from cfg import slocal
from cfg import glocal



bot = telebot.TeleBot(cfg.token)
vy = ['Chto za vopros? Vy yaz!', 'Samyj lubimyi yaz', 'Nash yaz', 'Kot', 'Krot', 'Superkrot konechno!', 'Yaz', 'Milyj yaz', 'Yedinstvennyj yaz']

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello there. I'm a brainless bot. Please tell me your group number.")
#    dbaser.cur.execute('SELECT schedule.stime, schedule.room, lessons.lessname, lessons.teachname FROM schedule INNER JOIN lessons WHERE  schedule.lessid=lessons.lessid AND schedule.gid=2321 ORDER BY schedule.stime ASC')

@bot.message_handler(commands=['getme']) #building a new client
def send_welcome(message):
    bot.reply_to(message, "Filling in a database...")
    s = shelve.open(slocal)
    s[str(message.chat.id)] = 0
    wat = s[str(message.chat.id)]
    print(wat)
    bot.send_message(message.chat.id, "Got it, pal! Your ID is "+str(message.chat.id)+"And your status is ")    
    s.close()
    
#GENERAL STATUS CHECK SQLS
# UPDATE GROUP set gid=X where client = chat.id
# UPDATE STATUS set status=X where client = chat.id
# SELECT status FROM STATUS where  client = chat.id
# SELECT gid FROM GROUP where  client = chat.id
# INSERT INTO STATUS (client,status) \
#      VALUES (chat.id, x)



@bot.message_handler(commands=['register'])
def register(message):
  bot.send_message(message.chat.id, "Please state your group number (looks something like 2xxx).")
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


@bot.message_handler(commands=['ktoya'])
def yaz(message):
    bot.reply_to(message, random.choice(vy))
    
@bot.message_handler(commands=['yaz'])
def yaz(message):
    bot.reply_to(message, "eto pro vas")

#@bot.message_handler(func=lambda m: True)
#def echo_all(message):
#    bot.reply_to(message, "whoa")

@bot.message_handler(commands=['today'])
def give_today(message):
    text=''
    dbaser.cur.execute('SELECT schedule.stime, schedule.room, lessons.lessname, lessons.teachname FROM schedule INNER JOIN lessons WHERE  schedule.lessid=lessons.lessid AND schedule.gid=2321 ORDER BY schedule.stime ASC')
    for row in dbaser.cur:
        temp = tools.tohrs(row[0]) + ": Room no. " + str(row[1]) + "\n" + "*"+str(row[2])+"*" + ". \n" + str(row[3]) + "\n \n"
        text = text + temp
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

if __name__ == '__main__':
     bot.polling(none_stop=True)
