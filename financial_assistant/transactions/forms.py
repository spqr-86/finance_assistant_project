from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'date',
            'description',
            'category',
            'type',
            'amount',
            'currency',
            'tags',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        } 