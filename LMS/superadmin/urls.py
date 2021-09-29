from django.urls import path

from . import views

app_name = 'superadmin'

urlpatterns = [
    path('dash/', views.dash, name='dash'),
    path('course_list/', views.course_list, name='course_list'),
    path('my_course_list/', views.my_course_list, name='my_course_list'),
    path('course_upload/', views.course_upload, name='course_upload'),
    path('school_list/', views.school_list, name='school_list'),
    path('teacher_list/', views.teacher_list, name='teacher_list'),
    path('student_list/', views.student_list, name='student_list'),
    path('quiz_list/', views.quiz_list, name='quiz_list'),
    path('course_modify/<int:course_id>/', views.course_modify, name='course_modify'),
    path('lecture_modify/<int:lecture_id>/', views.lecture_modify, name='lecture_modify'),
    path('quiz_modify/<int:quiz_id>/', views.quiz_modify, name='quiz_modify'),
    path('final_quiz_modify/<int:final_quiz_id>/', views.final_quiz_modify, name='final_quiz_modify'),
    path('lecture_quiz_upload/<int:course_id>/', views.lecture_quiz_upload, name='lecture_quiz_upload'),
    path('add_lecture/<int:course_id>/', views.add_lecture, name='add_lecture'),
    path('add_quiz/<int:lecture_id>/', views.add_quiz, name='add_quiz'),
    path('add_final_quiz/<int:course_id>/', views.add_final_quiz, name='add_final_quiz'),
]