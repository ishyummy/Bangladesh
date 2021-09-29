from django.urls import path

from . import views

app_name = 'student'

urlpatterns = [
    path('signup_info/', views.signup_info, name='signup_info'),
    path('dash/', views.dash, name='dash'),
    path('class_select/', views.class_select, name='class_select'),
    path('class_signup/<int:class_id>/', views.class_signup, name='class_signup'),
    path('my_class/', views.my_class, name='my_class'),
    path('take_class/<int:course_id>/<int:enroll_id>/', views.take_class, name='take_class'),
    path('take_lecture/<int:lecture_id>/<int:enroll_id>/', views.take_lecture, name='take_lecture'),
    path('take_lecture_code/<int:lecture_id>/<int:enroll_id>/', views.take_lecture_code, name='take_lecture_code'),
    path('take_quiz/<int:quiz_id>/<int:enroll_id>/', views.take_quiz, name='take_quiz'),
    path('take_final_quiz/<int:final_quiz_id>/<int:enroll_id>/', views.take_final_quiz, name='take_final_quiz'),
    path('my_quiz/', views.my_quiz, name='my_quiz'),
    path('setting_profile/', views.setting_profile, name='setting_profile'),
    path('setting_photo/', views.setting_photo, name='setting_photo'),
    path('setting_account/', views.setting_account, name='setting_account'),
]