from django.shortcuts import render, redirect
from .models import *
from school.models import *
from student.models import *
from superadmin.models import *
from account.forms import UserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password


def signup_info(request):
    if request.method == 'POST':
        school_id = request.POST.get("select_school", None)
        school = School.objects.get(id=school_id)

        new_teacher = Teacher.objects.create(
            user=request.user,
            name=request.POST['name'],
            school=school
        )
        request.user.is_info_set = True
        request.user.user_name = request.POST['name']
        request.user.save()

        return redirect('teacher:dash')
    else:
        school_list = School.objects.all()
        context = {'school_list': school_list}
        return render(request, 'teacher/teacher_signup_info.html', context)


def dash(request):
    teacher = Teacher.objects.get(user=request.user)
    courses = Course.objects.filter(author=request.user).count()
    enroll_list = Enroll.objects.filter(teacher=teacher).filter(is_assigned=True)
    students = enroll_list.count()
    class_taken = 0
    for enroll in enroll_list:
        lecture_pass_list = enroll.lecturepass_set.all()
        for lecture_pass in lecture_pass_list:
            if lecture_pass.is_passed:
                class_taken += 1

    context = {'courses': courses, 'students': students, 'class_taken': class_taken}
    return render(request, 'teacher/teacher_dash.html', context)


def my_course(request):
    course_list = Course.objects.filter(author=request.user)
    context = {'course_list': course_list}
    return render(request, 'teacher/teacher_my_course.html', context)


def course_select(request):
    teacher = Teacher.objects.get(user=request.user)
    school = teacher.school.user
    course_list = Course.objects.filter(author=school)
    context = {'course_list': course_list}
    return render(request, 'teacher/teacher_course_select.html', context)


def copy_course(request, course_id):
    course = Course.objects.get(id=course_id)
    lecture_list = Lecture.objects.filter(course=course)
    final_quiz_list = FinalQuiz.objects.filter(course=course)
    course.pk = None  # how to copy object
    course.author = request.user
    course.depth = 3
    course.save()

    for lecture in lecture_list:
        quiz = lecture.quiz
        question_list = Question.objects.filter(quiz=quiz)
        lecture.pk = None
        quiz.pk = None
        quiz.save()

        for question in question_list:
            option_list = Option.objects.filter(question=question)
            question.pk = None
            question.quiz = quiz
            question.save()
            for option in option_list:
                option.pk = None
                option.question = question
                option.save()

        lecture.course = course
        lecture.quiz = quiz
        lecture.save()

    for final_quiz in final_quiz_list:
        final_question_list = FinalQuestion.objects.filter(final_quiz=final_quiz)
        final_quiz.pk = None
        final_quiz.course = course
        final_quiz.save()

        for final_question in final_question_list:
            final_option_list = FinalOption.objects.filter(final_question=final_question)
            final_question.pk = None
            final_question.final_quiz = final_quiz
            final_question.save()

            for final_option in final_option_list:
                final_option.pk = None
                final_option.final_question = final_question
                final_option.save()

    return redirect('teacher:my_course')


def my_class(request):
    teacher = Teacher.objects.get(user=request.user)
    class_list = Class.objects.filter(teacher=teacher)
    context = {'class_list': class_list}
    return render(request, 'teacher/teacher_my_class.html', context)


def create_class(request):
    if request.method == 'POST':
        teacher = Teacher.objects.get(user=request.user)
        course_id = request.POST.get("select_course", None)
        course = Course.objects.get(id=course_id)

        new_class = Class.objects.create(
            school=teacher.school,
            teacher=teacher,
            course=course,
            class_name=request.POST['class_name'],
            batch_name=request.POST['batch_name'],
            start_date=request.POST['start_date'],
            end_date=request.POST['end_date'],
        )
        return redirect('teacher:my_class')
    else:
        course_list = Course.objects.filter(author=request.user)
        context = {'course_list': course_list}
        return render(request, 'teacher/teacher_create_class.html', context)


def enroll_select(request):
    teacher = Teacher.objects.get(user=request.user)
    enroll_list = Enroll.objects.filter(teacher=teacher).filter(is_assigned=False)
    context = {'enroll_list': enroll_list}
    return render(request, 'teacher/teacher_enroll_select.html', context)


def class_assign(request, enroll_id):
    enroll = Enroll.objects.get(id=enroll_id)
    enroll.is_assigned = True
    enroll.save()
    course = enroll.class_class.course
    lecture_list = Lecture.objects.filter(course=course)
    final_quiz_list = FinalQuiz.objects.filter(course=course)

    for lecture in lecture_list:
        new_lecture_pass = LecturePass.objects.create(
            enroll=enroll,
            lecture=lecture,
            student=enroll.student
        )
    for final_quiz in final_quiz_list:
        new_final_quiz_pass = FinalQuizPass.objects.create(
            enroll=enroll,
            final_quiz=final_quiz,
            student=enroll.student
        )

    return redirect('teacher:enroll_select')


def course_modify(request, course_id):
    course = Course.objects.get(id=course_id)

    if course.author != request.user:
        return redirect('/')
    if request.method == "POST":
        level = request.POST.get("level", None)
        category = request.POST.get("category", None)
        difficulty = request.POST.get("difficulty", None)
        course.title = request.POST['title']
        course.description = request.POST['description']
        course.price = request.POST['price']
        course.level = level
        course.category = category
        course.difficulty = difficulty
        course.tag = request.POST.get('tag_radio')
        course.type = request.POST.get('type_radio')
        course.save()

        return redirect('teacher:lecture_quiz_upload', course.id)
    else:
        context = {'course': course}
        return render(request, 'teacher/teacher_course_modify.html', context)


def lecture_quiz_upload(request, course_id):
    course = Course.objects.get(id=course_id)
    if course.author != request.user:
        print('here')
        return redirect('/')

    lecture_list = course.lecture_set.all()
    final_quiz_list = course.finalquiz_set.all()
    context = {'lecture_list': lecture_list, 'final_quiz_list': final_quiz_list, 'course': course}
    return render(request, 'teacher/teacher_lecture_quiz_upload.html', context)


def add_lecture(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == "POST":
        new_quiz = Quiz.objects.create(title='temp')
        new_lecture = Lecture.objects.create(
            course=course,
            quiz=new_quiz,
            title=request.POST['title'],
            video_link=request.POST['video_link'],
            code=request.POST['code'],
            file=request.FILES.get('file')
        )
        return redirect('teacher:add_quiz', new_lecture.id)
    else:
        return render(request, 'teacher/teacher_add_lecture.html')


def add_quiz(request, lecture_id):
    lecture = Lecture.objects.get(id=lecture_id)
    course = Course.objects.get(id=lecture.course.id)
    quiz = Quiz.objects.get(id=lecture.quiz.id)

    if request.method == "POST":
        quiz.title = request.POST['title']

        new_question = Question.objects.create(
            quiz=quiz,
            content=request.POST['content'],
            image=request.FILES.get('image1')
        )
        try:
            a = request.POST['correct1']
            bool1 = True
        except:
            bool1 = False
        new_option_1 = Option.objects.create(
            question=new_question,
            content=request.POST['option_content_1'],
            image=request.FILES.get('image2'),
            is_answer=bool1
        )

        try:
            a = request.POST['correct2']
            bool2 = True
        except:
            bool2 = False
        new_option_2 = Option.objects.create(
            question=new_question,
            content=request.POST['option_content_2'],
            image=request.FILES.get('image3'),
            is_answer=bool2
        )

        try:
            a = request.POST['correct3']
            bool3 = True
        except:
            bool3 = False
        new_option_3 = Option.objects.create(
            question=new_question,
            content=request.POST['option_content_3'],
            image=request.FILES.get('image4'),
            is_answer=bool3
        )
        if request.POST['score'] == '60':
            score = 60
        elif request.POST['score'] == '70':
            score = 70
        else:
            score = 80
        quiz.pass_score = score
        quiz.save()
        return redirect('teacher:lecture_quiz_upload', course.id)
    else:
        return render(request, 'teacher/teacher_add_quiz.html')


def add_final_quiz(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == "POST":
        new_final_quiz = FinalQuiz.objects.create(
            course=course,
            title=request.POST['title']
        )
        new_final_question = FinalQuestion.objects.create(
            final_quiz=new_final_quiz,
            content=request.POST['content'],
            image=request.FILES.get('image1')
        )
        try:
            a = request.POST['correct1']
            bool1 = True
        except:
            bool1 = False
        new_final_option_1 = FinalOption.objects.create(
            final_question=new_final_question,
            content=request.POST['option_content_1'],
            image=request.FILES.get('image2'),
            is_answer=bool1
        )

        try:
            a = request.POST['correct2']
            bool2 = True
        except:
            bool2 = False
        new_final_option_2 = FinalOption.objects.create(
            final_question=new_final_question,
            content=request.POST['option_content_2'],
            image=request.FILES.get('image3'),
            is_answer=bool2
        )

        try:
            a = request.POST['correct3']
            bool3 = True
        except:
            bool3 = False
        new_final_option_3 = FinalOption.objects.create(
            final_question=new_final_question,
            content=request.POST['option_content_3'],
            image=request.FILES.get('image4'),
            is_answer=bool3
        )
        if request.POST['score'] == '60':
            score = 60
        elif request.POST['score'] == '70':
            score = 70
        else:
            score = 80
        new_final_quiz.pass_score = score
        new_final_quiz.save()
        return redirect('teacher:lecture_quiz_upload', course.id)
    else:
        return render(request, 'teacher/teacher_add_quiz.html')


def lecture_modify(request, lecture_id):
    lecture = Lecture.objects.get(id=lecture_id)
    if request.method == "POST":
        lecture.title = request.POST['title']
        lecture.video_link = request.POST['video_link']
        lecture.code = request.POST['code']
        lecture.file = request.FILES.get('file')
        lecture.save()
        return redirect('teacher:lecture_quiz_upload', lecture.course.id)
    else:
        context = {'lecture': lecture}
        return render(request, 'teacher/teacher_lecture_modify.html', context)


def quiz_modify(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    question = quiz.question_set.all()[0]
    option_list = question.option_set.all()
    option1 = option_list[0]
    option2 = option_list[1]
    option3 = option_list[2]

    if request.method == "POST":
        quiz.title = request.POST['title']
        question.content = request.POST['content']
        question.image = request.FILES.get('image1')
        question.save()

        if request.POST.get('correct1') == 'on':
            option1.is_answer = True
        else:
            option1.is_answer = False
        option1.content = request.POST['option_content_1']
        option1.image = request.FILES.get('image2')
        option1.save()

        if request.POST.get('correct2') == 'on':
            option2.is_answer = True
        else:
            option2.is_answer = False

        option2.content = request.POST['option_content_2']
        option2.image = request.FILES.get('image3')
        option2.save()

        if request.POST.get('correct3') == 'on':
            option3.is_answer = True
        else:
            option3.is_answer = False

        option3.content = request.POST['option_content_3']
        option3.image = request.FILES.get('image4')
        option3.save()

        if request.POST['score'] == '60':
            score = 60
        elif request.POST['score'] == '70':
            score = 70
        else:
            score = 80
        quiz.pass_score = score
        quiz.save()

        return redirect('teacher:lecture_quiz_upload', quiz.lecture.course.id)
    else:
        context = {'quiz': quiz, 'question': question, 'option1': option1, 'option2': option2, 'option3': option3}
        return render(request, 'teacher/teacher_quiz_modify.html', context)


def final_quiz_modify(request, final_quiz_id):
    final_quiz = FinalQuiz.objects.get(id=final_quiz_id)
    final_question = final_quiz.finalquestion_set.all()[0]
    final_option_list = final_question.finaloption_set.all()
    option1 = final_option_list[0]
    option2 = final_option_list[1]
    option3 = final_option_list[2]

    if request.method == "POST":
        final_quiz.title = request.POST['title']
        final_question.content = request.POST['content']
        final_question.image = request.FILES.get('image1')
        final_question.save()

        if request.POST.get('correct1') == 'on':
            option1.is_answer = True
        else:
            option1.is_answer = False
        option1.content = request.POST['option_content_1']
        option1.image = request.FILES.get('image2')
        option1.save()

        if request.POST.get('correct2') == 'on':
            option2.is_answer = True
        else:
            option2.is_answer = False

        option2.content = request.POST['option_content_2']
        option2.image = request.FILES.get('image3')
        option2.save()

        if request.POST.get('correct3') == 'on':
            option3.is_answer = True
        else:
            option3.is_answer = False

        option3.content = request.POST['option_content_3']
        option3.image = request.FILES.get('image4')
        option3.save()

        if request.POST['score'] == '60':
            score = 60
        elif request.POST['score'] == '70':
            score = 70
        else:
            score = 80
        final_quiz.pass_score = score
        final_quiz.save()
        return redirect('teacher:lecture_quiz_upload', final_quiz.course.id)
    else:
        context = {'quiz': final_quiz, 'question': final_question, 'option1': option1, 'option2': option2, 'option3': option3}
        return render(request, 'teacher/teacher_quiz_modify.html', context)


def my_quiz(request):
    course_list = Course.objects.filter(author=request.user)
    total_lecture_list = []
    total_final_quiz_list = []
    for course in course_list:
        lecture_list = Lecture.objects.filter(course=course)
        total_lecture_list.append(lecture_list)
        final_quiz_list = course.finalquiz_set.all()
        total_final_quiz_list.append(final_quiz_list)

    context = {'total_lecture_list': total_lecture_list, 'total_final_quiz_list': total_final_quiz_list}
    return render(request, 'teacher/teacher_my_quiz.html', context)


def setting_profile(request):
    teacher = Teacher.objects.get(user=request.user)
    school_list = School.objects.all()
    context = {'teacher': teacher, 'school_list': school_list}

    if request.method == "POST":
        school_id = request.POST.get("select_school", None)
        school = School.objects.get(id=school_id)
        teacher.name = request.POST['name']
        teacher.school = school
        teacher.save()
        request.user.user_name = request.POST['name']
        request.user.save()

        return redirect('teacher:setting_profile')
    else:
        return render(request, 'teacher/teacher_setting_profile.html', context)


def setting_photo(request):
    if request.method == "POST":
        request.user.image = request.FILES.get('image')
        request.user.save()
        return redirect('teacher:setting_photo')
    else:
        return render(request, 'teacher/teacher_setting_photo.html')


def setting_account(request):
    if request.method == 'POST':
        request.user.email = request.POST.get("email")
        request.user.save()
        current_password = request.POST.get("current_password")
        if check_password(current_password, request.user.password):
            new_password = request.POST.get("password1")
            password_confirm = request.POST.get("password2")
            if new_password == password_confirm:
                request.user.set_password(new_password)
                request.user.save()
                auth_login(request, request.user)
        return redirect('teacher:setting_account')
    else:
        return render(request, 'teacher/teacher_setting_account.html')
