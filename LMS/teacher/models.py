from django.db import models
from account.models import User
from school.models import School
from superadmin.models import *
from student.models import Student


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Class(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=50)
    batch_name = models.CharField(max_length=50)
    start_date = models.CharField(max_length=50)
    end_date = models.CharField(max_length=50)

    def __str__(self):
        return self.class_name


class Enroll(models.Model):
    class_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_assigned = models.BooleanField(default=False)
    is_graduated = models.BooleanField(default=False)


class LecturePass(models.Model):
    enroll = models.ForeignKey(Enroll, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    is_passed = models.BooleanField(default=False)


class FinalQuizPass(models.Model):
    enroll = models.ForeignKey(Enroll, on_delete=models.CASCADE)
    final_quiz = models.ForeignKey(FinalQuiz, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    is_passed = models.BooleanField(default=False)