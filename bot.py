# -*- coding: utf-8 -*-
import cfg
import telebot
import dbaser
import random
import tools
import re
import shelve

reg=1
bot = telebot.TeleBot(cfg.token)
vy = ['Chto za vopros? Vy yaz!', 'Samyj lubimyi yaz', 'Nash yaz', 'Kot', 'Krot', 'Superkrot konechno!', 'Yaz', 'Milyj yaz', 'Yedinstvennyj yaz']

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello there. I'm a brainless bot. Please tell me your group number.")

@bot.message_handler(commands=['register'])
def register(message):
  bot.send_message(message.chat.id, "Please state your group number (looks something like 2xxx).")

#  match = re.match('2[1-5][1-5][1-5]', group, flags=0)
#  if len(match)>0 :
#        bot.send_message(message.chat.id, "Invalid group number, please register again.")
#  else : 
#  with shelve.open(slocal) as storage:
#  storage[str(chat_id)] = group
#  bot.send_message(message.chat.id, "Group updated successfully. Yours is "+group)

#@bot.message_handler(regexp="2[1-5][1-5][1-5]")
#def handle_message(message):
#  if reg == 1:
#    group = message.text
#    with shelve.open(cfg.slocal) as storage:
#      storage[str(chat_id)] = group
#    bot.send_message(message.chat.id, "Group updated successfully. Yours is "+group)

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
