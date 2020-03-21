from django.urls import path

from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('borrow/<int:book_id>/', views.borrow, name='borrow'),
    path('return/<int:loan_id>/', views.give_back, name='give_back'),
    path('lookup/<str:isbn>/', views.lookup, name='lookup'),
    path('late/', views.late_loans, name='late_loans'),
]
