# -*- coding: utf-8 -*-
import dbaser
import re
import datetime


facts = ['π=3.14159 26535 89793 23846 26433 83279 50288 41971 69399 37510 58209 74944 59230 78164 06286 20899 86280 34825 34211 70679 82148 08651 32823 ...','In a group of 23 people, at least two have the same birthday with the probability greater than 1/2', '12+3-4+5+67+8+9=100 and there exists at least one other representation of 100 with 9 digits in the right order and math operations in between', 'Among all shapes with the same area circle has the shortest perimeter', 'If you write out pi to two decimal places, backwards it spells “pie”.', '7. 111,111,111 × 111,111,111 = 12,345,678,987,654,321.', 'The number 4 is considered unlucky in much of Asia.', 'Godels Incompleteness Theorem: If the system is consistent, it cannot be complete. The consistency of the axioms cannot be proven within the system. Or the corralary that if the consitency of axioms can be proved within a system, that the system is invalid.','10! seconds = exactly 42 days', 'The Hairy Ball Theorem: If a sphere is covered in hair (think a coconut), no matter how you comb it, there will always be at least one hair sticking straight up. ','Take your age. Add it by 2. Then minus 2 from it. Boom! This is how old you are.', 'You can paint the inside of a bottomless pit but you cant paint the outside.If you take the rotation integral of 1/x from 1 to infinity it comes out as 6.28 (or 2 pi) which means that the bottomless structure created by the rotation of 1/x has a finite volume. But obviously an infinite surface area.']        
        
#def tohrs(seconds):              <= Worked in python 2.7
#  z=seconds
#  h=z/3600 
#  m=z%3600/60 
#  s=z%3600%60
#  hr = str(h) + ":" + str(m)
#  return hr
#  
  
        
def tohrs(seconds): #transforms seconds to hh:mm format
  a=seconds
  h=((a//3600))%24
  m=(a//60)%60
  s=a%60
  if m<10:
      m=str('0'+str(m))
  else:
      m=str(m)
  if s<10:
      s=str('0'+str(s))
  else:
      s=str(s)
  hr=str(h)+':'+str(m)
  return hr

  
def moment():  #returns current time in seconds since day started
    now = datetime.datetime.now() + datetime.timedelta(hours=dbaser.OFFSET_HOUR)
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = (now - midnight).seconds
    return seconds

lst=[2143,1233,1234,124141,31241,124124,23,24,3242,145234]
		
def separate(lst, n): #divides a list by n equal parts
	return [lst[i:i + n] for i in range(0, len(lst), n)]

def get_current_position_professor(data):
    ct = moment()
    res = ''
    for row in data:
        res = 'Преподаватель *%s* сейчас на *кафедре*' % str(row[3])
        if ct >= row[0] and ct <= row[4]:
            res = "\r\nПреподватель *%s* сейчас в кабинете *%s*" % (
                str(row[3]),
                str(row[1]),
                # tohrs(row[0]),
                # tohrs(ct),
                # tohrs(row[4]),
            )
            return res

    return res



def get_new_lesson(data):
    ct = moment()
    res = ''
    for row in data:
        if ct < row[0] and ct < row[4]:
            s = tohrs(row[0] - ct)
            h = s[:s.find(':')]
            m = s[s.find(':') + 1:]
            res = "\r\nСледующая пара *\"%s\"* через *%s* в кабинете *%s*" % (
                str(row[2]),
                "%s%s мин." % (("%s ч. " % h if not h in ['0',''] else ''), m),
                str(row[1])
            )
            break
    return res


