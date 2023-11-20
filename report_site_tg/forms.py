from django import forms
from .models import Order


class ReportSiteForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('count_reports', 'url_report', 'count_threads', 'proxy')
        widgets = {
            'count_reports': forms.TextInput(attrs={'placeholder': "Количество репортов"}),
            'url_report': forms.TextInput(attrs={'placeholder': "Кого репортим"}),
            'count_threads': forms.TextInput(attrs={'placeholder': "Количество потоков"}),
            'proxy': forms.TextInput(attrs={'placeholder': "Прокси"})
        }


class TextAddForm(forms.Form):
    new_text = forms.CharField(widget=forms.Textarea(attrs={'id': 'newText'}))
