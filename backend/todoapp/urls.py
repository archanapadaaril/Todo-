from django.urls import path
from . import views 

urlpatterns=[
    path('',views.todo_list,name='todo_list'),
    path('todo_detail/<int:pk>',views.todo_detail,name='todo_detail'),
    
]