from django.db import models
from config.settings import NULLABLE


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
        verbose_name='название',
        max_length=200,
    )

    model = models.CharField(
        verbose_name='модель',
        max_length=200,
        **NULLABLE
    )

    date_market_launch = models.DateField(
        verbose_name='дата выхода на рынок',
        **NULLABLE
    )

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'

    def __str__(self):
        return f"{self.name} {self.model}, " +\
            f"дата выхода на рынок {self.date_market_launch}"


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
        'название',
        max_length=200,
    )

    level = models.CharField(
        verbose_name='уровень',
        choices=[
            ('factory', 'Завод'),
            ('network', 'Розничная сеть'),
            ('entrepreneur', 'Индивидуальный предприниматель')
        ]
    )

    email = models.EmailField(
        verbose_name='email',
        max_length=200,
        **NULLABLE
    )

    country = models.CharField(
        'страна',
        max_length=200,
        **NULLABLE
    )

    city = models.CharField(
        'город',
        max_length=200,
        **NULLABLE
    )

    street = models.CharField(
        'улица',
        max_length=200,
        **NULLABLE
    )

    house_number = models.IntegerField(
        verbose_name='номер дома',
        **NULLABLE
    )

    product = models.ForeignKey(
        Products,
        on_delete=models.SET_NULL,
        verbose_name='продукт',
        **NULLABLE
    )

    supplier = models.ForeignKey(
        'self',
        verbose_name='поставщик',
        on_delete=models.DO_NOTHING,
        **NULLABLE
        )

    obligation = models.DecimalField(
        verbose_name='задолженность перед поставщиком',
        decimal_places=2,
        max_digits=20,
        default=0.00
    )

    time_created = models.TimeField(
        verbose_name='время создания',
        auto_now=True,
        **NULLABLE
    )

    class Meta:
        verbose_name = 'Сеть'
        verbose_name_plural = 'Сети'

    def __str__(self):
        return f"{self.get_level_display()}: {self.name}"

    def admin_action(self):
        self.obligation = 0

    def get_level(self):
        """
        Возвращает уровень сети.
        Первый объект, который ни на что не ссылается имеет уровень 0.
        """
        count = 0
        if self.supplier is None:
            return 0
        else:
            count = self.supplier.get_level() + 1
            return count
