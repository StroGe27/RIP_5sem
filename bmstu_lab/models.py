from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=255)

    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'books'

# class VM(models.Model):
#     # статус удален/действует
#     status = models.CharField(max_length=10)
#     class Meta:
#         app_label = 'bmstu_lab'
#         managed = False
#         db_table = 'student'

class Users(models.Model):
    name = models.CharField(max_length=30)
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'users'

class Moderators(models.Model):
    name = models.CharField(max_length=30)
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'moderators'

class Requests(models.Model):
    status = models.CharField(max_length=10)
    date_create = models.DateField()
    date_formation = models.DateField()
    date_complete = models.DateField()
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    moderator = models.ForeignKey('Moderators', on_delete=models.CASCADE)
    def __str__(self):
        return self.user
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'request'

class Orders(models.Model):
    title = models.CharField(max_length=50)
    src = models.CharField(max_length=50)
    definition = models.ForeignKey('Info_orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=10)
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'orders'

class Info_orders(models.Model):
    processor = models.CharField(max_length=10)
    ghz = models.CharField(max_length=10)
    cores = models.CharField(max_length=10)
    ram = models.CharField(max_length=10)
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'info_orders'