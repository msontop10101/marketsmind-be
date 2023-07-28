from django.urls import path
from . import views
from .views import GetDetailsView

urlpatterns = [
    path('news/', views.NewsView.as_view(), name='news'),
    path('get-details/', GetDetailsView.as_view()),
]
