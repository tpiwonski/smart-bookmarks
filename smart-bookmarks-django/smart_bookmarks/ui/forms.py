from django import forms


class AddBookmarkForm(forms.Form):
    url = forms.URLField(max_length=2048)
