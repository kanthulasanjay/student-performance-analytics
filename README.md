# 🎓 Student Performance Analytics

A Machine Learning-powered web application built with **Streamlit** that predicts a student's GPA based on demographic information, academic performance, parental support, and extracurricular activities.

The application provides an interactive dashboard where users can input student details and receive an estimated GPA prediction along with performance insights.

---

## 📌 Project Overview

Student academic performance depends on several factors such as study time, attendance, parental support, extracurricular activities, and demographic characteristics.

This project uses a trained Machine Learning regression model to analyze these factors and predict the student's GPA through an interactive Streamlit dashboard.

---

## 🚀 Features

- 🎯 Predict Student GPA using Machine Learning
- 📊 Interactive Streamlit Dashboard
- 📈 Beautiful Gauge Chart Visualization
- 📋 Display Raw Student Input
- ⚙️ Display Scaled Input Used by the Model
- 📚 Feature Engineering
- 💡 Performance Category Prediction
- 🎨 Modern Responsive UI

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Scikit-learn
- Pandas
- NumPy
- Plotly
- Joblib

---

## 📂 Project Structure

```
student-performance-analytics/
│
├── app.py
├── best_student_model.pkl
├── scaler.pkl
├── requirements.txt
├── student_performance.ipynb
├── Student_performance_data.csv
├── README.md
└── screenshots/
```

---

## 📊 Dataset Features

The model uses the following student information:

- Age
- Gender
- Ethnicity
- Parental Education
- Study Time Weekly
- Absences
- Tutoring
- Parental Support
- Extracurricular Activities
- Sports
- Music
- Volunteering
- Grade Class

### Engineered Features

- Study Efficiency
- Academic Support
- Activity Score
- Total Engagement

---

## 🤖 Machine Learning Workflow

1. Data Collection
2. Data Cleaning
3. Exploratory Data Analysis (EDA)
4. Feature Engineering
5. Data Scaling
6. Model Training
7. Model Evaluation
8. Model Selection
9. Model Serialization
10. Streamlit Deployment

---

## 📈 Performance Prediction

The application predicts GPA on a **10-point scale**.

Performance Categories:

| GPA | Category |
|------|-----------|
| 8.75 – 10 | ⭐⭐⭐⭐⭐ Excellent |
| 7.50 – 8.74 | 👍 Good |
| 5.00 – 7.49 | ⚠️ Average |
| Below 5 | ❌ Needs Improvement |

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/student-performance-analytics.git
```

Go to the project directory

```bash
cd student-performance-analytics
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 📸 Application Preview

### Dashboard

<img width="1836" height="863" alt="image" src="https://github.com/user-attachments/assets/458efd4c-1acb-4134-bbd0-0fa34399fcfa" />


---

### Prediction Result

<img width="1876" height="890" alt="image" src="https://github.com/user-attachments/assets/cdf43fd3-e508-4f68-9d39-1944fbb069cb" />

---

## 📊 Libraries Used

```
pandas
numpy
matplotlib
seaborn
plotly
scikit-learn
streamlit
joblib
xgboost
```

---

## 🎯 Future Improvements

- Multiple Machine Learning Models Comparison
- Feature Importance Visualization
- Student Performance Reports
- Download Prediction as PDF
- Cloud Deployment
- Authentication System
- Database Integration

---

## 👨‍💻 Author

**Sanjay**

Computer Science & Data Science Student

Machine Learning | Data Science | Python | Streamlit
