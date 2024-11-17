# Heart--Disease-Prediction

# Description
This project aims to analyze the factors influencing the risk of heart disease using a dataset containing demographic, lifestyle, and medical information. By exploring these factors, we identify the most significant contributors to heart disease and develop a predictive model.

# Data Source
- Dataset source - https://www.kaggle.com/datasets/aasheesh200/framingham-heart-study-dataset
- This data consists of 16 columns and 4240 rows

## The project evaluates features such as:

Gender
Age
Education Level
Smoking Status
Cigarettes Consumed Per Day
Blood Pressure Medication
Prevalent Stroke
Prevalent Hypertension
Diabetes
Total Cholesterol
Systolic Blood Pressure
Diastolic Blood Pressure
Body Mass Index (BMI)
Heart Rate
Glucose Levels
Using machine learning algorithms, the model predicts the likelihood of heart disease, providing actionable insights to improve health outcomes.

## Instructions to Run the Projects

1. Prerequisites
. Python 3.12.5 (or compatible version)
. A Python virtual environment setup (optional but recommended)
. Required libraries listed in requirements.txt
2. Clone the Repository
   git clone <repository-url> 
3. Set Up the Virtual Environment with Pipenv
   . pipenv install --dev  
   . pipenv shell  
4. Run the Project
   a) Train the Model
      python train.py
   b) Test the Model
       python predict.py
   c)Run the API (Optional)
       python app.py
       Access the API at http://127.0.0.1:8000.  
5. Explore Results
Analysis and visualizations are in the notebooks/ EDA .
Performance metrics are saved in the results/ Model training. 

