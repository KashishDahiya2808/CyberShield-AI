
import streamlit as st
import joblib
import pandas as pd
from pathlib import Path
from feature_extraction import extract_features

st.set_page_config(
    page_title="CyberShield AI",
    page_icon="🛡️",
    layout="centered"
)

MODEL_PATH = Path(__file__).parent / "trained_model" / "phishing_model.pkl"


@st.cache_resource
def load_model():
    package = joblib.load(MODEL_PATH)

    if not isinstance(package, dict):
        raise ValueError(
            "Model format is different. Please check train_model.py."
        )

    return (
        package["model"],
        package["feature_columns"],
        package.get(
            "label_mapping",
            {0: "Phishing", 1: "Legitimate"}
        )
    )


st.title("🛡️ CyberShield AI")
st.subheader("AI-Powered Phishing URL Detector")
st.write("Enter a URL to check whether it may be phishing.")

try:
    model, feature_columns, label_mapping = load_model()
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

url = st.text_input(
    "Enter website URL",
    placeholder="https://example.com"
)

if st.button("🔍 Scan URL", type="primary"):
    if not url.strip():
        st.warning("Please enter a URL first.")
    else:
        try:
            features = extract_features(url.strip())

            if isinstance(features, pd.DataFrame):
                input_data = features
            else:
                input_data = pd.DataFrame([features])

            missing = set(feature_columns) - set(input_data.columns)

            if missing:
                st.error(
                    "Feature mismatch. Missing features: "
                    + ", ".join(sorted(missing))
                )
                st.stop()

            input_data = input_data[feature_columns]
            prediction = model.predict(input_data)[0]
            result = label_mapping.get(
                int(prediction), f"Unknown label: {prediction}"
            )

            if result.lower() == "phishing":
                st.error("⚠️ Potential phishing URL detected!")
            elif result.lower() == "legitimate":
                st.success("✅ Model classifies this URL as legitimate.")
            else:
                st.info(f"Prediction: {result}")

            st.caption(
                "This is an automated prediction, not a guarantee "
                "that the website is safe."
            )

        except Exception as e:
            st.error(f"Prediction failed: {e}")
