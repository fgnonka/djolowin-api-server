from django import forms

from .models import PlayerCard

class CardForm(forms.ModelForm):
    value = forms.DecimalField(decimal_places=2, max_digits=10, min_value=1000)
    for_sale = forms.BooleanField(required=False)
    
    class Meta:
        model = PlayerCard
        fields = ["value", "for_sale"]
