# XGBoost_Model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# === Load dataset ===
df = pd.read_csv("vanet_threat_dataset.csv")

# === Define features and label ===
y = df["threat_type"]
X = df.drop(columns=["threat_type", "timestamp", "vehicle_id"], errors="ignore")

# === Encode target variable for XGBoost (needs numeric labels) ===
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# === Separate numeric and categorical columns ===
cat_cols = [c for c in X.columns if X[c].dtype == "object"]
num_cols = [c for c in X.columns if c not in cat_cols]

# === Preprocessing ===
pre = ColumnTransformer([
    ("num", StandardScaler(), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
])

# === Train/Test Split ===
Xtr, Xte, ytr, yte = train_test_split(
    X, y_encoded, test_size=0.25, stratify=y_encoded, random_state=42
)

# === XGBoost Model ===
model = Pipeline([
    ("pre", pre),
    ("clf", XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.3,
        objective='multi:softprob',
        random_state=42,
        use_label_encoder=False,
        eval_metric='mlogloss'
    ))
])

# === Train and Evaluate ===
model.fit(Xtr, ytr)
yp = model.predict(Xte)
acc = accuracy_score(yte, yp)

print(f"XGBoost Model Accuracy: {acc * 100:.2f}%")

# === Optional: Display class predictions ===
# Convert predictions back to original labels
yp_labels = label_encoder.inverse_transform(yp)
yte_labels = label_encoder.inverse_transform(yte)

# === Optional: Feature Importance ===
# Get feature names after preprocessing
feature_names = []
if num_cols:
    feature_names.extend(num_cols)
if cat_cols:
    # Get one-hot encoded feature names
    cat_features = model.named_steps['pre'].transformers_[1][1].get_feature_names_out(cat_cols)
    feature_names.extend(cat_features)

# Get feature importance
importance = model.named_steps['clf'].feature_importances_

# Create importance dataframe
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': importance
}).sort_values('importance', ascending=False).head(10)

print("\nTop 10 Most Important Features:")
print(importance_df)
