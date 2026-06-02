# 🔐 Password Security Analyzer

A production-ready web application that analyzes password strength using machine learning, entropy calculation, breach detection, and real-time feedback. Built with Flask, scikit-learn, and vanilla JavaScript.

![Cyber Security Theme](https://img.shields.io/badge/Theme-Cyber%20Security-blueviolet)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![ML](https://img.shields.io/badge/ML-RandomForest-orange)

## ✨ Features

- ML-Based Password Strength Prediction
- Shannon Entropy Calculation
- Breach Database Detection
- Password Score System (0–100)
- Common Password Blacklist
- Real-Time Recommendations
- Live Feedback System
- Strong Password Generator
- Show/Hide Password
- Copy to Clipboard
- Responsive Cyber Security Dashboard

## 🛠️ Technology Stack

| Layer       | Technologies                                      |
|-------------|---------------------------------------------------|
| Frontend    | HTML5, CSS3, Vanilla JavaScript                   |
| Backend     | Python Flask                                      |
| ML          | scikit-learn, pandas, numpy                       |
| Database    | SQLite                                            |
| Security    | XSS prevention, SQL injection protection         |

## 📁 Project Structure

```
Password-Security-Analyzer/
│
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── models/
│   ├── train_model.py         # ML training script
│   └── password_model.pkl     # Trained RandomForest model
│
├── database/
│   ├── breached_passwords.db  # SQLite breach database
│   └── common_passwords.txt   # Common password blacklist
│
├── static/
│   ├── css/
│   │   └── style.css          # Cyber‑themed styles
│   ├── js/
│   │   └── script.js          # Client‑side logic
│   └── assets/                # Images (logo, background)
│
├── templates/
│   └── index.html             # Main UI
│
├── utils/
│   ├── __init__.py
│   ├── entropy.py             # Shannon entropy calculator
│   ├── breach_checker.py      # Breach & blacklist detection
│   ├── recommendation.py      # Smart password suggestions
│   └── scorer.py              # Score calculation logic
│
└── dataset/                   # Generated training data (auto‑created)
    └── password_dataset.csv
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone or Download the Project

```bash
git clone https://github.com/Thabish0/Task-1-ThabishMuhammad.git
cd Password-Security-Analyzer
```

Or simply extract the ZIP file into a folder.

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Train the Machine Learning Model

```bash
python models/train_model.py
```

This generates the dataset, trains a RandomForest classifier, and saves `models/password_model.pkl`.  
You will see accuracy (~92%) and feature importance printed.

### Step 5: Initialize the Breach Database

```bash
python -c "from utils.breach_checker import BreachChecker; BreachChecker()"
```

This creates `database/breached_passwords.db` and `database/common_passwords.txt` with default breached passwords.

### Step 6: Run the Flask Application

```bash
python app.py
```

You should see:
```
✅ Database initialized with 28 breached passwords
✅ Loaded 28 common passwords
 * Running on http://127.0.0.1:5000
```

### Step 7: Open in Browser

Navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🧪 Usage

1. **Type or paste a password** – The analyzer updates instantly.
2. **View results** – Strength meter, score, entropy, breach status, and recommendations.
3. **Generate a strong password** – Click “Generate Strong Password”.
4. **Copy password** – Click the copy icon.
5. **Toggle visibility** – Click the eye icon to show/hide.

## 📄 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

*Remember: A strong password is your first line of defence.*
