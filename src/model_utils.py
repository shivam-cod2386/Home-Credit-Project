import lightgbm as lgb
import pandas as pd
import numpy as np
import json

MODEL_PATH = '../models/final_lightgbm_model.txt'
DEFAULTS_PATH = '../models/feature_defaults.json'

model = lgb.Booster(model_file=MODEL_PATH)

with open(DEFAULTS_PATH, 'r') as f:
    defaults = json.load(f)

CAT_COLS = ['NAME_CONTRACT_TYPE', 'CODE_GENDER', 'FLAG_OWN_CAR', 'FLAG_OWN_REALTY',
            'NAME_TYPE_SUITE', 'NAME_INCOME_TYPE', 'NAME_EDUCATION_TYPE',
            'NAME_FAMILY_STATUS', 'NAME_HOUSING_TYPE', 'OCCUPATION_TYPE',
            'WEEKDAY_APPR_PROCESS_START', 'ORGANIZATION_TYPE', 'FONDKAPREMONT_MODE',
            'HOUSETYPE_MODE', 'WALLSMATERIAL_MODE', 'EMERGENCYSTATE_MODE']

def predict_default_risk(user_input: dict):
    full_input = defaults.copy()
    full_input.update(user_input)

    df = pd.DataFrame([full_input])

    expected_features = model.feature_name()

    # Reindex to match model's expected features exactly —
    # any column not present (naming mismatch, etc.) becomes NaN instead of erroring
    df = df.reindex(columns=expected_features)

    for col in CAT_COLS:
        if col in df.columns:
            df[col] = df[col].astype('category')

    prob = model.predict(df, num_threads=1)[0]
    return float(prob)