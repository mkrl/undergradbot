from telebot import types
import shelve
import dbaser
import re

#def register(chat_id):
#  bot.send_message(message.chat.id, "Please state your group number (looks something like 2xxx).")
#  group = message.text 
#  match = re.match('2[1-5][1-5][1-5]', group, flags=0)
#  if len(match)>0 :
#        bot.send_message(message.chat.id, "Invalid group numberm please register again.")
#  else : 
#    with shelve.open(slocal) as storage:
#          storage[str(chat_id)] = group
#    bot.send_message(message.chat.id, "Group updated successfully.")
        
        
def tohrs(seconds):
  z=seconds
  h=z/3600 
  m=z%3600/60 
#  s=z%3600%60
  hr = str(h) + ":" + str(m)
  return hr