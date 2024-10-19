from flask import Flask, request, render_template, redirect, url_for
import joblib
import pandas as pd
from code_analyzer import CodeAnalyzer  # Import the code analyzer class

app = Flask(__name__)

# Load the model and scaler
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        code = request.form['code']

        # Analyze the code
        analyzer = CodeAnalyzer(code)
        metrics = analyzer.analyze()

        # Prepare features for the model
        data = pd.DataFrame([metrics])
        data_scaled = scaler.transform(data)

        # Predict code quality
        prediction = model.predict(data_scaled)[0]
        quality = "Good" if prediction == 1 else "Bad"

        return render_template('index.html', code=code, metrics=metrics, quality=quality)

    return render_template('index.html', code='', metrics=None, quality=None)

if __name__ == '__main__':
    app.run(debug=True)
