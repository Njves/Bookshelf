from bookshelf.views import BookDetailView, BookCreateView, BookUpdateView
from django.template.defaulttags import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.books, name='main'),
    path('detail/<int:pk>/', BookDetailView.as_view(), name='detail'),
    path('create', BookCreateView.as_view(), name='create'),
    path('remove/<int:id>', views.remove_book, name='remove'),
    path('edit/<int:pk>', BookUpdateView.as_view(), name='edit'),
    path('login', views.user_login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('write_comment', views.write_comment, name='write_comment'),
]