from django.db import models
from account.models import User


class Course(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    depth = models.IntegerField(default=1)
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField(default=1)
    category = models.CharField(max_length=50, default='Academic')
    difficulty = models.CharField(max_length=50, default='Beginner')
    level = models.CharField(max_length=50, default='All school')
    tag = models.CharField(max_length=50, default='Robotics')
    type = models.CharField(max_length=50, default='Beginner')

    def __str__(self):
        return self.title


class Quiz(models.Model):
    title = models.CharField(max_length=50)
    pass_score = models.IntegerField(default=60)

    def __str__(self):
        return self.title


class Lecture(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quiz = models.OneToOneField(Quiz, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    video_link = models.CharField(max_length=50, null=False)
    code = models.TextField()
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.content


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.CharField(max_length=50, null=False)
    image = models.ImageField(null=True, blank=True)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.content


class FinalQuiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    pass_score = models.IntegerField(default=60)

    def __str__(self):
        return self.title


class FinalQuestion(models.Model):
    final_quiz = models.ForeignKey(FinalQuiz, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.content


class FinalOption(models.Model):
    final_question = models.ForeignKey(FinalQuestion, on_delete=models.CASCADE)
    content = models.CharField(max_length=50, null=False)
    image = models.ImageField(null=True, blank=True)
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.content
