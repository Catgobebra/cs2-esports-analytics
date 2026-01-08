import json
from django.shortcuts import render
from django.db.models import Max

from .models import Team, DailyStats
from .forms import TeamComparisonForm
from cs2analit.ml.predictor import predict_win_probability

from typing import Optional
from datetime import date


def get_latest_date() -> Optional[date]:
    return DailyStats.objects.aggregate(max_date=Max('parse_date'))['max_date']


def get_rating_history(team) -> tuple[str, str]:
    history = DailyStats.objects.filter(team=team).order_by('parse_date').values('parse_date', 'rating')
    dates = [item['parse_date'].strftime('%Y-%m-%d') for item in history]
    values = [float(item['rating']) for item in history]
    return json.dumps(dates), json.dumps(values)


def get_map_comparison_data(stat1, stat2) -> tuple[str, str, str]:
    map_stats1 = stat1.map_stats.all().order_by('map_name')
    map_stats2 = stat2.map_stats.all().order_by('map_name')

    all_maps = sorted(set(ms.map_name for ms in map_stats1) | set(ms.map_name for ms in map_stats2))

    team1_winrates = []
    team2_winrates = []
    for map_name in all_maps:
        ms1 = next((ms for ms in map_stats1 if ms.map_name == map_name), None)
        ms2 = next((ms for ms in map_stats2 if ms.map_name == map_name), None)
        team1_winrates.append(float(ms1.win_rate) if ms1 else 0.0)
        team2_winrates.append(float(ms2.win_rate) if ms2 else 0.0)

    return json.dumps(all_maps), json.dumps(team1_winrates), json.dumps(team2_winrates)


def index(request):
    all_teams = Team.objects.all().order_by('name')
    latest_date = get_latest_date()

    form = TeamComparisonForm(request.GET or None)

    context = {
        'all_teams': all_teams,
        'latest_date': latest_date or 'Нет данных',
        'form': form,
        'show_analysis': False,
    }

    if request.GET and form.is_valid():
        team1 = form.cleaned_data['team1']
        team2 = form.cleaned_data['team2']

        stat1 = DailyStats.objects.filter(team=team1, parse_date=latest_date).first()
        stat2 = DailyStats.objects.filter(team=team2, parse_date=latest_date).first()

        if not (stat1 and stat2):
            context['error'] = "Нет свежих данных для одной или обеих команд."
        else:
            win_prob_team1, win_prob_team2 = predict_win_probability(stat1, stat2)

            rating_dates1, rating_values1 = get_rating_history(team1)
            rating_dates2, rating_values2 = get_rating_history(team2)
            maps_labels, team1_winrates, team2_winrates = get_map_comparison_data(stat1, stat2)

            context.update({
                'team1': stat1,
                'team2': stat2,
                'teams_to_display': [stat1, stat2],

                'win_prob_team1': win_prob_team1,
                'win_prob_team2': win_prob_team2,

                'recent_matches_team1': stat1.map_stats.all().order_by('map_name'),
                'recent_matches_team2': stat2.map_stats.all().order_by('map_name'),

                'rating_dates1': rating_dates1,
                'rating_values1': rating_values1,
                'rating_dates2': rating_dates2,
                'rating_values2': rating_values2,

                'maps_comparison_labels': maps_labels,
                'team1_winrates': team1_winrates,
                'team2_winrates': team2_winrates,

                'team1_name': team1.name,
                'team2_name': team2.name,

                'show_analysis': True,
            })
    elif request.GET:
        context['error'] = "Выберите две разные команды и корректно заполните форму."

    template = 'content_partial.html' if request.headers.get('HX-Request') else 'index.html'
    return render(request, template, context)