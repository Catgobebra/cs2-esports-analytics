from django import forms
from .models import Team

class TeamComparisonForm(forms.Form):
    team1 = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-ghost input-lg grow bg-cardsdark',
            'placeholder': 'Выберите команду',
            'list': 'teams_list',
        })
    )
    team2 = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input-ghost input-lg grow bg-cardsdark',
            'placeholder': 'Выберите команду',
            'list': 'teams_list',
        })
    )

    def clean_team1(self):
        name = self.cleaned_data['team1']
        if not Team.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Команда не найдена")
        return Team.objects.get(name__iexact=name)

    def clean_team2(self):
        name = self.cleaned_data['team2']
        if not Team.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Команда не найдена")
        return Team.objects.get(name__iexact=name)

    def clean(self):
        cleaned_data = super().clean()
        team1 = cleaned_data.get('team1')
        team2 = cleaned_data.get('team2')
        if team1 and team2 and team1 == team2:
            raise forms.ValidationError("Выберите две разные команды")
        return cleaned_data