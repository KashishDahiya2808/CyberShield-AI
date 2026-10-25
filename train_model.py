
import os
import time
import joblib
import pandas as pd

from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from feature_extraction import extract_features

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "trained_model")
MODEL_PATH = os.path.join(OUTPUT_DIR, "phishing_model.pkl")


def main():
    start = time.time()

    print("=" * 50)
    print("CYBERSHIELD AI - URL MODEL TRAINING")
    print("=" * 50)

    print("\n[1/5] Loading dataset...")
    dataset = fetch_ucirepo(id=967)

    data = dataset.data.features
    targets = dataset.data.targets

    url_col = next(
        (c for c in data.columns if str(c).strip().lower() == "url"),
        None
    )

    if url_col is None:
        raise ValueError("Dataset does not contain a URL column.")

    if targets.shape[1] != 1:
        raise ValueError("Expected one target column.")

    urls = data[url_col].reset_index(drop=True)
    y = pd.to_numeric(
        targets.iloc[:, 0].reset_index(drop=True),
        errors="coerce"
    )

    valid = urls.notna() & y.notna()
    urls = urls[valid].reset_index(drop=True)
    y = y[valid].astype(int).reset_index(drop=True)

    if set(y.unique()) != {0, 1}:
        raise ValueError(f"Unexpected target labels: {sorted(y.unique())}")

    print(f"URLs to process: {len(urls)}")

    print("\n[2/5] Extracting URL features...")
    rows = []

    for i, url in enumerate(urls, start=1):
        rows.append(extract_features(str(url)))

        if i % 10000 == 0:
            print(f"Processed {i}/{len(urls)} URLs")

    X = pd.DataFrame(rows)
    feature_columns = list(X.columns)

    print("Feature count:", len(feature_columns))

    print("\n[3/5] Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("\n[4/5] Training Random Forest...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    print("\nTest accuracy:", round(accuracy_score(y_test, predictions), 4))
    print("\nClassification report:")
    print(classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Phishing", "Legitimate"],
        zero_division=0
    ))

    print("\n[5/5] Saving model...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    package = {
        "model": model,
        "feature_columns": feature_columns,
        "label_mapping": {
            0: "Phishing",
            1: "Legitimate"
        }
    }

    joblib.dump(package, MODEL_PATH)

    print("\nTraining completed successfully!")
    print("Saved to:", MODEL_PATH)
    print("Time taken:", round((time.time() - start) / 60, 2), "minutes")


if __name__ == "__main__":
    main()
