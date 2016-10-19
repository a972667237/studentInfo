from django.db import models

# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    stu_no = models.CharField(max_length=50)
    profess = models.CharField(max_length=100)
    collega = models.CharField(max_length=100)
    className = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name
