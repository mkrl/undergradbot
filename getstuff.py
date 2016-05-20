
import shelve


s = shelve.open('deeznuts')
try:
    s['clid']=0
finally:
    s.close()

s = shelve.open('deeznuts.db')
try:
    fuck = s['clid']
finally:
    s.close()

print(fuck)



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