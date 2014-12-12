from catalog.models import Updater
from catalog.models import Currency
from datetime import date
from datetime import datetime
import lxml.html


class Runner:

	def __init__(self):

		# Инициируем переменные
		self.name = 'Обновление курсов валют (Центральный банк России)'
		self.alias = 'cbr'
		self.message = ''

		self.updater = Updater.objects.take(alias=self.alias, name=self.name)
		self.currency_rub = Currency.objects.take(alias='RUB', name='р.', full_name='Российский рубль', rate=1, quantity=1)

	def run(self):

		# Загружаем данные
		self.message = url = 'http://cbr.ru/eng/currency_base/D_print.aspx?date_req='+date.today().strftime("%d.%m.%Y")
		tree = lxml.html.parse(url)

		table = tree.xpath("//table[@class='CBRTBL']/tr")
		trn = 0
		for tr in table:
			tdn = 0
			if trn == 0 :
				for td in tr:
					if   td[0].text == 'Char code' : char_n = tdn
					elif td[0].text == 'Unit'      : unit_n = tdn
					elif td[0].text == 'Currency'  : curr_n = tdn
					elif td[0].text == 'Rate'      : rate_n = tdn
					tdn += 1
			else :
				for td in tr:
					if   tdn == char_n : char = td.text.strip()
					elif tdn == unit_n : unit = td.text
					elif tdn == curr_n : curr = td.text.strip()
					elif tdn == rate_n : rate = td.text
					tdn += 1
				try:
					currency = Currency.objects.get(alias=char)
				except Currency.DoesNotExist:
					currency = Currency(alias=char, name=char, full_name=curr, rate=1, quantity=1, created=datetime.now(), modified=datetime.now())
					currency.save()
				currency.rate = rate
				currency.quantity = unit
				currency.modified = datetime.now()
				currency.save()
			trn += 1

		return True