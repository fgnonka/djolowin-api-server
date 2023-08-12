from django import forms

from .models import PlayerCard

class CardForm(forms.ModelForm):
    value = forms.DecimalField(decimal_places=2, max_digits=10)
    for_sale = forms.BooleanField(required=False)
    
    class Meta:
        model = PlayerCard
        fields = ["value", "for_sale"]

    def __init__(self, *args, **kwargs):
        self.playercard_instance = kwargs.pop("playercard_instance", None)
        super().__init__(*args, **kwargs)

        if self.playercard_instance:
            self.fields["value"].initial = self.playercard_instance.value
            self.fields["for_sale"].initial = self.playercard_instance.for_sale