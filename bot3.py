# -*- coding: utf-8 -*-
import requests
import telepot
import json
token = "416666512:AAFgiPNP8tqtn9EgkVF_Dwww0CU4uvCTLDw"
TelegramBot = telepot.Bot(token)
answer = json.dumps(TelegramBot.getUpdates()[-1])
data = json.loads(answer)
old_id = data['update_id']
api_url = "https://btc-e.com/api/3/ticker/"
list = {'/btc':'btc', '/eth':'eth', '/DASH':'dsh', '/ltc':'ltc'}
while True:
	answer = json.dumps(TelegramBot.getUpdates()[-1])
	data = json.loads(answer)
	new_id = data['update_id']
	text = data['message']['text']
	chat_id = data['message']['chat']['id']
	if new_id != old_id:
		try:
			name = list[text] + "_usd"
			source = api_url + name
			trade_data = json.loads(requests.get(source).content)[name]
			bot_say = "продаем - " + str(trade_data["buy"]) + ", покупаем - " + str(trade_data["sell"]) + ", последняя - " + str(trade_data["last"])
			TelegramBot.sendMessage(chat_id, bot_say)
		except:
			TelegramBot.sendMessage(chat_id, "Это мы не проходили, это нам не задавали")
	old_id = new_id
