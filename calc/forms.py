from django import forms
from .models import Player, Team, Creator

class CreatorForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = ['name', 'num_bowlers', 'num_batsmen']

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'num_bowlers', 'num_batsmen', 'num_allrounders']

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = [
            'name', 'age', 'gender', 'role', 
            'wickets_taken', 'matches_played', 
            'batting_high_score', 'total_runs',
            'strike_rate', 'fifties', 'hundreds', 
            'economy_rate'
        ]
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            'role': forms.Select(choices=[('Batsman', 'Batsman'), ('Bowler', 'Bowler'), ('All-Rounder', 'All-Rounder')])
        }

