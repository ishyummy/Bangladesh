from django.shortcuts import render, redirect
from .models import *
from school.models import *
from teacher.models import *
from student.models import *


def dash(request):
    schools = School.objects.count()
    students = Student.objects.count()
    teachers = Teacher.objects.count()
    courses = Course.objects.count()
    lectures = Lecture.objects.count()
    quizzes = Quiz.objects.count() + FinalQuiz.objects.count()
    total_enroll = Enroll.objects.filter(is_assigned=True).count()
    graduate_enroll = Enroll.objects.filter(is_graduated=True).count()

    try:
        graduate_rate = graduate_enroll/total_enroll * 100
    except:
        graduate_rate = 0

    context = {'schools': schools,
               'students': students,
               'teachers': teachers,
               'courses': courses,
               'lectures': lectures,
               'quizzes': quizzes,
               'graduate_rate': graduate_rate
               }
    return render(request, 'admin/admin_dash.html', context)


def course_list(request):
    Course_list = Course.objects.all()
    context = {'Course_list': Course_list}
    return render(request, 'admin/admin_course_list.html', context)


def my_course_list(request):
    Course_list = Course.objects.filter(author=request.user)
    context = {'Course_list': Course_list}
    return render(request, 'admin/admin_course_list_mine.html', context)


def course_upload(request):
    if request.method == "POST":
        level = request.POST.get("level", None)
        category = request.POST.get("category", None)
        difficulty = request.POST.get("difficulty", None)

        new_course = Course.objects.create(
            author=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            price=request.POST['price'],
            level=level,
            category=category,
            difficulty=difficulty,
            tag=request.POST.get('tag_radio'),
            type=request.POST.get('type_radio'),
        )
        return redirect('superadmin:lecture_quiz_upload', new_course.id)
    else:
        return render(request, 'admin/admin_course_upload.html')


def lecture_quiz_upload(request, course_id):
    course = Course.objects.get(id=course_id)
    if course.author != request.user:
        print('here')
        return redirect('/')

    lecture_list = course.lecture_set.all()
    final_quiz_list = course.finalquiz_set.all()
    context = {'lecture_list': lecture_list, 'final_quiz_list': final_quiz_list, 'course': course}
    return render(request, 'admin/admin_lecture_quiz_upload.html', context)


def school_list(request):
    schools = School.objects.all()
    context = {'schools': schools}
    return render(request, 'admin/admin_school_list.html', context)


def teacher_list(request):
    teacher_list = Teacher.objects.all()
    context = {'teacher_list': teacher_list}
    return render(request, 'admin/admin_teacher_list.html', context)


def student_list(request):
    student_list = Student.objects.all()
    context = {'student_list': student_list}
    return render(request, 'admin/admin_student_list.html', context)


def quiz_list(request):
    course_list = Course.objects.all()
    total_lecture_list = []
    total_final_quiz_list = []
    for course in course_list:
        lecture_list = Lecture.objects.filter(course=course)
        total_lecture_list.append(lecture_list)
        final_quiz_list = course.finalquiz_set.all()
        total_final_quiz_list.append(final_quiz_list)

    context = {'total_lecture_list': total_lecture_list, 'total_final_quiz_list': total_final_quiz_list}
    return render(request, 'admin/admin_quiz_list.html', context)


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

        return redirect('superadmin:lecture_quiz_upload', course.id)
    else:
        context = {'course': course}
        return render(request, 'admin/admin_course_modify.html', context)


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
        return redirect('superadmin:add_quiz', new_lecture.id)
    else:
        return render(request, 'admin/admin_add_lecture.html')


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
        return redirect('superadmin:lecture_quiz_upload', course.id)
    else:
        return render(request, 'admin/admin_add_quiz.html')


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
        return redirect('superadmin:lecture_quiz_upload', course.id)
    else:
        return render(request, 'admin/admin_add_quiz.html')


def lecture_modify(request, lecture_id):
    lecture = Lecture.objects.get(id=lecture_id)
    if request.method == "POST":
        lecture.title = request.POST['title']
        lecture.video_link = request.POST['video_link']
        lecture.code = request.POST['code']
        lecture.file = request.FILES.get('file')
        lecture.save()
        return redirect('superadmin:lecture_quiz_upload', lecture.course.id)
    else:
        context = {'lecture': lecture}
        return render(request, 'admin/admin_lecture_modify.html', context)


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

        return redirect('superadmin:lecture_quiz_upload', quiz.lecture.course.id)
    else:
        context = {'quiz': quiz, 'question': question, 'option1': option1, 'option2': option2, 'option3': option3}
        return render(request, 'admin/admin_quiz_modify.html', context)


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
        return redirect('superadmin:lecture_quiz_upload', final_quiz.course.id)
    else:
        context = {'quiz': final_quiz, 'question': final_question, 'option1': option1, 'option2': option2, 'option3': option3}
        return render(request, 'admin/admin_quiz_modify.html', context)
