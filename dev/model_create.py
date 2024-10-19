import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

# Load the dataset
df = pd.read_csv('code_quality.csv')

# Define features and labels
features = [
    'lines_of_code', 'cyclomatic_complexity', 'num_functions_methods', 
    'depth_of_inheritance', 'naming_conventions', 'code_formatting', 'comment_density'
]
X = df[features]
y = df['quality']

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train the model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Save the model and scaler
joblib.dump(rf, 'model.pkl')
joblib.dump(scaler, 'scaler.pkl')
