Student Placement Prediction System

A Machine Learning-powered web application that predicts whether a student is likely to be placed based on academic performance, technical skills, internships, projects, aptitude, communication skills, certifications, and other relevant attributes.

The application is built using Python, Scikit-learn, and Streamlit, and provides both placement predictions and interpretable insights to help users understand the factors influencing the prediction.

Features

Predicts whether a student is likely to be Placed or Not Placed
Displays prediction confidence score
Provides explainable AI insights by comparing user inputs with placed student benchmarks
Interactive and responsive Streamlit web application
Modern dark-themed dashboard
Random Forest Machine Learning model
End-to-end ML pipeline from data preprocessing to deployment
Technologies Used

Python
Pandas
NumPy
Scikit-learn
Matplotlib
Seaborn
Streamlit
Joblib
Machine Learning Workflow

Data Collection
Data Cleaning
Exploratory Data Analysis (EDA)
Feature Engineering & Preprocessing
Train-Test Split
Model Training
Model Evaluation
Model Selection
Model Serialization using Joblib
Streamlit Deployment
Dataset Information

Dataset Size: 50,000 student records
Features: Academic, technical, aptitude, internship, project, and soft-skill related attributes
Target Variable: Placement Status (Placed / Not Placed)
Input Features

Age
Gender
Degree
Branch
CGPA
Internships
Projects
Coding Skills
Communication Skills
Aptitude Test Score
Soft Skills Rating
Certifications
Backlogs
Project Structure

Student-Placement-Prediction/
│
├── app3.py                    # Streamlit web application
├── project.ipynb              # Complete machine learning workflow
├── placement_model.pkl        # Trained Random Forest model
├── placed_avg_stats.pkl       # Average values of placed students
├── train.csv                  # Training dataset
├── requirements.txt           # Required Python libraries
├── README.md                  # Project documentation
├── config.toml                # Streamlit configuration

---


##  Run the Application

```bash
streamlit run app3.py
The application will open in your default browser.

Model Information

Model	Purpose
Logistic Regression	Baseline Model
Random Forest	Final Selected Model
The Random Forest classifier was selected based on its superior performance during evaluation and cross-validation.

Future Improvements

Hyperparameter tuning
Feature importance visualization
Additional ML algorithms
Deep Learning implementation
Resume upload and analysis
Cloud deployment
User authentication
Database integration
Author

Shubham Pal

B.Sc. Artificial Intelligence & Machine Learning

Thakur College of Science & Commerce

📌 Project Overview

The Student Placement Prediction System is an end-to-end Machine Learning project that predicts whether a student is likely to be placed during campus recruitment based on academic performance, technical skills, internships, projects, aptitude, communication skills, certifications, and other relevant attributes.

The project covers the complete machine learning lifecycle—from data preprocessing and exploratory data analysis (EDA) to model training, evaluation, and deployment using Streamlit.
# student-placement-prediction
