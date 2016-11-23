# -*- coding: utf-8 -*-
# this file is being used for testing puropses
import cfg
import telebot
import dbaser
import random
import tools
import shelve
from cfg import slocal
from cfg import glocal

import feedparser
d = feedparser.parse('http://feed.exileed.com/vk/feed/irkutskuniversity/?only_admin=1&at=1')
msg=d['feed']['title']

