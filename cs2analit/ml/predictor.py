# cs2analit/ml/predictor.py
import joblib
import pandas as pd
from django.conf import settings
import os

MODEL_PATH = os.path.join(settings.BASE_DIR, 'cs2analit', 'ml', 'cs_match_predictor.pkl')

_model = joblib.load(MODEL_PATH)

FEATURE_COLUMNS = ['exp_diff', 'form_diff', 'h2h_team1']

def predict_win_probability(team1_stats, team2_stats):
    data = {
        'exp_diff': 0.0,
        'form_diff': 0.0,
        'h2h_team1': 0.5,
    }

    features_df = pd.DataFrame([data])[FEATURE_COLUMNS]

    prob_team1 = _model.predict_proba(features_df)[0][1]
    win_prob_team1 = round(prob_team1 * 100, 1)
    win_prob_team2 = round(100 - win_prob_team1, 1)

    return win_prob_team1, win_prob_team2