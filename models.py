import uuid

from django.db import models
from django.utils import timezone
from django.conf import settings

class DistributorManager(models.Manager):

    def get_all_dicted(self):
        result = []
        for o in self.all():
            result.append(o.get_dicted())
        return result

    def take(self, *args, **kwargs):

        alias = str(kwargs.get('alias', '')).strip()
        name = str(kwargs.get('name', '')).strip()

        if not alias:
            return None

        try:
            result = self.get(alias = alias)

        except Distributor.DoesNotExist:

            if not name:
                return None

            result = Distributor(
                alias = alias,
                name = name)
            result.save()

        return result


class Distributor(models.Model):

    id = models.BigAutoField(primary_key = True, editable = False)

    name = models.TextField(db_index = True)
    alias = models.TextField(unique = True)
    description = models.TextField(null = True, default = '')

    state = models.BooleanField(default = True, db_index = True)
    created = models.DateTimeField(default = timezone.now, db_index = True)
    modified = models.DateTimeField(default = timezone.now, db_index = True)

    objects = DistributorManager()

    def get_dicted(self):

        result = {}

        result['id'] = str(self.id)
        result['name'] = self.name
        result['alias'] = self.alias
        result['description'] = self.description
        result['state'] = self.state
        result['created'] = str(self.created)
        result['modified'] = str(self.modified)

        return result

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class UpdaterManager(models.Manager):

    def get_all_dicted(self):
        result = []
        for o in self.all():
            result.append(o.get_dicted())
        return result

    def take(self, alias, name, distributor = None):

        try:
            updater = self.get(alias = alias)
        except Updater.DoesNotExist:
            updater = Updater(
                alias = alias,
                name = name,
                distributor = distributor)
            updater.save()
        return updater


class Updater(models.Model):

    id = models.BigAutoField(primary_key = True, editable = False)
    distributor = models.ForeignKey(Distributor, related_name = '+', null = True, default = None)

    name = models.TextField(db_index = True)
    alias = models.TextField(unique = True)
    login = models.TextField(null = True, default = '')
    password = models.TextField(null = True, default = '')
    updated = models.DateTimeField(default = timezone.now)

    state = models.BooleanField(default = True, db_index = True)
    created = models.DateTimeField(default = timezone.now, db_index = True)
    modified = models.DateTimeField(default = timezone.now, db_index = True)

    objects = UpdaterManager()

    def get_dicted(self):

        result = {}

        result['id'] = str(self.id)
        result['name'] = self.name
        result['alias'] = self.alias
        result['login'] = self.login
        result['password'] = self.password
        result['state'] = self.state
        result['updated'] = str(self.updated)
        result['created'] = str(self.created)
        result['modified'] = str(self.modified)

        try:
            result['distributor'] = self.distributor.get_dicted()
        except Exception:
            result['distributor'] = None

        return result

    def __str__(self):
        return self.name


    class Meta:
        ordering = ['name']


class StockManager(models.Manager):


    def get_all_dicted(self):
        result = []
        for o in self.all():
            result.append(o.get_dicted())
        return result


    def take(self, alias, name, delivery_time_min = 10, delivery_time_max = 20,
            distributor=None):

        try:
            stock = self.get(alias = alias)
        except Stock.DoesNotExist:
            stock = Stock(
                alias = alias,
                name = name,
                delivery_time_min = delivery_time_min,
                delivery_time_max = delivery_time_max,
                distributor = distributor)
            stock.save()
        return stock


class Stock(models.Model):

    id = models.BigAutoField(primary_key = True, editable = False)
    distributor = models.ForeignKey(Distributor, related_name = '+', null = True, default = None)

    name = models.TextField(db_index = True)
    alias = models.TextField(unique = True)
    description = models.TextField(null = True, default = '')
    delivery_time_min = models.BigIntegerField(db_index = True)
    delivery_time_max = models.BigIntegerField(db_index = True)
    state = models.BooleanField(default = True, db_index = True)
    created = models.DateTimeField(default = timezone.now, db_index = True)
    modified = models.DateTimeField(default = timezone.now, db_index = True)

    objects = StockManager()


    def get_dicted(self):

        result = {}

        result['id'] = str(self.id)
        result['name'] = self.name
        result['alias'] = self.alias
        result['delivery_time_min'] = self.delivery_time_min
        result['delivery_time_max'] = self.delivery_time_max
        result['state'] = self.state
        result['created'] = str(self.created)
        result['modified'] = str(self.modified)

        try:
            result['distributor'] = self.distributor.get_dicted()
        except Exception:
            result['distributor'] = None

        return result


    def __str__(self):
        return self.name


    class Meta:
        ordering = ['name']


class CategoryManager(models.Manager):


    def get_all_dicted(self):
        result = []
        for o in self.all():
            result.append(o.get_dicted())
        return result


    def get_category_tree(self, tree, parent = None, state = False):
        "Функция: дерево категорий (используется рекурсия)."

        # Получаем список дочерних категорий
        categories = self.filter(parent = parent).order_by('order')
        if state:
            categories = self.filter(parent = parent).filter(state = True)
        else:
            categories = self.filter(parent = parent)


        # Проходим по списку категорий с рекурсивным погружением
        for category in categories:
            tree.append(category)
            tree = self.get_category_tree(tree, parent = category, state = state)

        return tree


    def get_category_tree_html(self, root, parent = None, first = None, state = False):
        "Функция: дерево категорий (используется рекурсия)."

        # Импортируем
        from lxml import etree

        # Получаем список дочерних категорий
        if state:
            categories = self.filter(parent = parent).filter(state = True)
        else:
            categories = self.filter(parent = parent)

        # Проходим по списку категорий с рекурсивным погружением
        if len(categories):
            ul = etree.SubElement(root, "ul")
            ul.attrib['class'] = 'no-bullet'
            if first:
                li = etree.SubElement(ul, "li")
                i = etree.SubElement(li, "i")
                i.text = ''
                i.attrib['class'] = 'fa fa-circle-thin'
                a = etree.SubElement(li, "a")
                a.attrib['data-do'] = 'filter-products-select-category'
                a.attrib['data-id'] = ''
                a.attrib['class'] = 'tm-li-category-name'
                a.text = 'Все категории'

            for category in categories:
                li = etree.SubElement(ul, "li")

                # Если есть дочерние
                if state:
                    childs = self.filter(parent=category).filter(state=True).order_by('order')
                else:
                    childs = self.filter(parent=category).order_by('order')

                if len(childs):
                    li.attrib['class'] = 'closed'
                    i = etree.SubElement(li, "i")
                    i.attrib['data-do'] = 'switch-li-status'
                    i.attrib['data-state'] = 'closed'
                    i.text = ''
                    i.attrib['class'] = 'fa fa-plus-square-o'
                else:
                    i = etree.SubElement(li, "i")
                    i.text = ''
                    i.attrib['class'] = 'fa fa-circle-thin'
                a = etree.SubElement(li, "a")
                a.attrib['data-do'] = 'filter-products-select-category'
                a.attrib['data-id'] = str(category.id)
                a.attrib['class'] = 'tm-li-category-name'
                a.text = category.name
                self.get_category_tree_html(root = li, parent = category, state = state)

        # Возвращаем результат
        return root


class Category(models.Model):

    id = models.BigAutoField(primary_key = True, editable = False)
    parent = models.ForeignKey('self', related_name = '+', null = True, default = None)

    name = models.TextField(db_index = True)
    alias = models.TextField(null = True, default = '', db_index = True)
    description = models.TextField(null = True, default = '')
    level = models.BigIntegerField(default = 0, db_index = True)
    order = models.BigIntegerField(default = 999999, db_index = True)
    path = models.TextField(null = True, default = '', db_index = True)
    img = models.TextField(null = True, default = '')

    state = models.BooleanField(default = True, db_index = True)
    created = models.DateTimeField(default = timezone.now, db_index = True)
    modified = models.DateTimeField(default = timezone.now, db_index = True)

    objects = CategoryManager()

    def _name_leveled(self):
        return '{}{}'.format('— ' * self.level, self.name)

    name_leveled = property(_name_leveled)

    def _img_path(self):
        if self.img:
            return '{}/{}/{}/{}'.format(settings.BASE_DIR, 'media', 'category', self.img)
        else:
            return None

    img_path = property(_img_path)

    def _img_url(self):
        if self.img:
            return '{}/{}/{}'.format('media', 'category', self.img)
        else:
            return None

    def get_dicted(self):

        result = {}

        result['id'] = str(self.id)
        result['name'] = self.name
        result['name_leveled'] = '{} {}'.format('— ' * self.level, self.name)
        result['alias'] = self.alias
        result['description'] = self.description
        result['level'] = self.level
        result['order'] = self.order
        result['path'] = self.path
        result['img_url'] = self.img_url
        result['state'] = self.state
        result['created'] = str(self.created)
        result['modified'] = str(self.modified)

        try:
            result['parent'] = self.parent.get_dicted()
        except Exception:
            result['parent'] = None

        return result


    def __str__(self):
        return self.name


    class Meta:
        ordering = ['order']


class VendorManager(models.Manager):


    def get_all_dicted(self):
        result = []
        for o in self.all():
            result.append(o.get_dicted())
        return result


    def take(self, name, alias = None, get_doubles = True):

        import unidecode

        if not name:
            name = 'None'

        name = str(name)

        if alias:
            alias = str(alias)
        else:
            alias = name

        alias = unidecode.unidecode(alias)
        alias = alias.lower()

        translation_map = {
            ord(' ') : '-', ord('&') : 'and', ord('\'') : '',
            ord('(') : '', ord(')') : '', ord('[') : '',
            ord(']') : '', ord('.') : '', ord(',') : '',
            ord('+') : '', ord('/') : ''}

        alias = alias.translate(translation_map)

        alias = alias.strip()[:100]

        try:
            vendor = self.get(alias=alias)
        except Vendor.DoesNotExist:
            try:
                vendor = self.get(name=name)
            except Vendor.DoesNotExist:
                vendor = Vendor(alias = alias, name = name)
                vendor.save()

        if vendor.double and get_doubles:
            vendor = vendor.double

        return vendor

    # Return all objects in Pandas.DataFrame
    def get_df(self, **kwargs):

        import pandas as pd

        columns = ['id', 'double', 'name', 'alias', 'description', 'state', 'created', 'modified']

        vendors_ = self.filter(**kvargs).values(*columns)

        vendors = {}
        for key in columns:
            vendors[key] = []
        for vendor_ in vendors_:
            for key in columns:
                vendors[key].append(vendor_[key])

        vendors = pd.DataFrame(vendors, columns = columns)
        return vendors


class Vendor(models.Model):

    id = models.BigAutoField(primary_key = True, editable = False)
    double = models.ForeignKey('self', related_name = '+', null = True, default = None)

    name = models.TextField(unique = True)
    alias = models.TextField(unique = True)
    description = models.TextField(null = True, default = '')
    img = models.TextField(null = True, default = '')

    state = models.BooleanField(default = True, db_index = True)
    created = models.DateTimeField(default = timezone.now, db_index = True)
    modified = models.DateTimeField(default = timezone.now, db_index = True)

    objects = VendorManager()

    def _img_path(self):
        if self.img:
            return '{}/{}/{}/{}'.format(settings.BASE_DIR, 'media', 'vendor', self.img)
        else:
            return None

    img_path = property(_img_path)

    def _img_url(self):
        if self.img:
            return '{}/{}/{}'.format('media', 'vendor', self.img)
        else:
            return None

    img_url = property(_img_url)

    def get_dicted(self):

        result = {}

        result['id'] = str(self.id)
        result['name'] = self.name
        result['alias'] = self.alias
        result['description'] = self.description
        result['img_url'] = self.img_url
        result['state'] = self.state
        result['created'] = str(self.created)
        result['modified'] = str(self.modified)

        try:
            result['double'] = self.double.get_dicted()
        except Exception:
            result['double'] = None

        return result

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class UnitManager(models.Manager):

    def get_all_dicted(self):
        result = []
        for o in self.all():
            result.append(o.get_dicted())
        return result

    def take(self, alias, name):
        try:
            unit = self.get(alias=alias)
        except Unit.DoesNotExist:
            unit = Unit(
                alias = alias,
                name = name)
            unit.save()
        return unit


class Unit(models.Model):

    id = models.BigAutoField(primary_key = True, editable = False)

    name = models.TextField(db_index = True)
    name_short = models.TextField(null = True, default = '', db_index = True)
    name_short_xml = models.TextField(null = True, default = '')
    alias = models.TextField(unique = True)

    state = models.BooleanField(default = True, db_index = True)
    created = models.DateTimeField(default = timezone.now, db_index = True)
    modified = models.DateTimeField(default = timezone.now, db_index = True)

    objects = UnitManager()


    def get_dicted(self):

        result = {}

        result['id'] = str(self.id)
        result['name'] = self.name
        result['name_short'] = self.name_short
        result['name_short_xml'] = self.name_short_xml
        result['alias'] = self.alias
        result['state'] = self.state
        result['created'] = str(self.created)
        result['modified'] = str(self.modified)

        return result

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class PriceTypeManager(models.Manager):


    def get_all_dicted(self):
        result = []
        for o in self.all():
            result.append(o.get_dicted())
        return result


    def take(self, alias, name):
        try:
            price_type = self.get(alias=alias)
        except PriceType.DoesNotExist:
            price_type = PriceType(
                alias = alias,
                name = name)
            price_type.save()
        return price_type


class PriceType(models.Model):

    id = models.BigAutoField(primary_key = True, editable = False)

    name = models.TextField(db_index = True)
    alias = models.TextField(unique = True)
    multiplier = models.DecimalField(max_digits = 10, decimal_places = 4, default = 1.0, db_index = True)

    state = models.BooleanField(default = True, db_index = True)
    created = models.DateTimeField(default = timezone.now, db_index = True)
    modified = models.DateTimeField(default = timezone.now, db_index = True)

    objects = PriceTypeManager()

    def get_dicted(self):

        result = {}

        result['id'] = str(self.id)
        result['name'] = self.name
        result['alias'] = self.alias
        result['state'] = self.state
        result['multiplier'] = str(self.multiplier)
        result['created'] = str(self.created)
        result['modified'] = str(self.modified)

        return result

    def __str__(self):
        return self.name


    class Meta:
        ordering = ['name']


class CurrencyManager(models.Manager):


    def get_all_dicted(self):
        result = []
        for o in self.all():
            result.append(o.get_dicted())
        return result


    def take(self, alias, name, full_name, rate = 1, quantity = 1, test = False):
        try:
            currency = self.get(alias = alias)
        except Currency.DoesNotExist:
            currency = Currency(alias = alias, name = name, full_name = full_name,
                                rate = rate, quantity = quantity)
            currency.save()

        if test:
            print(currency)

        return currency


class Currency(models.Model):

    id = models.BigAutoField(primary_key = True, editable = False)

    name = models.TextField(db_index = True)
    full_name = models.TextField(db_index = True)
    alias = models.TextField(unique = True)
    rate = models.DecimalField(max_digits = 10, decimal_places = 4, db_index = True)
    quantity = models.DecimalField(max_digits = 10, decimal_places = 3, db_index = True)

    state = models.BooleanField(default = True, db_index = True)
    created = models.DateTimeField(default = timezone.now, db_index = True)
    modified = models.DateTimeField(default = timezone.now, db_index = True)

    objects = CurrencyManager()

    def get_dicted(self):

        result = {}

        result['id'] = str(self.id)
        result['name'] = self.name
        result['full_name'] = self.full_name
        result['alias'] = self.alias
        result['rate'] = str(self.rate)
        result['quantity'] = str(self.quantity)
        result['state'] = self.state
        result['created'] = str(self.created)
        result['modified'] = str(self.modified)

        return result

    def __str__(self):
        return self.name

    def _to_rub(self):

        return self.rate / quantity

    to_rub = property(_to_rub)

    class Meta:
        ordering = ['alias']


class ProductManager(models.Manager):

    def take(self, article, vendor, name, **kwargs):

        if not article:
            raise(ValueError('Внимание: не указан артикул!'))
        if not vendor:
            raise(ValueError('Внимание: не указан производитель!'))
        if not name:
            raise(ValueError('Внимание: не указано имя!'))

        try:
            product = self.get(article__iexact = article, vendor = vendor)

        except Product.DoesNotExist:

            product = Product()

            product.vendor = vendor
            product.name = name
            product.article = article
            product.unit = kwargs.get('unit', Unit.objects.take(alias = 'pcs', name = 'шт.'))
            product.description = kwargs.get('description', '')

            product.set_alias()
            product.save()

        if product.double:
            product = product.double

        if not product.description and kwargs.get('description', ''):
            product.description = kwargs.get('description', '')
            product.modified = timezone.now()
            product.save()

        if kwargs.get('test', False):
            print('{} {}'.format(product.vendor, product.article))

        ProductInputName.objects.take(product = product, name = name)
        ProductInputCategory.objects.take(product = product, category = kwargs.get('category', ''))

        return product

    # Return objects in Pandas.DataFrame
    def get_df(self, **kwargs):

        import pandas as pd

        columns = ['id', 'vendor', 'category', 'unit', 'double', 'price_type', 'currency', 'name',
                   'article', 'alias', 'description', 'edited', 'tested', 'for_export', 'on_stock',
                   'on_transit', 'on_factory', 'price', 'fixed', 'state', 'created', 'modified']

        products_ = self.filter(**kwargs).values(*columns)

        products = {}
        for key in columns:
            products[key] = []
        for product_ in products_:
            for key in columns:
                products[key].append(product_[key])

        df = pd.DataFrame(products, columns = columns)

        df.on_stock = df.on_stock.astype('float64')
        df.on_transit = df.on_transit.astype('float64')
        df.on_factory = df.on_factory.astype('float64')

        return df

class Product(models.Model):

    id = models.BigAutoField(primary_key = True, editable = False)
    vendor = models.ForeignKey(Vendor, related_name = '+')
    category = models.ForeignKey(Category, related_name = '+', null = True, default = None)
    unit = models.ForeignKey(Unit, related_name = '+', null = True, default = None)
    double = models.ForeignKey('self', related_name = '+', null = True, default = None)
    price_type = models.ForeignKey(PriceType, related_name = '+', null = True, default = None)
    currency = models.ForeignKey(Currency, related_name = '+', null = True, default = None)

    name = models.TextField(db_index = True)
    article = models.TextField(db_index = True)
    alias = models.TextField(db_index = True, null = True, default = None)
    description = models.TextField(null = True, default = '')
    edited = models.BooleanField(default = False, db_index = True)
    tested = models.BooleanField(default = False, db_index = True)
    for_export = models.BooleanField(default = False, db_index = True)

    on_stock = models.BigIntegerField(null = True, default = 0, db_index = True)
    on_transit = models.BigIntegerField(null = True, default = 0, db_index = True)
    on_factory = models.BigIntegerField(null = True, default = 0, db_index = True)

    price = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None, db_index = True)
    fixed = models.BooleanField(default = False, db_index = True)

    img = models.TextField(null = True, default = '')

    state = models.BooleanField(default = True, db_index = True)
    created = models.DateTimeField(default = timezone.now, db_index = True)
    modified = models.DateTimeField(default = timezone.now, db_index = True)

    objects = ProductManager()

    class Meta:
        ordering = ['name']
        unique_together = ('vendor', 'article')

    def _img_path(self):
        if self.img:
            return '{}/{}/{}/{}'.format(settings.BASE_DIR, 'media', 'product', self.img)
        else:
            return None

    img_path = property(_img_path)

    def _img_url(self):
        if self.img:
            return '{}/{}/{}'.format('media', 'vendor', self.img)
        else:
            return None

    img_url = property(_img_url)

    def set_alias(self):

        import unidecode

        # Собираем в единую строку
        self.alias = ' '.join([self.vendor.name, self.article, self.name])

        translation_map = {ord('&') : 'and', ord('\'') : '', ord('(') : ' ', ord(')') : ' ',
                           ord('[') : ' ', ord(']') : ' ', ord('.') : ' ', ord(',') : ' ',
                           ord('+') : ' ', ord('/') : ' '}
        self.alias = self.alias.translate(translation_map)

        translation_map_o = {ord('o'): '0', ord('е'): 'e', ord('т'): 't', ord('у'): 'y',
                             ord('о'): 'o', ord('р'): 'p', ord('а'): 'a', ord('н'): 'h',
                             ord('к'): 'k', ord('l'): 'i', ord('х'): 'x', ord('c'): 'c',
                             ord('в'): 'b', ord('м'): 'm'}
        self.alias = '{} {}'.format(self.alias, self.alias.translate(translation_map))

        self.alias = unidecode.unidecode(self.alias).lower()
        self.alias = self.alias.strip()

        while '  ' in self.alias:
            self.alias = self.alias.replace('  ', ' ')

        self.alias = self.alias[:2500]

        return True

    def get_dicted(self):

        result = {}

        result['id'] = str(self.id)

        links = {
            'vendor': self.vendor,
            'category': self.category,
            'unit': self.unit,
            'double': self.double,
            'price_type': self.currency}

        for key, link in links.items():
            if link:
                result[key] = link.get_dicted()
            else:
                result[key] = None

        result['name'] = str(self.name)
        result['article'] = str(self.article)
        result['description'] = str(self.description)
        result['edited'] = str(self.edited)
        result['for_export'] = str(self.for_export)

        result['on_stock'] = str(self.on_stock)
        result['on_transit'] = str(self.on_transit)
        result['on_factory'] = str(self.on_factory)

        result['price'] = str(self.price)
        result['fixed'] = str(self.fixed)

        result['img_url'] = self.img_url

        result['state'] = str(self.state)
        result['created'] = str(self.created)
        result['modified'] = str(self.modified)

        result['parties'] = []
        for party in Party.objects.filter(product = self):
            result['parties'].append(party.get_dicted())

        return result


    def __str__(self):
        return '{} {}'.format(self.vendor.name, self.article)

    def _get_input_name(self):

        names = []
        for name in self.input_names.all():
            names.append(name.name)

        name = ' '.join(names)

        return name

    input_name = property(_get_input_name)

    def _get_input_category(self):

        categories = []
        for category in self.input_categories.all():
            categories.append(category.category)

        try:
            category = ' '.join(categories)
        except TypeError:
            category = ''

        return category

    input_category = property(_get_input_category)

    def _get_price_str(self):

        try:
            currency = self.currency
        except Exception:
            return ''

        if self.price:
            price = '{:,}'.format(round(self.price, 2)).replace(',', ' ').replace('.', ',')
        else:
            return ''

        return '{} {}'.format(price, currency.name)

    price_str = property(_get_price_str)


    def _get_price_xml(self):

        try:
            currency = self.currency
        except:
            return ''

        if self.price:
            price = '{:,}'.format(round(self.price, 2)).replace(',', '&nbsp;').replace('.', ',')
        else:
            return '?'

        return '{}&nbsp;{}'.format(price, currency.name)

    price_xml = property(_get_price_xml)


    def _get_on_stock_xml(self):
        if self.on_stock == -1:
            quantity = '&infin;'
        elif self.on_stock:
            quantity = str(self.on_stock)
        elif self.on_stock is None:
            quantity = '?'
        else:
            quantity = ''
        return quantity

    on_stock_xml = property(_get_on_stock_xml)


    def _get_on_transit_xml(self):
        if self.on_transit == -1:
            quantity = '&infin;'
        elif self.on_transit:
            quantity = str(self.on_transit)
        elif self.on_transit is None:
            quantity = '?'
        else:
            quantity = ''
        return quantity

    on_transit_xml = property(_get_on_transit_xml)


    def _get_on_factory_xml(self):

        if self.on_factory == -1:
            quantity = '&infin;'
        elif self.on_factory:
            quantity = str(self.on_factory)
        elif self.on_factory is None:
            quantity = '?'
        else:
            quantity = ''
        return quantity

    on_factory_xml = property(_get_on_factory_xml)


    # TODO Need rafactoring
    def recalculate(self):

        rp = PriceType.objects.take(
            alias = 'RP',
            name = 'Розничная цена')

        rub = Currency.objects.take(alias = 'RUB', name = 'р.', full_name = 'Российский рубль',
                                    rate = 1, quantity = 1)

        quantities = {'stock' : [0], 'transit' : [0], 'factory' : [0]}

        undef_quantities = {'stock' : None, 'transit' : None, 'factory' : None}

        prices = []

        parties = Party.objects.filter(product = self, stock__state = True, stock__distributor__state = True)

        # Проходим по всем партиям продукта
        for party in parties:

            if party.quantity:
                if 'stock' in party.stock.alias:
                    quantities['stock'].append(party.quantity)
                elif 'transit' in party.stock.alias:
                    quantities['transit'].append(party.quantity)
                elif 'factory' in party.stock.alias:
                    quantities['factory'].append(party.quantity)

            elif party.quantity is None:
                if 'stock' in party.stock.alias:
                    undef_quantities['stock'] = True
                elif 'transit' in party.stock.alias:
                    undef_quantities['transit'] = True
                elif 'factory' in party.stock.alias:
                    undef_quantities['factory'] = True

            elif party.quantity == 0:
                continue

            if party.price and party.currency and party.price_type:
                prices.append(party.price * party.currency.rate * party.price_type.multiplier / party.currency.quantity)

        # Записываем информацию в базу
        if -1 in quantities['stock']:
            self.on_stock = -1
        elif sum(quantities['stock']) > 0:
            self.on_stock = sum(quantities['stock'])
        elif undef_quantities['stock']:
            self.on_stock = None
        else:
            self.on_stock = 0

        if -1 in quantities['transit']:
            self.on_transit = -1
        elif sum(quantities['transit']) > 0:
            self.on_transit = sum(quantities['transit'])
        elif undef_quantities['transit']:
            self.on_transit = None
        else:
            self.on_transit = 0

        if -1 in quantities['factory']:
            self.on_factory = -1
        elif sum(quantities['factory']) > 0:
            self.on_factory = sum(quantities['factory'])
        elif undef_quantities['factory']:
            self.on_factory = None
        else:
            self.on_factory = 0

        if len(prices):
            self.price = min(prices)
            self.price_type = rp
            self.currency = rub
        else:
            self.price = None
            self.price_type = rp
            self.currency = rub

        self.save()


class ProductInputNameManager(models.Manager):

    def take(self, product, name):

        try:
            name = self.get(product = product, name = name)
        except ProductInputName.DoesNotExist:
            name = ProductInputName(product = product, name = name)
            name.save()

        return name

    # Return objects in Pandas.DataFrame
    def get_df(self, **kwargs):

        import pandas as pd

        columns = ['id', 'product', 'name', 'state', 'created', 'modified']

        names_ = self.filter(**kwargs).values(*columns)

        names = {}
        for key in columns:
            names[key] = []
        for name_ in names_:
            for key in columns:
                names[key].append(name_[key])

        names = pd.DataFrame(names, columns = columns)
        return names

class ProductInputName(models.Model):

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    product = models.ForeignKey(Product, related_name = 'input_names')

    name = models.TextField(null = True, default = None, db_index = True)

    state = models.BooleanField(default = True, db_index = True)
    created = models.DateTimeField(default = timezone.now, db_index = True)
    modified = models.DateTimeField(default = timezone.now, db_index = True)

    objects = ProductInputNameManager()

    class Meta:
        db_table = 'catalog_product_input_name'
        ordering = ['name']
        unique_together = ('product', 'name')


class ProductInputCategoryManager(models.Manager):

    def take(self, product, category):

        try:
            category = self.get(product = product, category = category)
        except ProductInputCategory.DoesNotExist:
            category = ProductInputCategory(
                product = product,
                category = category)
            category.save()

        return category

    # Return objects in Pandas.DataFrame
    def get_df(self, **kwargs):

        import pandas as pd

        columns = ['id', 'product', 'category', 'state', 'created', 'modified']

        categories_ = self.filter(**kwargs).values(*columns)

        categories = {}
        for key in columns:
            categories[key] = []
        for category_ in categories_:
            for key in columns:
                categories[key].append(category_[key])

        categories = pd.DataFrame(categories, columns = columns)
        return categories


class ProductInputCategory(models.Model):

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    product = models.ForeignKey(Product, related_name = 'input_categories')

    category = models.TextField(null = True, default = None, db_index = True)

    state = models.BooleanField(default = True, db_index = True)
    created = models.DateTimeField(default = timezone.now, db_index = True)
    modified = models.DateTimeField(default = timezone.now, db_index = True)

    objects = ProductInputCategoryManager()

    class Meta:
        db_table = 'catalog_product_input_category'
        ordering = ['category']
        unique_together = ('product', 'category')


class PartyManager(models.Manager):

    def get_all_dicted(self):
        result = []
        for o in self.all():
            result.append(o.get_dicted())
        return result

    def make(self, product, stock, **kwargs):

        if product is None:
            raise(ValueError('Ошибка! Не указан товар.'))
        if stock is None:
            raise(ValueError('Ошибка! Не указан склад.'))

        time = kwargs.get('time', None)
        if time:
            Party.objects.filter(product = product, stock = stock, created__lt = time).delete()

        article = kwargs.get('article', None)
        price = kwargs.get('price', None)
        price_type = kwargs.get('price_type', PriceType.objects.take(alias = 'DP', name = 'Диллерская цена'))
        currency = kwargs.get('currency', None)
        price_out = kwargs.get('price', None)
        price_type_out = kwargs.get('price_type', PriceType.objects.take(alias = 'RP', name = 'Розничная цена'))
        currency_out = kwargs.get('currency', None)
        quantity = kwargs.get('quantity', 0)
        unit = kwargs.get('unit', Unit.objects.take(alias = 'pcs', name = 'шт.'))

        product_name = kwargs.get('product_name', product.name)



        # Проверяем количество
        if quantity == 0:
            raise(ValueError('Внимание: нулевое количество! {} {}'.format(product, quantity)))

        # Проверяем входную цену
        if price and not currency:
            price = None
        if currency and not price:
            curency = None

        # Проверяем выходную цену
        if price_out and not currency_out:
            price_out = None
        if currency_out and not price_out:
            curency_out = None

        # Приводим выходную цену к рубляем, если нужно
        rub = Currency.objects.take(alias = 'RUB', name = 'р.', full_name = 'Российский рубль',
                                    rate = 1, quantity = 1)
        if price_out and currency_out.id != rub.id:
            price_out = price_out * self.currency.rate / self.currency.quantity

        # Вычисляем выходную цену, если нужно
        if price and not price_out:
            price_out = price * currency.rate / currency.quantity * price_type.multiplier

        party = Party(product = product, stock = stock, article = article, price = price,
                      price_type = price_type, currency = currency, price_out = price_out,
                      price_type_out = price_type_out, currency_out = currency_out,
                      quantity = quantity, unit = unit, product_name = product_name)
        party.save()

        if kwargs.get('test', False):
            print('{} {} = {}; {} on {}'.format(party.product.vendor.name,
                                                party.product.article,
                                                party.price_str,
                                                party.quantity,
                                                party.stock.alias))

        party.product.recalculate()

        return party


    def clear(self, stock, time = None):
        if time:
            Party.objects.filter(stock = stock, created__lt = time).delete()
        else:
            Party.objects.filter(stock = stock).delete()
        return True


class Party(models.Model):

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    product = models.ForeignKey(Product, related_name = '+')
    stock = models.ForeignKey(Stock, related_name = '+')
    price_type = models.ForeignKey(PriceType, related_name = '+', null = True, default = None)
    currency = models.ForeignKey(Currency, related_name = '+', null = True, default = None)
    price_type_out = models.ForeignKey(PriceType, related_name = '+', null = True, default = None)
    currency_out = models.ForeignKey(Currency, related_name = '+', null = True, default = None)
    unit = models.ForeignKey(Unit, related_name = '+', null = True, default = None)

    article = models.TextField(null = True, default = None, db_index = True) # Артикул поставщика
    price = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None, db_index = True)
    price_out = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None, db_index = True)
    quantity = models.BigIntegerField(null = True, default = None, db_index = True)
    product_name = models.TextField(null = True, default = None)

    state = models.BooleanField(default = True, db_index = True)
    created = models.DateTimeField(default = timezone.now, db_index = True)
    modified = models.DateTimeField(default = timezone.now, db_index = True)

    objects = PartyManager()


    def get_dicted(self):

        result = {}

        result['id'] = str(self.id)
        result['article'] = self.article
        result['price'] = str(self.price)
        result['price_out'] = str(self.price_out)
        result['quantity'] = str(self.quantity)
        result['product_name'] = self.product_name
        result['state'] = self.state
        result['created'] = str(self.created)
        result['modified'] = str(self.modified)

        try:
            result['stock'] = self.stock.get_dicted()
        except Exception:
            result['stock'] = None

        try:
            result['price_type'] = self.price_type.get_dicted()
        except Exception:
            result['price_type'] = None

        try:
            result['currency'] = self.currency.get_dicted()
        except Exception:
            result['currency'] = None

        try:
            result['price_type_out'] = self.price_type_out.get_dicted()
        except Exception:
            result['price_type_out'] = None

        try:
            result['currency_out'] = self.currency_out.get_dicted()
        except Exception:
            result['currency_out'] = None

        try:
            result['unit'] = self.unit.get_dicted()
        except Exception:
            result['unit'] = None

        result['price_str'] = self._get_price_str()
        result['price_xml'] = self._get_price_xml()
        result['price_out_str'] = self._get_price_out_str()
        result['price_out_xml'] = self._get_price_out_xml()

        return result

    def _round_price_str(self, price):
        price = '{:,}'.format(round(price, 2))
        price = price.replace(',', ' ')
        price = price.replace('.', ',')
        return price

    def _get_price_str(self):
        if self.price and self.currency:
            price = self._round_price_str(self.price)
            price = '{} {}'.format(price, self.currency.name)
        else:
            price = ''
        return price

    price_str = property(_get_price_str)

    def _get_price_xml(self):
        if self.price and self.currency:
            price = self._round_price_str(self.price)
            price = '{}&nbsp;{}'.format(price, self.currency.name)
        else:
            price = ''
        return price

    price_xml = property(_get_price_xml)

    def _get_price_out_str(self):

        if self.price_out and self.currency_out:
            price_out = self._round_price_str(self.price_out)
            price_out = '{}&nbsp;{}'.format(price_out, self.currency_out.name)
        elif self.price and self.currency:
            price_out = self.price * self.currency.rate / self.currency.quantity * self.price_type.multiplier
            price_out = self._round_price_str(price_out)
            currency = Currency.objects.take(alias = 'RUB', name = 'р.',
                                             full_name = 'Российский рубль', rate = 1, quantity = 1)
            price_out = '{} {}'.format(price_out, currency.name)
        else:
            price_out = ''
        return price_out

    price_out_str = property(_get_price_out_str)

    def _get_price_out_xml(self):

        if self.price_out and self.currency_out:
            price_out = self._round_price_str(self.price_out)
            price_out = '{}&nbsp;{}'.format(price_out, self.currency_out.name)
        elif self.price and self.currency:
            price_out = self.price * self.currency.rate / self.currency.quantity * self.price_type.multiplier
            price_out = self._round_price_str(price_out)
            currency = Currency.objects.take(alias = 'RUB', name = 'р.',
                                             full_name = 'Российский рубль', rate = 1, quantity = 1)
            price_out = '{}&nbsp;{}'.format(price_out, currency.name)
        else:
            price_out = ''
        return price_out

    price_out_xml = property(_get_price_out_xml)

    class Meta:
        ordering = ['-created']


class PartyHystory(models.Model):

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    product = models.ForeignKey(Product, related_name = '+')
    stock = models.ForeignKey(Stock, related_name = '+')
    price_type = models.ForeignKey(PriceType, related_name = '+', null = True, default = None)
    currency = models.ForeignKey(Currency, related_name = '+', null = True, default = None)
    price_type_out = models.ForeignKey(PriceType, related_name = '+', null = True, default = None)
    currency_out = models.ForeignKey(Currency, related_name = '+', null = True, default = None)

    price = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
    price_out = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, default = None)
    quantity = models.BigIntegerField(null = True, default = None)
    unit = models.ForeignKey(Unit, null = True, default = None, db_index = True)
    date = models.DateField(db_index = True)


    def get_dicted(self):

        result = {}

        result['id'] = str(self.id)
        result['article'] = self.article
        result['price'] = str(self.price)
        result['price_out'] = self.price_out
        result['quantity'] = self.description
        result['comment'] = self.comment
        result['date'] = str(self.date)

        try:
            result['product'] = self.product.get_dicted()
        except Exception:
            result['product'] = None

        try:
            result['stock'] = self.stock.get_dicted()
        except Exception:
            result['stock'] = None

        try:
            result['price_type'] = self.price_type.get_dicted()
        except Exception:
            result['price_type'] = None

        try:
            result['currency'] = self.currency.get_dicted()
        except Exception:
            result['currency'] = None

        try:
            result['price_type_out'] = self.price_type_out.get_dicted()
        except Exception:
            result['price_type_out'] = None

        try:
            result['currency_out'] = self.currency_out.get_dicted()
        except Exception:
            result['currency_out'] = None

        try:
            result['unit'] = self.unit.get_dicted()
        except Exception:
            result['unit'] = None

        return result

    class Meta:
        ordering = ['-date']


class ProductPhotoManager(models.Manager):

    def load(self, *args, **kwargs):

        # Библиотеки. необходимые для загрузки данных в память
        import requests
#        from io import BytesIO
        from django.conf import settings

        # Инициализация переменных
        product = kwargs.get('product', None)
        source = str(kwargs.get('source', '')).strip()

        # Если указаны продукт и источник изображения
        if product and source:

            # Получаем объект с базы, или создаём его
            try:
                photo = self.get(product = product, source = source)
            except Exception:
                photo = ProductPhoto(product = product, source = source)

            # Если изображение ещё не загружено
            if not photo.patch:
                r = requests.get(source)
#                print(type(r.content))
#                print(photo.id)

                # Получаем разрешение файла
                s = source.split('.')
                ext = s[len(s) - 1].lower()
#                print(ext)

                photo.src = '{media_url}catalog/photos/{id}.{ext}'.format(
                    media_url = settings.MEDIA_URL,
                    id = photo.id,
                    ext = ext)
                photo.patch = '{media_dir}catalog/photos/{id}.{ext}'.format(
                    media_dir = settings.MEDIA_DIR,
                    id = photo.id,
                    ext = ext)

#                print(photo.src)
#                print(photo.patch)

                # Записывваем фото на диск
                f = open(photo.patch, 'wb')
                f.write(r.content)
                f.close()

                # Записываем изменения в память
                photo.save()

            print('ProductPhoto {} {}: {}'.format(
                product.vendor.name,
                product.article,
                source))


class ProductPhoto(models.Model):

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    product = models.ForeignKey(Product, related_name = '+', null = True, default = None)
    trumb = models.ForeignKey('self', related_name = '+', null = True, default = None)

    name = models.TextField(null = True, default = '', db_index = True)
    patch = models.TextField(null = True, default = '')
    src = models.TextField(null = True, default = '')
    description = models.TextField(null = True, default = '')
    source = models.TextField(null = True, default = '')
    hash_md5 = models.TextField(null = True, default = None, db_index = True)

    state = models.BooleanField(default = True, db_index = True)
    created = models.DateTimeField(default = timezone.now, db_index = True)
    modified = models.DateTimeField(default = timezone.now, db_index = True)

    objects = ProductPhotoManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']

models = {
    'distributor': Distributor,
    'updater': Updater,
    'stock': Stock,
    'category': Category,
    'vendor': Vendor,
    'unit': Unit,
    'pricetype': PriceType,
    'currency': Currency,
    'product': Product,
    'party': Party,
    'partyhystory': PartyHystory,

    'productphoto': ProductPhoto}
