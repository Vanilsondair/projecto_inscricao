from django.urls import path
from django.contrib.auth import views as auth_views
from .views import excluir_cadeira
from . import views

urlpatterns = [
    path('', views.lista_cadeiras, name='lista_cadeiras'),
    path('login/',  auth_views.LoginView.as_view(), name='login'),
    path('logout/',  auth_views.LogoutView.as_view(), name='logout'),
    path('cadeiras_feitas/',  views.cadeiras_feitas, name='cadeiras'),
     path('excluir_cadeira/<int:inscricao_id>/', excluir_cadeira, name='excluir_cadeira'),
    # Outras rotas podem ser definidas aqui

  
]
