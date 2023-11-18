from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=30)
    mail = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    role = models.CharField(max_length=30)
    def __str__(self):
        return self.name
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'users'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
class Moderators(models.Model):
    name = models.CharField(max_length=30)
    mail = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'moderators'
    def __str__(self):
        return self.name

class Requests_status(models.Model):
    name_status = models.CharField(max_length=20)
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'requests_status'
    def __str__(self):
        return self.name_status

class Requests(models.Model):
    id = models.BigAutoField(primary_key=True)
    date_create = models.DateField()
    date_formation = models.DateField()
    date_complete = models.DateField()
    moderator = models.ForeignKey('Moderators', on_delete=models.CASCADE)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    status = models.ForeignKey('Requests_status', on_delete=models.CASCADE)
    def __str__(self):
        return self.status, self.date_complete
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'requests'
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

class Order_to_request(models.Model):
    order = models.ForeignKey('Orders', on_delete=models.CASCADE)
    request = models.ForeignKey('Requests', on_delete=models.CASCADE)
    amount_months = models.IntegerField()
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'order_to_request' 
 
class Orders(models.Model):
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    processor = models.CharField(max_length=100)
    ghz = models.FloatField()
    ram = models.IntegerField()
    availableos = models.ForeignKey('AvailableOS', on_delete=models.CASCADE)
    cost = models.IntegerField()
    ip = models.CharField(max_length=20)
    img = models.CharField(max_length=20)
    cluster = models.ForeignKey('Clusters', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title, self.status
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'orders' 
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
 
class AvailableOS(models.Model):
    name = models.CharField(max_length=30)
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'availableos' 
    def __str__(self):
        return self.name

class Clusters(models.Model):
    location = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'clusters' 