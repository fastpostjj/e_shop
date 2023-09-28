from django.db import models
from django.utils.translation import ugettext as _
from config.settings import NULLABLE


"""
Модель сети по продаже электроники.
Сеть должна представляет собой иерархическую структуру из 3 уровней:

-  Завод;
-  Розничная сеть;
-  Индивидуальный предприниматель.

Каждое звено сети ссылается только на одного поставщика оборудования
(не обязательно предыдущего по иерархии). Важно отметить, что уровень
иерархии определяется не названием звена, а отношением к остальным
элементам сети, т.е. завод всегда находится на 0 уровне, а если розничная
сеть относится напрямую к заводу, минуя остальные звенья - её уровень - 1.

Каждое звено сети должно обладать следующими элементами:
Название;
Контакты:
Email;
Страна;
Город;
Улица;
Номер дома;
Продукты:
Название;
Модель;
Дата выхода продукта на рынок;
Поставщик (предыдущий по иерархии объект сети);
Задолженность перед поставщиком в денежном выражении с точностью до копеек;
Время создания (заполняется автоматически при создании).
Сделать вывод в админ-панели созданных объектов
"""


class Products(models.Model):
    """
    Класс Продукты:
    Название;
    Модель;
    Дата выхода продукта на рынок;
    name,
    model,
    date_market_launch
    """
    name = models.CharField(
        verbose_name=_('name'),
        max_length=200,
    )

    model = models.CharField(
        verbose_name=_('name'),
        max_length=200,
        **NULLABLE
    )

    date_market_launch = models.DateField(
        verbose_name=_("date of market launch"),
        **NULLABLE
    )

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return f"Продукт{self.name}, модель:{self.model}, " +\
            "дата выхода на рынок: {self.date_market_launch}"


class Retails(models.Model):
    """
    Класс модели сети по продаже электроники.
    name,
    level,
    email,
    country,
    city,
    street,
    house_number,
    product,
    supplier,
    obligation,
    time_created
    """
    name = models.CharField(
        _('name'),
        max_length=200,
    )

    level = models.CharField(
        verbose_name=_('level'),
        choices=[
            ('factory', 'Завод'),
            ('network', 'Розничная сеть'),
            ('entrepreneur', 'Индивидуальный предприниматель')
        ]
    )

    email = models.EmailField(
        verbose_name=_('email'),
        max_length=200,
        **NULLABLE
    )

    country = models.CharField(
        _('country'),
        max_length=200,
        **NULLABLE
    )

    city = models.CharField(
        _('city'),
        max_length=200,
        **NULLABLE
    )

    street = models.CharField(
        _('street'),
        max_length=200,
        **NULLABLE
    )

    house_number = models.IntegerField(
        verbose_name=_('house number'),
        **NULLABLE
    )

    product = models.ForeignKey(
        Products,
        on_delete=models.SET_NULL,
        verbose_name=_('products'),
        **NULLABLE
    )

    supplier = models.ForeignKey(
        'self',
        verbose_name=_('supplier'),
        on_delete=models.DO_NOTHING,
        **NULLABLE
        )

    obligation = models.DecimalField(
        verbose_name=_('indebtedness to the supplier'),
        default=0.00
    )

    time_created = models.TimeField(
        verbose_name=_('creation time'),
        auto_now=True,
        **NULLABLE
    )

    class Meta:
        verbose_name = _('network model')
        verbose_name_plural = _('network models')

    def __str__(self):
        return f"{self.name} {self.level}"
