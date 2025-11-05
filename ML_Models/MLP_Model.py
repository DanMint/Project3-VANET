# MLP_Model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

# === Load dataset ===
df = pd.read_csv("vanet_threat_dataset.csv")

# === Define features and label ===
y = df["threat_type"]
X = df.drop(columns=["threat_type", "timestamp", "vehicle_id"], errors="ignore")

# === Separate columns ===
cat_cols = [c for c in X.columns if X[c].dtype == "object"]
num_cols = [c for c in X.columns if c not in cat_cols]

# === Preprocessor ===
pre = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
])

# === Split ===
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

# === Model ===
model = Pipeline([
    ("pre", pre),
    ("clf", MLPClassifier(hidden_layer_sizes=(64, 32), activation="relu",
                          solver="adam", max_iter=500, random_state=42))
])

# === Train and Evaluate ===
model.fit(Xtr, ytr)
yp = model.predict(Xte)
acc = accuracy_score(yte, yp)
print(f"MLP Neural Network Accuracy: {acc * 100:.2f}%")
