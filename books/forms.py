from django import forms
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Book


class IsbnForm(forms.Form):
    isbn = forms.CharField(max_length=17, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse("books:add_a_book")
        self.helper.form_method = "post"

        self.helper.add_input(
            Submit(
                "submit",
                "Ajouter le livre",
                css_class="mt-3 mb-3 btn-warning",
            )
        )


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ["id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse("books:manually_add_a_book")
        self.helper.form_method = "post"

        self.helper.add_input(
            Submit(
                "submit",
                "Ajouter le livre",
                css_class="mt-3 mb-3 btn-warning",
            )
        )
