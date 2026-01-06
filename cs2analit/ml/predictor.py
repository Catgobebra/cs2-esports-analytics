import joblib
import pandas as pd
from django.conf import settings
import os

MODEL_PATH = os.path.join(settings.BASE_DIR, 'cs2analit', 'ml', 'cs_match_predictor.pkl')
_model = joblib.load(MODEL_PATH)

FEATURE_COLUMNS = ['exp_diff', 'form_diff', 'h2h_team1']

def predict_win_probability(team1_stats, team2_stats):
    form1 = float(team1_stats.win_rate_last_3m or 50.0)
    form2 = float(team2_stats.win_rate_last_3m or 50.0)

    exp1 = team1_stats.maps_played or 0
    exp2 = team2_stats.maps_played or 0

    if form2 > form1 or (form2 == form1 and exp2 > exp1):
        team1_stats, team2_stats = team2_stats, team1_stats
        swapped = True
    else:
        swapped = False

    form_diff = (float(team1_stats.win_rate_last_3m or 50.0) - float(team2_stats.win_rate_last_3m or 50.0)) / 100.0
    exp_diff = (team1_stats.maps_played or 0) - (team2_stats.maps_played or 0)
    h2h_team1 = 0.5

    data = {
        'exp_diff': exp_diff,
        'form_diff': form_diff,
        'h2h_team1': h2h_team1,
    }

    features_df = pd.DataFrame([data])[FEATURE_COLUMNS]

    prob_stronger_win = _model.predict_proba(features_df)[0][1]

    if swapped:
        win_prob_original_team1 = round((1 - prob_stronger_win) * 100, 1)
        win_prob_original_team2 = round(prob_stronger_win * 100, 1)
    else:
        win_prob_original_team1 = round(prob_stronger_win * 100, 1)
        win_prob_original_team2 = round((1 - prob_stronger_win) * 100, 1)

    return win_prob_original_team1, win_prob_original_team2