from __future__ import annotations
import joblib
import pandas as pd
from django.conf import settings
import os

MODEL_PATH = os.path.join(settings.BASE_DIR, 'cs2analit', 'ml', 'cs_match_predictor.pkl')
_model = joblib.load(MODEL_PATH)

FEATURE_COLUMNS = ['exp_diff', 'form_diff', 'h2h_team1']


def predict_win_probability(team1_stats, team2_stats) -> tuple[float, float]:
    form1: float = float(team1_stats.win_rate_last_3m or 50.0)
    form2: float = float(team2_stats.win_rate_last_3m or 50.0)

    exp1: int = team1_stats.maps_played or 0
    exp2: int = team2_stats.maps_played or 0

    if form2 > form1 or (form2 == form1 and exp2 > exp1):
        team1_stats, team2_stats = team2_stats, team1_stats
        swapped: bool = True
    else:
        swapped: bool = False

    form_diff: float = (float(team1_stats.win_rate_last_3m or 50.0) - float(team2_stats.win_rate_last_3m or 50.0)) / 100.0
    exp_diff: int = (team1_stats.maps_played or 0) - (team2_stats.maps_played or 0)
    h2h_team1: float = 0.5

    data: dict = {
        'exp_diff': exp_diff,
        'form_diff': form_diff,
        'h2h_team1': h2h_team1,
    }

    features_df: pd.DataFrame = pd.DataFrame([data])[FEATURE_COLUMNS]

    prob_stronger_win: float = _model.predict_proba(features_df)[0][1]

    if swapped:
        return round((1 - prob_stronger_win) * 100, 1), round(prob_stronger_win * 100, 1)
    else:
        return round(prob_stronger_win * 100, 1), round((1 - prob_stronger_win) * 100, 1)
