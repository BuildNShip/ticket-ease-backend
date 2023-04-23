from django.urls import path

from . import views

urlpatterns = [
    path('get-questions/', views.CollectFormDataAPI.as_view()),
    path('collect-data/', views.CollectFormDataAPI.as_view()),
    path('generate-ticket/', views.TicketGeneration.as_view()),
    path('mark-attendance/', views.AttendanceAPI.as_view()),
    path('list-attendance/', views.AttendanceAPI.as_view()),

]
