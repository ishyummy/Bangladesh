from django.urls import path

from . import views

app_name = 'school'

urlpatterns = [
    path('signup_info/', views.signup_info, name='signup_info'),
    path('dash/', views.dash, name='dash'),
    path('my_course/', views.my_course, name='my_course'),
    path('course_select/', views.course_select, name='course_select'),
    path('copy_course/<int:course_id>/', views.copy_course, name='copy_course'),
    path('course_modify/<int:course_id>/', views.course_modify, name='course_modify'),
    path('lecture_modify/<int:lecture_id>/', views.lecture_modify, name='lecture_modify'),
    path('quiz_modify/<int:quiz_id>/', views.quiz_modify, name='quiz_modify'),
    path('final_quiz_modify/<int:final_quiz_id>/', views.final_quiz_modify, name='final_quiz_modify'),
    path('lecture_quiz_upload/<int:course_id>/', views.lecture_quiz_upload, name='lecture_quiz_upload'),
    path('add_lecture/<int:course_id>/', views.add_lecture, name='add_lecture'),
    path('add_quiz/<int:lecture_id>/', views.add_quiz, name='add_quiz'),
    path('add_final_quiz/<int:course_id>/', views.add_final_quiz, name='add_final_quiz'),
    path('teacher_list/', views.teacher_list, name='teacher_list'),
    path('student_list/', views.student_list, name='student_list'),
    path('quiz_list/', views.quiz_list, name='quiz_list'),
    path('setting_profile/', views.setting_profile, name='setting_profile'),
    path('setting_photo/', views.setting_photo, name='setting_photo'),
    path('setting_account/', views.setting_account, name='setting_account'),
]