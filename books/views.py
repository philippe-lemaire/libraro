from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from .models import Book
from .forms import IsbnForm, BookForm
from isbnlib import *


# Create your views here.


class BooksIndexView(generic.ListView):
    model = Book


class BooksDetailView(generic.DetailView):
    model = Book


def add_a_book(request):
    form = IsbnForm(request.POST or None)
    context = {"form": form}
    template_name = "books/add_a_book.html"
    if request.method == "POST":
        if form.is_valid():
            isbn = form.cleaned_data["isbn"]
            if is_isbn10(isbn):
                isbn = to_isbn13(isbn)
            try:
                data = meta(isbn, service="wiki")
            except:
                data = meta(isbn)
            # make isbn-13 or whatever just isbn
            if "ISBN-13" in data:
                data["isbn"] = data["ISBN-13"]
                del data["ISBN-13"]
            # make keys lowercase
            data = {k.lower(): v for k, v in data.items()}
            print(data)
            if not data:
                messages.warning(request, "Livre non trouvé dans les bases ISBN.")
                return HttpResponseRedirect(reverse("books:add_a_book"))

            try:
                new_book = Book.objects.create(**data)
                messages.success(request, f"Livre {new_book.title} a été ajouté.")
            except IntegrityError:
                messages.warning(
                    request, f"Livre déjà présent dans la base de données."
                )
            return HttpResponseRedirect(reverse("books:add_a_book"))
    return render(request, template_name, context)


def manually_add_a_book(request):
    form = BookForm(request.POST or None)
    context = {"form": form}
    template_name = "books/manually_add_a_book.html"
    if request.method == "POST":
        if form.is_valid():
            new_book = form.save()
            messages.success(request, f"Livre {new_book.title} a été ajouté.")
            return HttpResponseRedirect(reverse("books:manually_add_a_book"))

    return render(request, template_name, context)
