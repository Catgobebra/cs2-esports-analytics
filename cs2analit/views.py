from django.shortcuts import render, get_object_or_404
from django.db.models import Max
from .models import Team, DailyStats
from .forms import TeamComparisonForm
from cs2analit.ml.predictor import predict_win_probability
import json

def index(request):
    all_teams = Team.objects.all().order_by('name')
    latest_date = DailyStats.objects.aggregate(max_date=Max('parse_date'))['max_date']

    form = TeamComparisonForm(request.GET or None)

    context = {
        'all_teams': all_teams,
        'latest_date': latest_date or 'Нет данных',
        'form': form,
        'show_analysis' : False
    }

    if request.GET and form.is_valid():
        team1 = form.cleaned_data['team1']
        team2 = form.cleaned_data['team2']

        stat1 = DailyStats.objects.filter(team=team1, parse_date=latest_date).first()
        stat2 = DailyStats.objects.filter(team=team2, parse_date=latest_date).first()

        win_prob_team1, win_prob_team2 = predict_win_probability(stat1, stat2)

        if stat1 and stat2:
            map_stats_team1 = stat1.map_stats.all().order_by('map_name')
            map_stats_team2 = stat2.map_stats.all().order_by('map_name')

            all_maps = set(ms.map_name for ms in map_stats_team1) | set(ms.map_name for ms in map_stats_team2)
            maps_sorted = sorted(all_maps)

            team1_winrates = [float(ms.win_rate) if ms else 0 for ms in [next((ms for ms in map_stats_team1 if ms.map_name == m), None) for m in maps_sorted]]
            team2_winrates = [float(ms.win_rate) if ms else 0 for ms in [next((ms for ms in map_stats_team2 if ms.map_name == m), None) for m in maps_sorted]]

            rating_history1 = DailyStats.objects.filter(team=team1).order_by('parse_date').values('parse_date', 'rating')
            rating_dates1 = [item['parse_date'].strftime('%Y-%m-%d') for item in rating_history1]
            rating_values1 = [float(item['rating']) for item in rating_history1]

            rating_history2 = DailyStats.objects.filter(team=team2).order_by('parse_date').values('parse_date', 'rating')
            rating_dates2 = [item['parse_date'].strftime('%Y-%m-%d') for item in rating_history2]
            rating_values2 = [float(item['rating']) for item in rating_history2]

            context.update({
               'team1': stat1,
                'team2': stat2,
                'teams_to_display': [stat1, stat2],

                'win_prob_team1': win_prob_team1,
                'win_prob_team2': win_prob_team2,

                'recent_matches_team1': map_stats_team1,
                'recent_matches_team2': map_stats_team2,

                'rating_dates1': json.dumps(rating_dates1),
                'rating_values1': json.dumps(rating_values1),

                'rating_dates2': json.dumps(rating_dates2),
                'rating_values2': json.dumps(rating_values2),

                'maps_comparison_labels': json.dumps(maps_sorted),
                'team1_winrates': json.dumps(team1_winrates),
                'team2_winrates': json.dumps(team2_winrates),
                'team1_name': team1.name,
                'team2_name': team2.name,

                'show_analysis': True
            })
        else:
            context['error'] = "Нет свежих данных"

    else:
        if request.GET:
            context['error'] = "Выберите две разные команды"

    if request.headers.get('HX-Request'):
        return render(request, 'content_partial.html', context)
    return render(request, 'index.html', context)