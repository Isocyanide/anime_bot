from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import (Updater, MessageHandler, Filters, CommandHandler, InlineQueryHandler,
						  ConversationHandler, RegexHandler, CallbackQueryHandler)
import logging
import copy
import pprint
import pickle

import requests
import xml.etree.ElementTree as ET
import pprint

pp = pprint.PrettyPrinter(indent=4)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(token="810413428:AAEebRUP04reN7_V5INK84ZpkWGZTiJCPxc")

dispatcher = updater.dispatcher
j = updater.job_queue

list1 = []

button = ["Magnet"]

def feed_in():

	url1 = "http://www.horriblesubs.info/rss.php?res=720"

	res = requests.get(url1)

	with open("animefeed.xml",'wb') as f:
		f.write(res.content)

	tree = ET.parse('animefeed.xml')
	root = tree.getroot()

	feedlist = []

	for item in root.findall('./channel/item'):

		feed = {}

		for child in item:
			feed[child.tag] = child.text.encode('utf8')

		feedlist.append(feed)

	return feedlist


def notif(bot, update):

	list1_file = open('list1.db','rb+')

	try:
		list1 = pickle.load(list1_file)
	except:
		list1 = []

	list1_file.close()

	feed = feed_in()

	list1_file = open('list1.db','wb+')

	list2 = feed
	final_list = [i for i in list2 if i not in list1]
	pickle.dump(list2, list1_file)

	list1_file.close()


	for i in final_list:

		title = str(i['title'])
		hyphen_index = title.rfind('-')
		title = title[16:hyphen_index].strip()

		magnet = str(i['link'])[2:]
		l = magnet.find("&")
		magnet = magnet[:l]
		text = f"{title} has aired \nMagnet:\n```{magnet}```"

		try:
			pass
			bot.send_message(chat_id = "@AnimeNotifChannel" , text = text, parse_mode = 'markdown')
		except BaseException as e:
			print(e)


job = j.run_repeating(notif, interval = 3600, first = 0)
updater.start_polling()
updater.idle()
