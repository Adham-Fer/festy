from django import forms
from .models import Evenement, ImageEvenement
from django.forms import inlineformset_factory

class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['nom', 'date', 'description', 'capacite']


ImageEvenementFormSet = inlineformset_factory(
    Evenement, ImageEvenement,
    fields=('image', 'legende', 'est_principale'),
    extra=1, can_delete=True
)
