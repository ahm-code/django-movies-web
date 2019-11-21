from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('create/', views.create, name='create'), # this mean calling  myapp.com/create. it will run create function when visit that link
    path('edit/<str:movie_id>', views.edit, name='edit'), 
    path('delete/<str:movie_id>', views.delete, name='delete'), 
]
