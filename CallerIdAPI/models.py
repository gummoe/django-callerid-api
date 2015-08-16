from django.db import models


# Create your models here.
class Contact(models.Model):
    number = models.CharField(max_length=15)
    name = models.CharField(max_length=255)
    context = models.CharField(max_length=255)

    def __str__(self):
        return self.number + ' ' + self.name + ' ' + self.context