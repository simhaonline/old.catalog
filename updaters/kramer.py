import catalog.runner
from catalog.models import *


class Runner(catalog.runner.Runner):

    name  = 'Kramer'
    alias = 'kramer'
    url = {'start': 'http://kramer.ru/',
           'login': 'http://kramer.ru/?login=yes',
           'links': 'http://kramer.ru/partners/prices/',
           'base': 'http://kramer.ru',
           'price': 'http://kramer.ru/filedownload.php?id='}


    def __init__(self):

        super().__init__()

        self.vendor = Vendor.objects.take(name = self.name)
        self.stock = self.take_stock('factory', 'на заказ', 40, 60)

    def run(self):

        # Авторизуемся
        self.login({'backurl': '/',
                    'AUTH_FORM': 'Y',
                    'TYPE': 'AUTH',
                    'USER_LOGIN': self.updater.login,
                    'USER_PASSWORD': self.updater.password,
                    'Login': 'Войти'})

        # Заходим на страницу загрузки
        tree = self.load_html(self.url['links'])

        # Получаем ссылки со страницы
        urls = tree.xpath('//a/@href')
        prices = set()
        for url in urls:
            url = self.url['base'] + url
            if self.url['price'] in url:
                prices.add(url)

        for url in prices:
            request = self.load(url)
            self.parse_price(request)

        # Чистим партии
        Party.objects.clear(stock=self.stock, time = self.start_time)

        # Пишем результат в лог
        self.log()

    def parse_price(self, request):

        from io import BytesIO

        filename = request.headers.get('content-disposition')

        xls_data = BytesIO(request.content)

        if 'Cable' in filename:
            self.parse_cables(xls_data)
        elif 'device' in filename:
            self.parse_devices(xls_data)

    def parse_devices(self, xls_data):

        import xlrd

        # Номера строк и столбцов
        num = {'header': 4}

        # Распознаваемые слова
        word = {'group': 'ГРУППА',
                'article': 'P/N',
                'model': 'Модель',
                'size': 'Размер',
                'name': 'Описание',
                'price': 'Цена, $',
                'dop': 'Примечание'}

        book = xlrd.open_workbook(file_contents = xls_data.read())
        sheet = book.sheet_by_index(0)

        group_name = ''
        category_name = ''
        category = ''

        for row_num in range(sheet.nrows):
            row = sheet.row_values(row_num)

            # Пустые строки
            if row_num < num['header']:
                continue

            # Заголовок таблицы
            elif row_num == num['header']:
                for cel_num, cel in enumerate(row):
                    if str(cel).strip() == word['article']:
                        num['article'] = cel_num
                    elif str(cel).strip() == word['model']:
                        num['model'] = cel_num
                    elif str(cel).strip() == word['size']:
                        num['size'] = cel_num
                    elif str(cel).strip() == word['name']:
                        num['name'] = cel_num
                    elif str(cel).strip() == word['price']:
                        num['price'] = cel_num
                    elif str(cel).strip() == word['dop']:
                        num['dop'] = cel_num

                # Проверяем, все ли столбцы распознались
                if len(num) < len(word):
                    raise(ValueError('Ошибка структуры данных: не все столбцы опознаны.'))

            # Категория
            elif row[num['name']] and not row[num['article']] and not row[num['price']]:
                if word['group'] in row[num['name']]:
                    group_name = row[num['name']]
                else:
                    category_name = row[num['name']]
                category = "Devices: {} {}".format(group_name, category_name)

            # Товар
            elif row[num['name']] and row[num['article']] and row[num['price']]:

                product_ = {}
                party_ = {}

                product_['name'] = "{} {} {}".format(self.vendor.name, row[num['model']], row[num['name']])
                if row[num['size']]:
                    product_['name'] += " (размер: {})".format(str(row[num['size']]))
                product_['name'] = self.fix_name(product_['name'])

                product_['article'] = row[num['article']]
                product_['article'] = self.fix_article(product_['article'])

                try:
                    product = Product.objects.take(article = product_['article'],
                                                   vendor = self.vendor,
                                                   name = product_['name'],
                                                   category = category,
                                                   test = self.test)
                    self.products.append(product.id)
                except ValueError as error:
                    continue

                party_['price'] = row[num['price']]
                party_['price'] = self.fix_price(party_['price'])

                try:
                    party = Party.objects.make(product = product,
                                               stock = self.stock,
                                               product_name = product_['name'],
                                               price = party_['price'],
                                               currency = self.usd,
                                               quantity = -1,
                                               time = self.start_time,
                                               test = self.test)
                    self.parties.append(party.id)
                except ValueError as error:
                    pass

        return True


    def parse_cables(self, xls_data):

        import xlrd

        # Номера строк и столбцов
        num = {'header': 4}

        # Распознаваемые слова
        word = {'article': 'Part Number',
                'model': 'Модель',
                'name': 'Описание',
                'size': 'Метры',
                'price': 'Цена,     $',
                'dop': 'Примечание'}

        book = xlrd.open_workbook(file_contents = xls_data.read())
        sheet = book.sheet_by_index(0)
        category = ''

        for row_num in range(sheet.nrows):
            row = sheet.row_values(row_num)

            # Пустые строки
            if row_num < num['header']:
                continue

            # Заголовок таблицы
            elif row_num == num['header']:
                for cel_num, cel in enumerate(row):
                    if   str(cel).strip() == word['article']:
                        num['article'] = cel_num
                    elif str(cel).strip() == word['model']:
                        num['model'] = cel_num
                    elif str(cel).strip() == word['name']:
                        num['name'] = cel_num
                    elif str(cel).strip() == word['size']:
                        num['size'] = cel_num
                    elif str(cel).strip() == word['price']:
                        num['price'] = cel_num
                    elif str(cel).strip() == word['dop']:
                        num['dop'] = cel_num

                # Проверяем, все ли столбцы распознались
                if len(num) < len(word) + 1:
                    raise(ValueError('Ошибка структуры данных: не все столбцы опознаны.'))

            # Категория
            elif row[num['name']] and not row[num['article']] and not row[num['price']]:
                category = 'Cables: {}'.format(row[num['name']])

            # Товар
            elif row[num['name']] and row[num['article']] and row[num['price']]:

                product_ = {}
                party_ = {}

                product_['name'] = '{} {} {}'.format(self.vendor.name, row[num['model']], row[num['name']])
                if row[num['size']]:
                    product_['name'] = '{} (длина: {} м.)'.format(product_['name'],
                                                                  str(row[num['size']]).replace('.', ','))
                product_['name'] = self.fix_name(product_['name'])

                product_['article'] = row[num['article']]
                product_['article'] = self.fix_article(product_['article'])

                try:
                    product = Product.objects.take(article = product_['article'],
                                                   vendor = self.vendor,
                                                   name = product_['name'],
                                                   category = category,
                                                   test = self.test)
                    self.products.append(product.id)
                except ValueError as error:
                    continue

                party_['price'] = row[num['price']]
                party_['price'] = self.fix_price(party_['price'])

                try:
                    party = Party.objects.make(product = product,
                                               stock = self.stock,
                                               product_name = product_['name'],
                                               price = party_['price'],
                                               currency = self.usd,
                                               quantity = -1,
                                               time = self.start_time,
                                               test = self.test)
                    self.parties.append(party.id)
                except ValueError as error:
                    pass
