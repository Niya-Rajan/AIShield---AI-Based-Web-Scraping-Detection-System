import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

# ---------------- LOAD DATASET ----------------
df = pd.read_csv("data/dataset.csv")
# ---------------- FEATURES ----------------
X = df[[
    "pages_visited",
    "session_duration",
    "avg_time_per_page",
    "pages_per_min"
]]

# ---------------- LABELS ----------------
y = df["label"]

print("Label Distribution:")
print(df["label"].value_counts())

# ---------------- TRAIN-TEST SPLIT ----------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ---------------- MODEL TRAINING ----------------
model = XGBClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

# ---------------- PREDICTION ----------------
y_pred = model.predict(X_test)

# ---------------- EVALUATION ----------------
acc = accuracy_score(y_test, y_pred)
print("\nModel Accuracy:", acc)

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# ---------------- SAVE MODEL ----------------
joblib.dump(model, "model.pkl")
print("\nModel saved as model.pkl")