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


class Course(models.Model):
    course_id = models.CharField(max_length=20)
    course_name = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    place = models.CharField(max_length=100)
    teacher = models.CharField(max_length=10)

class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
