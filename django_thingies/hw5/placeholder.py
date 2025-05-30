from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def admin_registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'registration.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'registration.html', {'error': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return render(request, 'registration.html', {'error': 'Email already used'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.save()

        return redirect('login')
    return render(request, 'registration.html')
