from django.db import models
from __future__ import annotations


class Team(models.Model):
    name: str = models.CharField(max_length=100, unique=True)
    slug: str = models.SlugField(max_length=100, unique=True)
    hltv_id: int = models.PositiveIntegerField(unique=True)
    team_url: str = models.URLField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class DailyStats(models.Model):
    team: Team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='daily_stats')
    parse_date: str = models.DateField()
    rank: int = models.PositiveSmallIntegerField()
    maps_played: int = models.PositiveIntegerField()
    kd_diff: str = models.CharField(max_length=20)
    kd_ratio: float = models.DecimalField(max_digits=4, decimal_places=2)
    rating: float = models.DecimalField(max_digits=4, decimal_places=2)
    win_rate_last_3m: float | None = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.team.name} — {self.parse_date} (#{self.rank})"


class MapStats(models.Model):
    daily_stats: DailyStats = models.ForeignKey(DailyStats, on_delete=models.CASCADE, related_name='map_stats')
    map_name: str = models.CharField(max_length=50)
    win_rate: float = models.DecimalField(max_digits=5, decimal_places=2)
    wins: int = models.PositiveSmallIntegerField(default=0)
    losses: int = models.PositiveSmallIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.map_name} — {self.win_rate}%"