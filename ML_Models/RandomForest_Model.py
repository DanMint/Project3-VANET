# RandomForest_Model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# === Load dataset ===
df = pd.read_csv("vanet_threat_dataset.csv")

# === Define features and label ===
y = df["threat_type"]
X = df.drop(columns=["threat_type", "timestamp", "vehicle_id"], errors="ignore")

# === Categorical vs Numeric ===
cat_cols = [c for c in X.columns if X[c].dtype == "object"]

# === Preprocessor (RF doesn’t need scaling) ===
pre = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
], remainder="passthrough")

# === Split ===
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

# === Model ===
model = Pipeline([
    ("pre", pre),
    ("clf", RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1))
])

# === Train and Evaluate ===
model.fit(Xtr, ytr)
yp = model.predict(Xte)
acc = accuracy_score(yte, yp)
print(f"Random Forest Accuracy: {acc * 100:.2f}%")
