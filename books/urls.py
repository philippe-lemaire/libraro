from django.urls import path
from . import views

app_name = "books"

urlpatterns = [
    path("", views.BooksIndexView.as_view(), name="index"),
    path("ajouter", views.add_a_book, name="add_a_book"),
]
