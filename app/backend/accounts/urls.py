from django.urls import path
from . import views

urlpatterns = [
    path('escolher-tipo/', views.escolher_tipo_de_usuario, name='escolher_tipo_de_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),
    path('dashboard-redirect/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard-professor/', views.dashboard_professor, name='dashboard_professor'),
    path('dashboard-aluno/', views.dashboard_aluno, name='dashboard_aluno'),
    path('login-admin/', views.login_admin, name='login_admin'),
    path('login-professor/', views.login_professor, name='login_professor'),
    path('login-aluno/', views.login_aluno, name='login_aluno'),
]
