from django.shortcuts import render, redirect
from .models import *
from school.models import *
from teacher.models import *
from superadmin.models import *
from account.forms import UserChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.hashers import check_password


def signup_info(request):
    if request.method == 'POST':
        school_id = request.POST.get("select_school", None)
        school = School.objects.get(id=school_id)

        new_student = Student.objects.create(
            user=request.user,
            name=request.POST['name'],
            school=school
        )
        request.user.is_info_set = True
        request.user.user_name = request.POST['name']
        request.user.save()

        return redirect('student:dash')
    else:
        school_list = School.objects.all()
        context = {'school_list': school_list}
        return render(request, 'student/student_signup_info.html', context)


def dash(request):
    student = Student.objects.get(user=request.user)
    enroll_class_num = Enroll.objects.filter(student=student).filter(is_assigned=True).count()
    context = {'enroll_class_num': enroll_class_num}
    return render(request, 'student/student_dash.html', context)


def class_select(request):
    school = Student.objects.get(user=request.user).school
    class_list = Class.objects.filter(school=school)
    context = {'class_list': class_list}
    return render(request, 'student/student_class_select.html', context)


def class_signup(request, class_id):
    class_class = Class.objects.get(id=class_id)
    teacher = class_class.teacher
    student = Student.objects.get(user=request.user)
    try:
        _id = Enroll.objects.filter(class_class=class_class).get(student=student)
    except:
        _id = None
    if _id is None:
        new_enroll = Enroll.objects.create(
            class_class=class_class,
            teacher=teacher,
            student=student
        )
        return redirect('student:dash')
    else:
        return redirect('student:dash')


def my_class(request):
    student = Student.objects.get(user=request.user)
    enroll_list = Enroll.objects.filter(student=student).filter(is_assigned=True)

    for enroll in enroll_list:
        flag = 0
        lecture_pass_list = LecturePass.objects.filter(enroll=enroll)
        final_quiz_pass_list = FinalQuizPass.objects.filter(enroll=enroll)
        for lecture_pass in lecture_pass_list:
            if not lecture_pass.is_passed:
                flag = 1
                break
        for final_quiz_pass in final_quiz_pass_list:
            if not final_quiz_pass.is_passed:
                flag = 1
                break
        if flag == 0:
            enroll.is_graduated = True
            enroll.save()

    context = {'enroll_list': enroll_list}
    return render(request, 'student/student_my_class.html', context)


def take_class(request, course_id, enroll_id):
    course = Course.objects.get(id=course_id)
    enroll = Enroll.objects.get(id=enroll_id)
    lecture_list = course.lecture_set.all()
    final_quiz_list = course.finalquiz_set.all()
    lecture_pass_list = LecturePass.objects.filter(enroll=enroll)
    final_quiz_pass_list = FinalQuizPass.objects.filter(enroll=enroll)
    student = Student.objects.get(user=request.user)
    enroll_list = Enroll.objects.filter(student=student).filter(is_assigned=True)

    for enroll in enroll_list:
        flag = 0
        lecture_pass_list = LecturePass.objects.filter(enroll=enroll)
        final_quiz_pass_list = FinalQuizPass.objects.filter(enroll=enroll)
        for lecture_pass in lecture_pass_list:
            if not lecture_pass.is_passed:
                flag = 1
                break
        for final_quiz_pass in final_quiz_pass_list:
            if not final_quiz_pass.is_passed:
                flag = 1
                break
        if flag == 0:
            enroll.is_graduated = True
            enroll.save()

    context = {
        'lecture_list': lecture_list,
        'final_quiz_list': final_quiz_list,
        'course': course,
        'enroll': enroll,
        'lecture_pass_list': lecture_pass_list,
        'final_quiz_pass_list': final_quiz_pass_list
    }
    return render(request, 'student/student_take_class.html', context)


def take_lecture(request, lecture_id, enroll_id):
    lecture = Lecture.objects.get(id=lecture_id)
    enroll = Enroll.objects.get(id=enroll_id)
    context = {'lecture': lecture, 'enroll': enroll}
    return render(request, 'student/student_take_lecture.html', context)


def take_lecture_code(request, lecture_id, enroll_id):
    lecture = Lecture.objects.get(id=lecture_id)
    enroll = Enroll.objects.get(id=enroll_id)
    context = {'lecture': lecture, 'enroll': enroll}
    return render(request, 'student/student_take_lecture_code.html', context)


def take_quiz(request, quiz_id, enroll_id):
    quiz = Quiz.objects.get(id=quiz_id)
    enroll = Enroll.objects.get(id=enroll_id)
    lecture = quiz.lecture
    course = lecture.course
    lecture_pass = LecturePass.objects.filter(enroll=enroll).get(lecture=lecture)
    question_list = Question.objects.filter(quiz=quiz)
    option_list = []
    for question in question_list:
        temp = Option.objects.filter(question=question)
        option_list.append(temp)

    if request.method == 'POST':
        answer_list = request.POST.getlist('answers[]')
        pass_score = quiz.pass_score / 100
        total = 0
        correct = 0
        for question in question_list:
            total += 1
            flag = 0
            option_set = question.option_set.all()
            for option in option_set:
                if option.is_answer:
                    for answer in answer_list:
                        answer_option = Option.objects.get(id=answer)
                        if answer_option == option:
                            break
                    else:
                        flag = 1
                else:
                    for answer in answer_list:
                        answer_option = Option.objects.get(id=answer)
                        if answer_option == option:
                            flag = 1
                            break
                if flag:
                    break
            if flag == 0:
                correct += 1

        if correct/total > pass_score:
            lecture_pass.is_passed = True
            lecture_pass.score = correct/total * 100
            lecture_pass.save()
            return redirect('student:take_class', course.id, enroll.id)
        else:
            return redirect('student:take_class', course.id, enroll.id)

    else:
        context = {'quiz': quiz, 'course': course, 'question_list': question_list, 'option_list': option_list}
        return render(request, 'student/student_take_quiz.html', context)


def take_final_quiz(request, final_quiz_id, enroll_id):
    final_quiz = FinalQuiz.objects.get(id=final_quiz_id)
    enroll = Enroll.objects.get(id=enroll_id)
    course = final_quiz.course
    final_quiz_pass = FinalQuizPass.objects.filter(enroll=enroll).get(final_quiz=final_quiz)
    final_question_list = FinalQuestion.objects.filter(final_quiz=final_quiz)
    final_option_list = []
    for final_question in final_question_list:
        temp = FinalOption.objects.filter(final_question=final_question)
        final_option_list.append(temp)

    if request.method == 'POST':
        answer_list = request.POST.getlist('answers[]')
        pass_score = final_quiz.pass_score / 100
        total = 0
        correct = 0
        for final_question in final_question_list:
            total += 1
            flag = 0
            option_set = final_question.finaloption_set.all()
            for option in option_set:
                if option.is_answer:
                    for answer in answer_list:
                        answer_option = FinalOption.objects.get(id=answer)
                        if answer_option == option:
                            break
                    else:
                        flag = 1
                else:
                    for answer in answer_list:
                        answer_option = FinalOption.objects.get(id=answer)
                        if answer_option == option:
                            flag = 1
                            break
                if flag:
                    break
            if flag == 0:
                correct += 1

        if correct/total > pass_score:
            final_quiz_pass.is_passed = True
            final_quiz_pass.score = correct/total * 100
            final_quiz_pass.save()
            return redirect('student:take_class', course.id, enroll.id)
        else:
            return redirect('student:take_class', course.id, enroll.id)

    else:
        context = {
            'final_quiz': final_quiz,
            'course': course,
            'final_question_list': final_question_list,
            'final_option_list': final_option_list
        }
        return render(request, 'student/student_take_final_quiz.html', context)


def my_quiz(request):
    student = Student.objects.get(user=request.user)
    enroll_list = Enroll.objects.filter(student=student).filter(is_assigned=True)
    course_list = []
    lecture_pass_list = []
    final_quiz_pass_list = []

    for enroll in enroll_list:
        course_list.append(enroll.class_class.course)
        temp_list = LecturePass.objects.filter(enroll=enroll)
        temp_list_2 = FinalQuizPass.objects.filter(enroll=enroll)
        for temp in temp_list:
            lecture_pass_list.append(temp)
        for temp2 in temp_list_2:
            final_quiz_pass_list.append(temp2)

    total_lecture_list = []
    total_final_quiz_list = []
    for course in course_list:
        lecture_list = Lecture.objects.filter(course=course)
        total_lecture_list.append(lecture_list)
        final_quiz_list = course.finalquiz_set.all()
        total_final_quiz_list.append(final_quiz_list)

    context = {
        'total_lecture_list': total_lecture_list,
        'total_final_quiz_list': total_final_quiz_list,
        'lecture_pass_list': lecture_pass_list,
        'final_quiz_pass_list': final_quiz_pass_list
    }
    return render(request, 'student/student_my_quiz.html', context)


def setting_profile(request):
    student = Student.objects.get(user=request.user)
    school_list = School.objects.all()
    context = {'student': student, 'school_list': school_list}

    if request.method == "POST":
        school_id = request.POST.get("select_school", None)
        school = School.objects.get(id=school_id)
        student.name = request.POST['name']
        student.school = school
        student.save()
        request.user.user_name = request.POST['name']
        request.user.save()

        return redirect('student:setting_profile')
    else:
        return render(request, 'student/student_setting_profile.html', context)


def setting_photo(request):
    if request.method == "POST":
        request.user.image = request.FILES.get('image')
        request.user.save()
        return redirect('student:setting_photo')
    else:
        return render(request, 'student/student_setting_photo.html')


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
        return redirect('student:setting_account')
    else:
        return render(request, 'student/student_setting_account.html')
