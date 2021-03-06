import requests
from datetime import datetime
import sched, time
from requests.exceptions import ConnectionError
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS "btcEUR" (
				'scrapeTime' NUMERIC,
				'priceEUR' REAL NOT NULL,
				'volumeCoins' REAL NOT NULL,
				'volumePrice' REAL NOT NULL,
				'numberTrades' INTEGER,
				'latency' INTEGER)''')

url = "https://api.kraken.com/0/public/Ticker?pair=BTCEUR" 

s = sched.scheduler(time.time, time.sleep)

def getData(sc):
	now = datetime.now()
	nowMillis = int(round(time.time() * 1000))
	timestamp1 = now.strftime("%d/%m/%Y %H:%M:%S")
	
	try:
		data = requests.get(url, timeout=1)
		latencyPing = (int(round(time.time() * 1000)) - nowMillis)
		priceEUR = data.json()['result']['XXBTZEUR']['a'][0]
		volumeCoins = data.json()['result']['XXBTZEUR']['v'][1]
		volumePrice = data.json()['result']['XXBTZEUR']['p'][1]
		numberTrades = int(data.json()['result']['XXBTZEUR']['t'][1])

		params = (timestamp1, priceEUR, volumeCoins, volumePrice, numberTrades, latencyPing)

		c = conn.cursor()
		c.execute('''INSERT INTO btcEUR VALUES (?,?,?,?,?,?)''', params)
		conn.commit()
		print("Inserted")

	except ConnectionError as e:
		data = "No response"
		print(data)

	s.enter(5, 1, getData, (sc,))

s.enter(5, 1, getData, (s,))
s.run()

