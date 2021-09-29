from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.user.type == 'school':
            return redirect('school:dash')
        elif request.user.type == 'teacher':
            return redirect('teacher:dash')
        elif request.user.type == 'student':
            return redirect('student:dash')
        elif request.user.type == 'superadmin':
            return redirect('superadmin:dash')
        else:
            return render(request, 'home.html')
    else:
        return redirect('account:login')