from django import forms


class AddBookmarkForm(forms.Form):
    url = forms.URLField(max_length=2048)


class SearchBookmarksForm(forms.Form):
    q = forms.CharField(max_length=1024)
