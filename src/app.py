from flask import Flask, request, jsonify, render_template
from model_utils import predict_default_risk

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json() if request.is_json else request.form

        # Convert age (years) to DAYS_BIRTH (negative days, as in original dataset)
        age_years = float(data.get('age', 35))
        days_birth = -int(age_years * 365)

        # Convert years employed to DAYS_EMPLOYED (negative days)
        years_employed = float(data.get('years_employed', 5))
        days_employed = -int(years_employed * 365)

        user_input = {
            'EXT_SOURCE_1': float(data.get('ext_source_1')) if data.get('ext_source_1') else None,
            'EXT_SOURCE_2': float(data.get('ext_source_2')) if data.get('ext_source_2') else None,
            'EXT_SOURCE_3': float(data.get('ext_source_3')) if data.get('ext_source_3') else None,
            'AMT_CREDIT': float(data.get('amt_credit')),
            'AMT_ANNUITY': float(data.get('amt_annuity')),
            'AMT_INCOME_TOTAL': float(data.get('amt_income_total')),
            'AMT_GOODS_PRICE': float(data.get('amt_goods_price')),
            'DAYS_BIRTH': days_birth,
            'DAYS_EMPLOYED': days_employed,
            'CODE_GENDER': data.get('gender', 'M'),
            'NAME_EDUCATION_TYPE': data.get('education', 'Secondary / secondary special'),
            'NAME_FAMILY_STATUS': data.get('family_status', 'Married'),
            'FLAG_OWN_CAR': data.get('own_car', 'N'),
        }

        # Remove None values so defaults fill them in instead
        user_input = {k: v for k, v in user_input.items() if v is not None}

        probability = predict_default_risk(user_input)
        risk_level = "High Risk" if probability > 0.5 else "Low Risk"

        return jsonify({
            "default_probability": round(probability, 4),
            "risk_percentage": f"{probability*100:.2f}%",
            "risk_level": risk_level
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=False, host='0.0.0.0', port=port)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)