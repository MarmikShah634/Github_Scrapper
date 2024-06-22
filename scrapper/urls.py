from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signin/', views.signin, name='signin'),
    path('index/', views.index, name='index'),
    path('logout/', views.custom_logout, name='logout'),
    path('<path:path>', views.custom_page_not_found),
]

handler404 = 'scrapper.views.custom_page_not_found'