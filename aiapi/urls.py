# your_app_name/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('ai-analyst/', views.answer_question, name='answer'),
]
