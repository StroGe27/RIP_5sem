from django.db import models

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
    status = models.CharField(max_length=10)
    processor = models.CharField(max_length=100)
    ghz = models.FloatField()
    ram = models.IntegerField()
    rate = models.CharField(max_length=100)
    availableos = models.CharField(max_length=10)
    cost = models.IntegerField()
    class Meta:
        app_label = 'bmstu_lab'
        managed = False
        db_table = 'orders'
