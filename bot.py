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
from csvtools import CsvLessons

CSV_FILES = ['csv/autumn_2016-2017_2_fix.csv']
bot = telebot.TeleBot(cfg.token)


@bot.message_handler(commands=['start']) #building a new client
def send_welcome(message):
    bot.reply_to(message, "Доброго времени суток! Для начала использования, пожалуйста зарегистрируйтесь с помощью /register.")
    s = shelve.open(slocal)
    s[str(message.chat.id)] = 0
    wat = s[str(message.chat.id)]
    print(wat) #выводим в консоль ID чата клиента
    # bot.send_message(message.chat.id, 'Got it, pal! Your ID is '+str(message.chat.id)+'. Now lets get it started.')       <= раньше клиенту посылался его chat.id, можно включить для отладки
    s.close()

@bot.message_handler(commands=['help']) #general help
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я ИМЭИбот, могу показать ваше расписание, помочь в поиске преподавателя и кое-что ещё. \n Команды: \n \n */help* - показывает это сообщение \n */register* - Выслушаю номер вашей группы \n */today* - Расписание на сегодня, время до начала занятий. \n */getteacher* - Поиск преподавателя \n */news* - Новости ИГУ \n */fact* - случайный математический факт", parse_mode="Markdown")
    

@bot.message_handler(commands=['register']) 
def register(message):
  bot.send_message(message.chat.id, "Пожалуйста, введите номер группы (выглядит как 2xxx).")
  s = shelve.open(slocal)
  s[str(message.chat.id)] = 1
  ass = s[str(message.chat.id)]
  print(ass)
  

@bot.message_handler(regexp="2[1-5][1-5][1-5]")
def handle_message(message):
  s = shelve.open(slocal)
  if  s[str(message.chat.id)] == 1:
    group = ''
    gs = shelve.open(glocal)
    group = message.text
    gs[str(message.chat.id)] = group
    bot.send_message(message.chat.id, "Группа успешно обновлена, ваша - "+group)
    gs.close()
  s[str(message.chat.id)] = 2 
  pens =  s[str(message.chat.id)]
  print(pens)
  s.close()



@bot.message_handler(commands=['today'])
def give_today(message):
	s = shelve.open(slocal)
	if  s[str(message.chat.id)] == 1 or s[str(message.chat.id)] == 0:
		bot.send_message(message.chat.id, "Пожалуйста, сперва зарегистрируйтесь. Введите /register для начала.")
		s.close()
	else:
		text=''
		gs = shelve.open(glocal)
		grp = gs[str(message.chat.id)]
		# dbaser.cur.execute("SELECT schedule.stime, schedule.room, lessons.lessname, lessons.teachname, schedule.etime FROM schedule INNER JOIN lessons WHERE  schedule.lessid=lessons.lessid AND schedule.gid=? ORDER BY schedule.stime ASC", (grp,))
		# rows = dbaser.cur.fetchall()
		rows = dbaser.get_schedules_by_group(grp)
		for row in rows:
			temp = tools.tohrs(row[0]) + " *"+str(row[2])+"*" + "\n Кабинет " + str(row[1]) + "\n" + str(row[3]) + "\n"
			text = text + temp
		text+=tools.get_new_lesson(rows)
		print(text)
		bot.send_message(message.chat.id, text, parse_mode="Markdown")
		gs.close()

@bot.message_handler(commands=['news'])
def btns(message):
	bot.send_message(message.chat.id, "Парсим последние новости ИГУ...") 
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

@bot.message_handler(commands=['getteacher'])
def give_getteacher(message):
	bot.send_message(message.chat.id,"Введите фамилию / имя преподавателя")
	s = shelve.open(slocal)
	s[str(message.chat.id)] = 'getteacher'
	s.close()

@bot.message_handler(content_types=["text"])
def handle_message(message):
	s = shelve.open(slocal)
	if s[str(message.chat.id)] == 'getteacher':
		professor = message.text
		print('Ищем преподавателя "%s"...' % professor)
		rows = dbaser.get_schedules_by_group(professor=professor)
		text = tools.get_current_position_professor(rows)
		if text.strip()=='' : text = 'Преподаватель не найден. Возможно, попробовать сформулировать запрос по-другому?'
		print(text)
		bot.send_message(message.chat.id, text, parse_mode="Markdown")

	s[str(message.chat.id)] = 2
	s.close()

if __name__ == '__main__':
	c = CsvLessons(path=CSV_FILES[0])
	dbaser.upload_lessons(c.lessons)
	dbaser.upload_weeks(c.week_top_dates, c.week_bottom_dates)
	bot.polling(none_stop=True)
