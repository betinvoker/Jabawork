from django import forms
 
class OpinionForm(forms.Form):
    text = forms.CharField(label="Отзыв", widget=forms.Textarea, required=False)
    date_opinion = forms.DateField(label="Дата отзыва")
    opinion = forms.ChoiceField(label="Мнение", choices=(("True", "Положительный отзыв"), ("False", "Отрицательный отзыв")), required=False)
    university = forms.IntegerField(min_value=1)