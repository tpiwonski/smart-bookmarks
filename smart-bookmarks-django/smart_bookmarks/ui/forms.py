from django import forms


class AddBookmarkForm(forms.Form):
    url = forms.URLField(max_length=2048)


class SearchBookmarksForm(forms.Form):
    q = forms.CharField(max_length=1024)
    op = forms.ChoiceField(choices=[('AND', 'AND'), ('OR', 'OR')], widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['op'] = 'AND'
