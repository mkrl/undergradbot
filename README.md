# undergradbot
A test python Telegram bot working via pyTelegramBotAPI. 

## Возможности

* Парсер расписания
* Простой парсер университетских новостей
* Поиск преподавателя
* Расписание для студентов на каждый день, время до начала пары

## Команды

* **/start** - Инициирует диалог с ботом, показывает стартовый экран приветствия
* **/register** - Регистрирует студента в группе (необходимо для получения расписания)
* **/today** - Выводит список сегодняшних занятий для студента, показывает время до начала следующего занятия
* **/getteacher** - Поиск преподавателя, показывает какая сейчас пара у определённого преподавателя, а также его кафедру, если занятий сейчас нет
* **/news** - Новости с портала Университета
* **/fact** - Случайный математический факт

## Requirements

* pyTelegramBotAPI
* feedparser
* pytest



## Чейнджлог

* Nov 23: Большой апдейт (потому что я вовремя не пушу промежуточные версии). Нормальный парсер расписания, поиск преподавателей по частичному совпадению, новая БД с полями для кафедр, сам парсер перенёс в отдельный файл. Написал несколько классов для парсера. Добавил readme. Ведём логи в bot.log. Перевёл все команды на русский.
* May 24: RSS парсер новостей, поправил несколько багов
* May 21: Стабильная версия с базовым функционалом, конвертировал бд в кириллицу (тестим с помощью /unicode)
* May 20: Initial commit, регистрация, структура бд, разбивка кода по отдельным файлам
