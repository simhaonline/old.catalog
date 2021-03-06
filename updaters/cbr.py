from datetime import date

import catalog.runner
from catalog.models import *
from anodos.models import Log


class Runner(catalog.runner.Runner):


    name  = 'Центральный банк России'
    alias = 'cbr'
    test = False

    def __init__(self):

        super().__init__()

        self.url = {
            'start' : 'http://cbr.ru/',
            'data'  : 'http://cbr.ru/eng/currency_base/D_print.aspx?date_req={}'\
                    .format(date.today().strftime("%d.%m.%Y"))}

        self.currencies = []


    def run(self):

        # Получаем HTML-данные
        r = self.load_cookie()
        tree = self.load_html(self.url['data'])

        if tree is None:
            return False

        self.parse(tree)

        Log.objects.add(subject = "catalog.updater.{}".format(self.updater.alias),
                        channel = "info",
                        title = "Updated",
                        description = "Обновлены курсы валют: {} шт.".format(len(self.currencies)))

    def parse(self, tree):

        # Номера столбцов
        num = {}

        # Распознаваемые слова
        word = {'alias': 'Char code',
                'quantity': 'Unit',
                'name': 'Currency',
                'rate': 'Rate'}

        table = tree.xpath("//table[@class='CBRTBL']/tr")
        for trn, tr in enumerate(table):

            # Заголовок таблицы
            if trn == 0:
                for tdn, td in enumerate(tr):

                    if td[0].text == word['alias']:
                        num['alias'] = tdn

                    elif td[0].text == word['quantity']:
                        num['quantity'] = tdn

                    elif td[0].text == word['name']:
                        num['name'] = tdn

                    elif td[0].text == word['rate']:
                        num['rate'] = tdn

            # Валюта
            else:

                # Определяем значения переменных
                alias = tr[num['alias']].text.strip()
                quantity = tr[num['quantity']].text.strip()
                name = tr[num['name']].text.strip()
                rate = tr[num['rate']].text.strip()

                # Записываем информацию в базу
                currency = Currency.objects.take(alias = alias,
                                                 name = name,
                                                 full_name = name,
                                                 rate = rate,
                                                 quantity = quantity,
                                                 test = self.test)
                currency.rate = rate
                currency.quantity = quantity
                currency.modified = timezone.now()
                currency.save()

                self.currencies.append(currency.id)
