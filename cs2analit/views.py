from django.shortcuts import render, get_object_or_404
from django.db.models import Max
from .models import Team, DailyStats,MapStats

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

        map_stats_team1 = stat1.map_stats.all().order_by('-win_rate')
        map_stats_team2 = stat2.map_stats.all().order_by('-win_rate')


        if stat1 and stat2:
            context.update({
                'team1': stat1,
                'team2': stat2,
                'recent_matches_team1': map_stats_team1,
                'recent_matches_team2': map_stats_team2,
                'teams_to_display': [stat1, stat2],
                'show_analysis': True,
            })
        else:
            context['error'] = "Нет свежих данных для одной из команд"
    elif team1_name or team2_name:
        context['error'] = "Выберите обе команды"

    return render(request, 'index.html', context)