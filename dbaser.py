# -*- coding: utf-8 -*-
import sqlite3
import cfg
import csvtools
OFFSET_HOUR = 8
con = sqlite3.connect(cfg.dbase, check_same_thread=False)
cur = con.cursor()

def lesson_exist_id( lesson):
    try:
        id = -1
        cur.execute('select lessid from lessons where lessname=\'%s\' and teachname=\'%s\' ' % (
            lesson.discipline,
            lesson.professor
        ))
        for row in cur.fetchall(): id = int(row[0])
        cur.connection.commit()
        return id
    except:
        return -1


def upload_lesson( lesson):
    try:
        if not lesson_exist_id(lesson) > -1:
            sql = 'INSERT INTO lessons(lessid, lessname, teachname) VALUES( (%s), \'%s\',\'%s\') ;' % (
                'select max(lessid) +1 from lessons',
                lesson.discipline,
                lesson.professor
            )
            cur.execute(sql)
            cur.connection.commit()
            return (lesson_exist_id(lesson), True)
        return (lesson_exist_id(lesson), False)
    except:
        return (-1, False)

def schedule_exist(lesson, lessid):
    c = 0
    sql = """
        SELECT count(*) FROM schedule
        where stime=%d and etime=%d and room='%s' and lessid=%d and gid=%d and week_day=%d and week=%d
        """ % (
        lesson.time.start_sec,
        lesson.time.end_sec,
        lesson.room,
        lessid,
        lesson.gid,
        lesson.week_day,
        lesson.week
    )
    cur.execute(sql)
    for row in cur.fetchall():
        c = int(row[0])
    cur.connection.commit()
    return c > 0

def upload_schedule( lesson, lessid):
    if not schedule_exist(lesson, lessid):
        sql_insert = """
        INSERT OR REPLACE INTO schedule(stime, etime, room, lessid, gid, week_day, week)
        VALUES(%d, %d, '%s', %d, %d, %d, %d)
        """ % (
            lesson.time.start_sec,
            lesson.time.end_sec,
            lesson.room,
            lessid,
            lesson.gid,
            lesson.week_day,
            lesson.week
        )
        cur.execute(sql_insert)
        cur.connection.commit()
        return True
    return False

def upload_lessons( lessons):
    print('Заливаем в базу занятия и расписания ...')
    count_lessons = 0
    count_schedules = 0
    lesson_inserted = False
    for lesson in lessons:
        iid, lesson_inserted = upload_lesson(lesson)
        if lesson_inserted: count_lessons += 1
        if iid > -1:
            if upload_schedule(lesson, iid):
                count_schedules += 1
    print('Добавлено в базу %d занятий' % count_lessons)
    print('Добавлено в базу %d расписаний' % count_schedules)

def upload_weeks(week_top_dates, week_bottom_dates):
    cur.execute('delete from weeks;')
    cur.connection.commit()

    sql_insert = 'INSERT INTO weeks(id, day, month) VALUES(%d, %d, %d)'
    print('Заливаем недели...')
    print('Заливаем числитель...')
    c = 0
    for d in week_top_dates:
        cur.execute(sql_insert % ( csvtools.WEEK_TOP, d.day, d.month))
        cur.connection.commit()
        c += 1
    print('Сохранено %d недель по числителю' % c)
    print('Заливаем знаменатель...')
    c = 0
    for d in week_bottom_dates:
        cur.execute(sql_insert % (csvtools.WEEK_BOTTOM, d.day, d.month))
        cur.connection.commit()
        c += 1
    print('Сохранено %d недель по знаменатею' % c)

def get_schedules_by_group(group=None, professor=None):
    rows =[]
    import datetime
    week_first_day = csvtools.get_date_first_week_day(datetime.datetime.now()+datetime.timedelta(hours=OFFSET_HOUR))
    print('Получаем расписание на сегодня (%s) для группы %s ...' % (
        datetime.datetime.now() + datetime.timedelta(hours=OFFSET_HOUR), group))
    sql = """
    SELECT schedule.stime, schedule.room, lessons.lessname, lessons.teachname, schedule.etime
    FROM schedule INNER JOIN lessons on schedule.lessid=lessons.lessid
    WHERE %s schedule.week_day=%d
    and schedule.week in (%d, (select id from weeks where day=%d and month=%d) )
    %s
    ORDER BY schedule.stime ASC""" % (
        ('schedule.gid=%d and' % int(group)) if not group is None else '',
        (datetime.datetime.now()+datetime.timedelta(hours=OFFSET_HOUR)).weekday() + 1,
        csvtools.WEEK_ALL,
        week_first_day.day,
        week_first_day.month,
        (' AND UPPER(lessons.teachname) like UPPER(\'%'+professor+'%\') ') if not professor is None else ''
    )
    print(sql)
    cur.execute(sql)
    rows = cur.fetchall()
    print('Получено %d занятий.' % len(rows))
    return rows
