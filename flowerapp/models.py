from django.db import models


class Event(models.Model):
    name = models.CharField('Название события', max_length=100)
    
    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'

    def __str__(self):
        return self.name


class Flower(models.Model):
    name = models.CharField('Название цветка', max_length=100)

    class Meta:
        verbose_name = 'Цветок'
        verbose_name_plural = 'Цветы'
        
    def __str__(self):
        return self.name


class Addition(models.Model):
    name = models.CharField('Название доп. опции', max_length=100)
    default_qty = models.PositiveSmallIntegerField('шт', default=1)
    
    class Meta:
        verbose_name = 'Доп. опция'
        verbose_name_plural = 'Доп. опции'

    def __str__(self):
        return self.name


class Bouquet(models.Model):
    name = models.CharField('Название букета', max_length=100)
    description = models.TextField('Описание', blank=True, default='')
    length = models.DecimalField('Высота, см', max_digits=10, decimal_places=2)
    width = models.DecimalField('Ширина, см', max_digits=10, decimal_places=2)
    price = models.DecimalField('Цена букета', max_digits=10, decimal_places=2)
    events = models.ManyToManyField(Event, verbose_name='Событие')
    additions = models.ManyToManyField(Addition, verbose_name='Доп. опции', blank=True)
    image = models.ImageField('Изображение каталог', upload_to='bouquets/catalog/')
    image_card = models.ImageField('Изображение карточка товара', upload_to='bouquets/card/', blank=True)
    flowers = models.ManyToManyField(Flower, verbose_name='Цветы', through='BouquetFlower')
    
    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'
        ordering = ['name']

    def __str__(self):
        return self.name


class BouquetFlower(models.Model):
    bouquet = models.ForeignKey(Bouquet, verbose_name='Букет', on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, verbose_name='Цветок', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('шт', default=1)
    
    class Meta:
        verbose_name = 'Состав букета (позиция)'
        verbose_name_plural = 'Состав букета'
        
    def __str__(self):
        return f'{self.flower.name} x{self.quantity}'


class Courier(models.Model):
    name = models.CharField('Имя курьера', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    
    class Meta:
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Принят'),
        ('assembled', 'Собран'),
        ('delivering', 'Передан в доставку'),
        ('delivered', 'Доставлен'),
    ]

    client_name = models.CharField('Имя клиента', max_length=100)
    client_phone = models.CharField('Телефон клиента', max_length=20)
    client_address = models.TextField('Адрес клиента')
    bouquet = models.ForeignKey(Bouquet, verbose_name='Букет', on_delete=models.CASCADE)
    courier = models.ForeignKey(
        Courier, verbose_name='Курьер',
        on_delete=models.SET_NULL, null=True, blank=True, related_name='orders'
    )
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='accepted')
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']
        
    def __str__(self):
        return f'Заказ #{self.id} - {self.client_name}'


class Consultation(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Заявка принята'),
        ('completed', 'Оказана'),
        ('rejected', 'Отклонена'),
    ]

    client_name = models.CharField('Имя клиента', max_length=100)
    client_phone = models.CharField('Телефон клиента', max_length=20)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='accepted')
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Консультация'
        verbose_name_plural = 'Консультации'

    def __str__(self):
        return f'Консультация - {self.client_name}'
    