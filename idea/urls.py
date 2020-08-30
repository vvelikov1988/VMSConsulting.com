from django.urls import path
from .views import index, idea_detail, add_idea, delete, edit

app_name = 'idea'

urlpatterns = [
    path('', index, name='home'),
    path('add/', add_idea, name='add'),
    path('<int:pk>/', idea_detail, name='detail'),
    path('<int:pk>/edit/', edit, name='edit'),
    path('<int:pk>/delete/', delete, name='delete'),
]
