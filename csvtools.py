
# -*- coding: utf-8 -*-
import csv
import os
import datetime
import tools

CSV_FILES = ['csv/autumn_2016-2017_2_fix.csv', 'csv/2.csv'] #can parse multiple files
DAYS = ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА', 'ВОСКРЕСЕНЬЕ']
WEEK_TOP = 1
WEEK_BOTTOM = 2
WEEK_ALL = 3
WEEK_TOP_SEARCH_TEXT = 'ВЕРХНЯЯ НЕДЕЛЯ:'
WEEK_BOTTOM_SEARCH_TEXT = 'НИЖНЯЯ НЕДЕЛЯ:'


def get_week_by_date(week_top_dates, week_bottom_dates, by_date=datetime.datetime.now()):
    """
    Определяет числительная или знаменательная неделя для даты by_date
    """
    def in_week_dates(week_dates, date_):
        for wd in week_dates:
            if date_.month == wd.month and date_.day == wd.day:
                return True
        return False

    date_ = get_date_first_week_day(by_date) if not by_date is None else None

    if in_week_dates(week_top_dates, date_):
        return WEEK_TOP
    elif in_week_dates(week_bottom_dates, date_):
        return WEEK_BOTTOM
    else:
        return WEEK_ALL
    return week

def get_date_first_week_day(by_date):
    """
    возвращает дату для первого дня недели даты by_date
    """
    return by_date - datetime.timedelta(days=by_date.weekday()) if not by_date is None else None


class Lesson_Time:
    start, end = None, None
    def __init__(self, **kwargs):
        self.start = datetime.datetime.strptime(kwargs.get('start'), "%H.%M")
        self.end = datetime.datetime.strptime(kwargs.get('end'), "%H.%M")
        super(Lesson_Time, self).__init__()

    def get_sec(self, t):
        return t.second + t.minute * 60 + t.hour * 3600 if not t is None else 0

    @property
    def start_sec(self): return self.get_sec(self.start)

    @property
    def end_sec(self): return self.get_sec(self.end)

class Lesson:
    week_day = None
    time = None
    group = None
    group_code = None
    week = WEEK_ALL
    discipline = None
    professor = None
    room = None

    def __init__(self, **kwargs):
        self.week_day = kwargs.get('week_day')
        self.time = kwargs.get('time')
        self.group = int(kwargs.get('group'))
        self.group_code = kwargs.get('group_code')
        self.week = int(kwargs.get('week', WEEK_ALL))
        self.discipline = kwargs.get('discipline').strip()
        self.professor = kwargs.get('professor').strip()
        self.room = kwargs.get('room').strip()
        super(Lesson, self).__init__()

    @property
    def gid(self):
        return int(self.group_code[:self.group_code.find('-')].strip())

    def set_time(self, time1, time2):
        if not time1 is None: # числитель
            self.time = time1
        else:                 # знаменатель
            self.time = time2
            self.week = WEEK_BOTTOM

    def debug(self):
        z = {}
        zz = dir(self)

        for a in filter(lambda x: not x.startswith('_'), zz):
            if a in ['print','g','set_time','debug']: continue
            z[a] = getattr(self, a)
            if z[a].__class__ is Lesson_Time:
                z[a]={'start':z[a].start, 'end':z[a].end}
        return z


class CsvLessons(object):
    lessons = [] # занятия
    start_index = None # индекс стартовой строки, потому как в начале идет шапка
    index = None # индекс текущей строки при чтении
    groups = [] # список найденных групп
    last_row_weekday, last_row_time = None, None # последние найденне день недели и время занятия, нужно при строках знаменателя
    last_row_professor, last_row_room = None, None # последний найденный препод
    week_top_dates, week_bottom_dates = [],[] # списки начала недель числитель и знаменатель соответственно
    skip_empty_line = False # пропускать при чтении пустые строки


    def __init__(self, path, skip_empty_line = False):
        self.skip_empty_line = skip_empty_line
        self.parse_file(path)
        super(CsvLessons, self).__init__()

    def is_empty(self, data):
        """
        Проверяем на пустоту
        """
        if data is None: return True
        if data.__class__ is list:
            for item in data:
                if self.is_empty(item):
                    return False
            return True
        elif data.__class__ is str:
            return data.strip() == ''
        return False

    def get_header_index(self, row):
        """
        Проверяем строку на шапку, если в строке есть ячейка "ДНИ" , тосчитаем ее шапкой
        """
        return self.index if row[0].upper()=='ДНИ' else None

    def get_week_day_id(self, row):
        """
        Получаем номер дня недели
        """
        week_day_name = row[0].upper().strip() if len(row) > 0 and not row[0] is None else None
        # print('[%s]'%week_day_name)
        return DAYS.index(week_day_name)+1 if week_day_name in DAYS else None

    def get_groups(self, row):
        """
        Получаем список групп
        """
        self.groups = [item for item in row if not self.is_empty(item)]
        return self.groups

    def get_time(self, row):
        """
        Получаем время
        """
        if self.is_empty(row[1]): return None
        period = [t.strip() for t in row[1].split('-')]
        return Lesson_Time(start=period[0], end=period[1])

    def make_numerator(self, week_day, group_id, time_):
        """
        если в списке есть запись для данной группы, в то же время,
        то значит у нас знаменатель и нужно существующую запись сделать числителем
        """

        for lesson in self.lessons:
            if lesson.group == group_id and lesson.week_day == week_day and lesson.time.start == time_.start:  # l.time.end == time.end:
                lesson.week = WEEK_TOP

    def parse_line_lessons(self, row, week_day, time_):
        """
        Получаем список занятий в строке
        """
        items = row[2:-2]  # отрезаем дни недели и время в начале и в конце строки
        group_id = -1
        lessons = []

        for i in range(0, len(items), 3):
            group_id += 1
            item = items[i:i + 3]

            row_time = self.get_time(row)
            if row_time is None: # если стока без времени, то предудующую делаем числителем
                self.make_numerator(week_day, group_id, time_)
            if self.is_empty(item[0]): continue # если ди

            lessons.append(
                Lesson(
                    week_day=week_day,
                    time=time_,
                    group=group_id,
                    group_code=self.groups[group_id],
                    week=WEEK_ALL if not row_time is None else WEEK_BOTTOM,
                    discipline=item[0],
                    professor=item[1],
                    room=item[2],
                )
            )
        return lessons

    def make_week_dates(self, dates):
        ct = datetime.datetime.now()
        return [datetime.datetime.strptime("%s.%d" % (d.strip(), ct.year), "%d.%m.%Y") for d in dates]


    def get_weeks(self, row):
        """
        Получаем недели для числителей и знаменателей
        нужно учитывать что значние сдвинуто на 3 ячейки вправо
        """
        k = 0
        for item in row:
            if WEEK_TOP_SEARCH_TEXT.upper() in item.strip().upper():
                self.week_top_dates = self.make_week_dates(row[k + 3].split(','))
                return True
            elif WEEK_BOTTOM_SEARCH_TEXT.upper() in item.strip().upper() :
                self.week_bottom_dates = self.make_week_dates(row[k + 3].split(','))
                return True
            k += 1
        return False

    def parse_file(self, path):
        """Парсим файл"""
        print(u'Обрабатываем файл <%s>...' % path)
        if not os.path.exists(path):
            return False
        self.lessons = list()
        with open(path, 'r') as f:
            stream = csv.reader(f, delimiter=';', )
            for row in stream:
                if self.skip_empty_line and self.is_empty(row): continue
                self.lessons.extend(self.parse_line(row))
                if len(self.week_top_dates) > 0 and len(self.week_bottom_dates) > 0:
                    break

        print(u'Прочитано %d групп.' % len(self.groups))
        print(u'Прочитано %d занятий.' % len(self.lessons))
        return self.lessons

    def parse_line(self, row):
        """Парсим строку файла"""
        self.index = 0 if self.index is None else self.index + 1
        if self.start_index is None:
            self.start_index = self.get_header_index(row)

        if self.start_index is None or self.index <= self.start_index: # пропускаем все что выше шапки
            return []

        if self.index-self.start_index == 1:# строка с названиями групп
            self.get_groups(row)
            return []

        if self.get_weeks(row): return []# строка с описание недель
        self.last_row_day = (lambda d: d if not d is None else self.last_row_day )(self.get_week_day_id(row))
        self.last_row_time = (lambda t: t if not t is None else self.last_row_time )(self.get_time(row))

        return self.parse_line_lessons(row, self.last_row_day, self.last_row_time)



    def get_group_id_by_name(self, name, exact_match=False):
        """
        Возвращает индекс группы по названию, если
        :param name: название группы
        :param exact_match: точное совпадение имени
        :return:
        """
        if exact_match:
            if name in self.groups:
                return self.groups.index(name)
        else:
            for i in range(len(self.groups)):
                if name in self.groups[i]:
                    return (i, self.groups[i])
        return None

if __name__ == '__main__':
    c = CsvLessons(path=CSV_FILES[0], skip_empty_line=False)
    print(u'|' + '-' * 146 + '|')
    print(u'|%s|%s|%s|%s|%s|' % (
        u'Группа'.center(10, ' '),
        u'День недели'.center(15, ' '),
        u'Время'.center(15, ' '),
        u'Дисциплина'.center(72, ' '),
        u'Числитель/знаменатель'.center(30, ' '),
    ))
    print(u'|'+'-'*146+'|')
    k = 0
    for l in c.lessons:
        if l.group != 1: continue #только группа 2121-ДБ
        if l.week == WEEK_TOP: w=u'ЧИСЛИТЕЛЬ'
        elif l.week == WEEK_BOTTOM: w=u'ЗНАМЕНАТЕЛЬ'
        else: w=u'ВСЕГДА'
        print(u'|%s|%s|%s|  %s|%s|' % (
            c.groups[l.group].center(10, ' '),
            DAYS[l.week_day-1].center(15, ' '),
            str(u'%s:%s-%s:%s' % (
                str(l.time.start.hour).rjust(2, '0'),
                str(l.time.start.minute).rjust(2, '0'),
                str(l.time.end.hour).rjust(2, '0'),
                str(l.time.end.minute).rjust(2, '0'),
                                )).center(15, ' '),
            l.discipline.ljust(70, ' '),
            w.center(30, ' '),


        ))
        k+=1
        print(u'|' + '-' * 146 + '|')
    print(u'| ВСЕГО:   |' + (u'  %d  |' % k).rjust(136, ' '))
    print(u'|' + '-' * 146 + '|')

    # print(c.get_lessons_by_group(group_id=c.get_group_id_by_name('02121-ДБ',True)))
    # DEBUG_DATE = datetime.datetime.now()
    # DEBUG_DATE=DEBUG_DATE-datetime.timedelta(days=6)
    # print(DEBUG_DATE, DEBUG_DATE.weekday()+1)

    # ll = c.get_lessons_by_group(group_id=c.get_group_id_by_name('02121-ДБ',True), by_date=DEBUG_DATE)
    # for l in ll:
    #     print('group:%d time:[%s-%s] week:%d day:%d' % (l.group, l.time.start, l.time.end, l.week, l.week_day) )

