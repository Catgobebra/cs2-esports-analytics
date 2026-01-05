from django.shortcuts import render, get_object_or_404
from django.db.models import Max
from .models import Team, DailyStats
import json

def index(request):
    team1_name = request.GET.get('team1')
    team2_name = request.GET.get('team2')

    all_teams = Team.objects.all().order_by('name')
    latest_date = DailyStats.objects.aggregate(max_date=Max('parse_date'))['max_date']

    context = {
        'all_teams': all_teams,
        'latest_date': latest_date or 'Нет данных',
    }

    if team1_name and team2_name and team1_name != team2_name:
        team1 = get_object_or_404(Team, name=team1_name)
        team2 = get_object_or_404(Team, name=team2_name)

        stat1 = DailyStats.objects.filter(team=team1, parse_date=latest_date).first()
        stat2 = DailyStats.objects.filter(team=team2, parse_date=latest_date).first()

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

    elif team1_name or team2_name:
        context['error'] = "Выберите обе команды"

    return render(request, 'index.html', context)