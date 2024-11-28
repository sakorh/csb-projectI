from django.urls import path

from .views import homePageView, transferView, loginView, logoutView, registrationView

app_name = 'bankapp'
urlpatterns = [
    path('/<username>/', homePageView, name='home'),
    path('login/', loginView, name='login'),
    path('login/login/', loginView),
    path('/<username>/logout/', logoutView, name='logout'),
    path('/<username>/transfer/', transferView, name='transfer'),
    path('login/register/', registrationView, name='register'),
    path('login/register/add_user/', registrationView)
]