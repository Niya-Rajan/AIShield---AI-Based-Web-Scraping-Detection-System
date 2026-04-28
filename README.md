# 🛡️ AIShield – Deception-Based Web Scraping Detection System

## 🚀 Overview
**AIShield** is an intelligent web security system designed to detect and mitigate automated web scraping using **behavioral analysis, machine learning, and deception techniques**.

Unlike traditional approaches such as CAPTCHA or IP blocking, AIShield focuses on analyzing **user behavior patterns** to identify sophisticated bots that mimic human activity. Instead of blocking malicious users, the system serves **misleading content**, making scraping ineffective while maintaining a seamless experience for legitimate users.

---

## 🎯 Key Features

- 🔍 **Behavioral Analysis**
  - Real-time tracking of user sessions
  - Feature extraction: navigation speed, session duration, interaction patterns

- 🤖 **Machine Learning Detection**
  - XGBoost classifier for human vs bot classification
  - Optimized for structured behavioral data

- 🎭 **Deception Mechanism (Core Innovation)**
  - Serves fake or modified content to detected bots
  - Reduces value of extracted data

- 🕵️ **Honeypot Detection**
  - Hidden endpoints to trap automated crawlers
  - Enhances bot identification

- ⚡ **Real-Time Processing**
  - Lightweight middleware integration
  - Minimal latency for real users

---

## 🧠 System Architecture

1. User interacts with the web application  
2. Session data is captured and logged  
3. Behavioral features are extracted  
4. ML model classifies session:
   - `Human (0)`
   - `Bot (1)`  
5. Response handling:
   - Human → Normal content  
   - Bot → Deceptive / fake content  

---

## 📊 Dataset

- Self-curated dataset (no public dataset used)
- 253 session samples:
  - 160 Human sessions
  - 93 Bot sessions

### Features:
- Pages visited  
- Session duration  
- Average time per page  
- Pages per minute (derived feature)

---



---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)  
- **Machine Learning:** XGBoost, Scikit-learn  
- **Data Processing:** Pandas, NumPy  
- **Frontend:** HTML, CSS, JavaScript  
- **Logging:** CSV-based session logging  

---

---

---

## 💡 Why AIShield?

AIShield introduces a **proactive security approach**:

> Instead of blocking bots, it **misleads them**.

This makes it more effective against modern AI-driven scrapers while preserving user experience.

---


---

## 📄 License

This project is licensed under the MIT License.
