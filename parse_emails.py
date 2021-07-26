#!/usr/bin/python3

import base64
import datetime
import os
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from html.parser import HTMLParser

class TransactionType(str, Enum):
	BUY = 'Buy'
	SELL = 'Sell'

class HTMLFilter(HTMLParser):
    text = ""
    def handle_data(self, data):
        self.text += data

@dataclass
class Transaction:
	transaction_date: datetime
	share_code: str
	transaction_type: TransactionType
	unit_price: float
	units: int
	buy_price: float	

	def __lt__(self, other):
		return self.transaction_date < other.transaction_date

	def __repr__(self):
		transaction_date = self.transaction_date.strftime("%Y/%m/%d")
		return f"{transaction_date},{self.share_code},{self.transaction_type.value},{self.unit_price},{self.units},{self.buy_price}"

PATTERN = re.compile("(bought|sold) (\d+) units in (.*)\s\((.*)\) at a price of \$(.*) per unit")
BUY_PRICE_PATTERN = re.compile("The total settlement amount, including brokerage, is \$(\d+\.\d+)\.")
BUY_PRICE_PATTERN_FALLBACK = re.compile("The total settlement amount, including the trade fee, is \$(\d+\.\d+)\.")
# Date: 29 Apr 2021 12:04:07 +1000
DATE_PATTERN = re.compile("Date: ([0-3]?[0-9] .* ([0-9]){4})")

location = sys.argv[1]
results = []

for email in os.listdir(location):
	if not email.endswith(".eml"):
		continue

	with open(Path(location, email)) as f:
		# An email from CommSec has 2 ----boundary blocks
		# The 0th block is the email metadata
		# The first block after the boundary is the contents
		# The second block is the PDF
		contents = f.read().split("----boundary")
		transaction_date = datetime.datetime.strptime(DATE_PATTERN.search(contents[0]).group(1), "%d %b %Y")

		encoded_contents = contents[1].split("Content-Transfer-Encoding: base64")[1]
		email_contents = str(base64.b64decode(encoded_contents))
		f = HTMLFilter()
		f.feed(email_contents)
		email_contents = f.text

		transaction_type = TransactionType.BUY if PATTERN.search(email_contents).group(1) == "bought" else TransactionType.SELL
		units = PATTERN.search(email_contents).group(2)
		share = PATTERN.search(email_contents).group(3)
		share_code = PATTERN.search(email_contents).group(4)
		unit_price = PATTERN.search(email_contents).group(5)
		try:
			buy_price = BUY_PRICE_PATTERN.search(email_contents).group(1)
		except Exception:
			buy_price = BUY_PRICE_PATTERN_FALLBACK.search(email_contents).group(1)

		transaction = Transaction(transaction_date, share_code, transaction_type, unit_price, units, buy_price)
		results.append(transaction)

results.sort()
for result in results:
	print(result)
