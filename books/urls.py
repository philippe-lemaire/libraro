from django.urls import path
from . import views

app_name = "books"

urlpatterns = [
    path("", views.BooksIndexView.as_view(), name="index"),
    path("ajouter", views.add_a_book, name="add_a_book"),
    path("ajouter-a-la-main", views.manually_add_a_book, name="manually_add_a_book"),
    path("livre/<int:pk>/", views.BooksDetailView.as_view(), name="book_detail"),
]
