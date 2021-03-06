from django import forms

from smart_bookmarks.search.services import OPERATOR_AND, OPERATOR_OR


class AddBookmarkForm(forms.Form):
    url = forms.URLField(max_length=2048)


class SearchBookmarksForm(forms.Form):
    q = forms.CharField(required=False, label="")
    op = forms.ChoiceField(
        choices=[(OPERATOR_AND, OPERATOR_AND), (OPERATOR_OR, OPERATOR_OR)],
        label="",
        widget=forms.RadioSelect,
    )

    def __init__(self, data=None, *args, **kwargs):
        values = {"op": OPERATOR_AND}
        if data:
            values.update({k: v for k, v in data.items()})

        super().__init__(values, *args, **kwargs)
        self.initial["op"] = OPERATOR_AND

    def clean_op(self):
        op = self.cleaned_data["op"]
        return op if op else OPERATOR_AND

    def get_query(self):
        return self.cleaned_data["q"]

    def get_operator(self):
        return self.cleaned_data["op"]
