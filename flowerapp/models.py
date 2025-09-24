from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Flower(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Addition(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Bouquet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    size = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    events = models.ManyToManyField(Event)
    flowers = models.ManyToManyField(Flower)
    additions = models.ManyToManyField(Addition, blank=True)

    def __str__(self):
        return self.name


class Courier(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Принят'),
        ('assembled', 'Собран'),
        ('delivering', 'Передан в доставку'),
        ('delivered', 'Доставлен'),
    ]

    client_name = models.CharField(max_length=100)
    client_phone = models.CharField(max_length=20)
    client_address = models.TextField()
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)
    courier = models.ForeignKey(Courier, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='accepted')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id} - {self.client_name}"


class Consultation(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Заявка принята'),
        ('completed', 'Оказана'),
        ('rejected', 'Отклонена'),
    ]

    client_name = models.CharField(max_length=100)
    client_phone = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='accepted')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Консультация - {self.client_name}"