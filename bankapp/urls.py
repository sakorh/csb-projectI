from django.urls import path

from .views import homePageView, transferView, loginView, logoutView, registrationView

app_name = 'bankapp'
urlpatterns = [
    path('', homePageView, name='home'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('transfer/', transferView, name='transfer'),
    path('register/', registrationView, name='register'),
    path('register/add_user/', registrationView)
]
