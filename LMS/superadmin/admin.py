from django.contrib import admin
from .models import *

admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(FinalQuiz)
admin.site.register(FinalQuestion)
admin.site.register(FinalOption)
