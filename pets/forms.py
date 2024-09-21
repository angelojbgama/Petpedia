from django import forms

from core.models import PET

class PETForm(forms.ModelForm):
    class Meta:
        model = PET
        fields = ['nome', 'especie', 'idade', 'vacinado', 'vacinas', 'caracteristicas', 'foto', 'localidade', 'disponivel_adocao']
