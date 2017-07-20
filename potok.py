# -*- coding: utf-8 -*-
import requests
from Queue import Queue
import threading
import time
import telepot
import json
token = "416666512:AAFgiPNP8tqtn9EgkVF_Dwww0CU4uvCTLDw"
TelegramBot = telepot.Bot(token)
answer = json.dumps(TelegramBot.getUpdates()[-1])
data = json.loads(answer)
old_id = data['update_id']
LastTradeInfo  = {"ltc_sell":0, "ltc_buy":0, "ltc_last":0, "btc_sell":0, "btc_buy":0, "btc_last":0, "eth_sell":0, "eth_buy":0, "eth_last":0, "dsh_sell":0, "dsh_buy":0, "dsh_last":0}
def crypto_api():
	global queue
	global LastTradeInfo
	list = {'/btc':'btc', '/eth':'eth', '/DASH':'dsh', '/ltc':'ltc'}
	while True:
		time.sleep(10)
		#"закрывает" участок кода только для одного потока
		# в этот момент времени, чтоб не возникало конфликта записи
		# нам не требется, с этим участком работает только один поток
		#LOCK.acquire()
		trade_data = json.loads(requests.get("https://btc-e.com/api/3/ticker/btc_usd-ltc_usd-eth_usd-dsh_usd").content)
		for name in list:
			name = list[name]
			for key in ["sell", "buy", "last"]:
				LastTradeInfo[name+"_"+key] = trade_data[name+"_usd"][key] 
		#LOCK.release()
def chat(old_id, TelegramBot):
	global queue
	global LastTradeInfo
	list = {'/btc':'btc', '/eth':'eth', '/DASH':'dsh', '/ltc':'ltc'}
	while True:
		answer = json.dumps(TelegramBot.getUpdates()[-1])
		data = json.loads(answer)
		new_id = data['update_id']
		text = data['message']['text']
		chat_id = data['message']['chat']['id']
		if new_id != old_id:
			try:
				name = list[text]
				bot_say = "покупаем - " + str(LastTradeInfo[name+"_sell"]) + ", продаем - " + str(LastTradeInfo[name+"_buy"]) + ", последняя - " + str(LastTradeInfo[name+"_last"])
				TelegramBot.sendMessage(chat_id, bot_say)
			except:
				TelegramBot.sendMessage(chat_id, u"Это мы не проходили, это нам не задавали")
		old_id = new_id
queue = Queue()
LOCK = threading.RLock()
thread_ = threading.Thread(target=crypto_api)
thread_.start()
thread_ = threading.Thread(target=chat(old_id, TelegramBot))
thread_.start()
