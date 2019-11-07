from django import forms


class FlagForm(forms.Form):
    Flag = forms.CharField(label="你得到的Flag是",
                           max_length="50",

                           )
