import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
df = pd.read_csv("dataset.csv")

# Features
X = df[[
    "pages_visited",
    "session_duration",
    "avg_time_per_page",
    "pages_per_min"
]]

# Labels
y = df["label"]
print(df["label"].value_counts())
# Split data (IMPORTANT: added random_state + stratify)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model (improved version)
model = XGBClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Accuracy
acc = accuracy_score(y_test, y_pred)
print("Model Accuracy:", acc)

# Save model
joblib.dump(model, "model.pkl")

print("Model saved as model.pkl")