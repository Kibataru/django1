import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from nazach.forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth.forms import SetPasswordForm

# ------------------------------ 22 -------------------------------------
def post(request):
    if request.method == 'POST':
        return HttpResponse('Форма отправлена!')
    return render(request, 'posttok.html')

def index_endpoint(request):
    user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")
    return HttpResponse(f"<p>User-Agent: {user_agent}</p>")

def data_endpoint(request):
    count = int(request.GET.get('count', 3))
    items = [
        f"Item {chr(random.randint(65, 90))} = {random.randint(10, 100)} {random.choice(['red', 'green', 'blue'])}"
        for _ in range(count)
    ]
    return HttpResponse("\n".join(items))

# ------------------------------ 333 ------------------------------------
def get_name(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            return redirect('success_page')
        else:
            return redirect('stranger_page')
    return render(request, 'main.html')

def success_page(request):
    return HttpResponse("Привет! Мы знаем Ваше имя")

def stranger_page(request):
    return HttpResponse("Привет! Мы не знаем Вашего имени")

# ------------------------------ 4444 -----------------------------------
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно! Теперь войдите в систему.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('get_name')
            else:
                messages.error(request, 'Неверное имя пользователя или пароль.')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('register')

# ------------------------------ 55555 ----------------------------------
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ------------------------------ 66666 ----------------------------------
def account_recovery(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Восстановление аккаунта"
                    message = render_to_string('account_recovery_email.html', {
                        'user': user,
                        'domain': 'http://192.168.0.2:8000/',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    })
                    send_mail(
                        subject,
                        message,
                        'barsikmoy17@gmail.com',
                        [email],
                        fail_silently=False,
                    )
                messages.success(request, 'Письмо с инструкциями отправлено на ваш email.')
                return redirect('account_recovery_done')
            else:
                messages.error(request, 'Пользователь с таким email не найден.')
        else:
            messages.error(request, 'Исправьте ошибки в форме.')
    else:
        form = PasswordResetForm()
    return render(request, 'account_recovery.html', {'form': form})

def recover_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Пароль успешно изменен. Теперь войдите в систему.')
                return redirect('login')
        else:
            form = SetPasswordForm(user)
        return render(request, 'recover_account.html', {'form': form})
    else:
        messages.error(request, 'Ссылка для восстановления недействительна.')
        return redirect('account_recovery')

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Пожалуйста, войдите в систему.')
        return redirect('login')
    return render(request, 'profile.html', {'user': request.user})

def edit_profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Пожалуйста, войдите в систему.')
        return redirect('login')
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

def delete_account(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Пожалуйста, войдите в систему.')
        return redirect('login')
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        messages.success(request, 'Ваш аккаунт успешно удален.')
        return redirect('register')
    return render(request, 'delete_account.html')

def account_recovery_done(request):
    return render(request, 'account_recovery_done.html')