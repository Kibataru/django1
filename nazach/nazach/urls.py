from django.contrib import admin
from django.urls import path
from main import views
from django.contrib.auth import views as auth_views
from main.views import UserCreateView, UserListView, UserDetailView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.register, name='register'),  #Регистр главная
    path('login/', views.login, name='login'),  #Логин
    path('logout/', views.logout, name='logout'), #Выход
    path('accounts/profile/', views.get_name, name='get_name'), #Задния + меню
    path('success/', views.success_page, name='success_page'), #Имя получено 3 задание
    path('stranger/', views.stranger_page, name='stranger_page'), #Имя не получено 3 задание
    path('post/', views.post, name='simple_post'), #2 задание
    path('index/', views.index_endpoint, name='mainpage'), #2 задание
    path('data/', views.data_endpoint, name='data'), #2 задание

    path('users/create/', UserCreateView.as_view(), name='user-create'),  # crud 5 task, созданеи
    path('users/', UserListView.as_view(), name='user-list'),  # Список пользователей
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),  # Просмотр пользователя
    path('users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update'),  # Обновление
    path('users/<int:pk>/delete/', UserDeleteView.as_view(), name='user-delete'),  # Удаление

    #Сброс пароля
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'), 
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #Сброс акка
    path('account_recovery/', views.account_recovery, name='account_recovery'),
    path('recover/<uidb64>/<token>/', views.recover_account, name='recover_account'),
    path('account_recovery/done/', views.account_recovery_done, name='account_recovery_done'),
    
    #Профиль, редакт и делит
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('account/delete/', views.delete_account, name='delete_account'),
]