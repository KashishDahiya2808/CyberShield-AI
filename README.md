
# 🛡️ CyberShield AI
### AI-Powered Phishing URL Detector

## 📌 About the Project
CyberShield AI is a machine-learning-based project designed to classify URLs as potentially phishing or legitimate.

It extracts URL-based features and uses a Random Forest classifier to make predictions through a simple Streamlit web interface.

## 🎯 Objectives
- Detect potentially suspicious URLs.
- Extract useful URL-based features.
- Apply machine learning for URL classification.
- Provide a simple, user-friendly interface.

## ✨ Features
- URL input and scanning.
- 14 URL-based features.
- Random Forest classification model.
- Streamlit web interface.
- Prediction results displayed to the user.

## 🛠️ Technologies Used
- Python
- Pandas
- Scikit-learn
- Streamlit
- Joblib
- UCI Machine Learning Repository dataset

## 📊 Model Training
- Dataset: PhiUSIIL Phishing URL Dataset
- URLs processed: 235,795
- Features: 14
- Algorithm: Random Forest Classifier
- Test accuracy: 99.53%

Note: Accuracy is based on the project's test split. Real-world performance may differ, and predictions should not be treated as a guarantee of website safety.

## 📂 Project Structure
```text
CyberShield-AI/
├── app.py
├── train_model.py
├── feature_extraction.py
├── trained_model/
│   └── phishing_model.pkl
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository
```bash
git clone <your-github-repository-url>
cd CyberShield-AI
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
```bash
pip install streamlit pandas scikit-learn joblib ucimlrepo
```

### 4. Run the application
```bash
streamlit run app.py
```

Open the local URL displayed in the terminal.

## 🚀 How to Use
1. Start the Streamlit application.
2. Enter a URL in the input field.
3. Click **Scan URL**.
4. Review the predicted classification.

## ⚠️ Limitations
- Predictions may be incorrect.
- URL-based features alone cannot establish whether a website is safe.
- The reported test accuracy does not guarantee real-world performance.

## 🔮 Future Improvements
- Test on independent, unseen URLs.
- Improve feature extraction and model validation.
- Add prediction confidence and clearer error handling.
- Improve the user interface and reporting.

## 👩‍💻 Project Status
Working prototype — further validation and testing are required.

## 📄 Disclaimer
This project is intended for educational purposes. Do not rely on its predictions as the sole basis for deciding whether a website is safe.
