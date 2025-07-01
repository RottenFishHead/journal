from django.urls import path
from . import views

app_name = 'research'

urlpatterns = [
    path('', views.research_list, name='research_list'),
    path('create/', views.research_create, name='research_create'),
    path('<int:pk>/', views.research_detail, name='research_detail'),
    path('<int:pk>/edit/', views.research_edit, name='research_edit'),  
    path('<int:pk>/delete/', views.research_delete, name='research_delete'),

]