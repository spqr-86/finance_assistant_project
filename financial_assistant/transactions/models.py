from django.db import models
from django.contrib.auth.models import User

from .validators import validate_not_future_date

class Category(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True, 
        verbose_name='категория'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(
        max_length=3, 
        unique=True,
        verbose_name = 'код валюты'
    )  # ISO 4217 currency code (e.g., USD, EUR)
    name = models.CharField(
        max_length=50,
        verbose_name = 'название валюты'
)
 
    class Meta:
        verbose_name = 'валюта'
        verbose_name_plural = 'валюта'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name = 'тег'
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TYPE_CHOICES = [
        ('income', 'Доход'),
        ('expense', 'Расход'),
    ]

    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('completed', 'Завершено'),
        ('canceled', 'Отменено'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('credit_card', 'Кредитная карта'),
        ('bank_transfer', 'Банковский перевод'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        )
    date = models.DateField(verbose_name='Дата', validators=[validate_not_future_date])
    description = models.CharField(
        max_length=255,
        verbose_name='Описание',
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,
        verbose_name='Категория',
    )
    type = models.CharField(
        max_length=7, 
        choices=TYPE_CHOICES,
        verbose_name='Тип транзакции',
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Сумма',
    )
    currency = models.ForeignKey(
        Currency, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name='Валюта',
    )
    
    tags = models.ManyToManyField(
        Tag, 
        blank=True, 
        verbose_name='Теги',
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Заметки',
    )
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Способ оплаты',
        blank=True, 
        null=True, 
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='completed',
        verbose_name='Статус',
        blank=True, 
        null=True, 
    )
    is_recurring = models.BooleanField(
        default=False,
        verbose_name='Повторяющаяся транзакция',
        blank=True, 
        null=True, 
    )
    recurrence_period = models.CharField(
        max_length=20, 
        blank=True, 
        null=True, 
        verbose_name='Период повторения',
    )  # e.g., 'monthly', 'weekly'


    class Meta:
        ordering = ['-date']
        verbose_name = 'транзакция'
        verbose_name_plural = 'транзакции'

    def __str__(self):
        return f"{self.date} - {self.description} - {self.amount}"
