# Description
This project aims to analyze the factors influencing the risk of heart disease using a dataset containing demographic, lifestyle, and medical information. By exploring these factors, we identify the most significant contributors to heart disease and develop a predictive model.

# Data Source
- Dataset source: Framingham Heart Study Dataset
- The dataset consists of 16 columns and 4,240 rows.
- Features Evaluated:
- Gender
- Age
- Education Level
- Smoking Status
- Cigarettes Consumed Per Day
- Blood Pressure Medication
- Prevalent Stroke
- Prevalent Hypertension
- Diabetes
- Total Cholesterol
- Systolic Blood Pressure
- Diastolic Blood Pressure
- Body Mass Index (BMI)
- Heart Rate
- Glucose Levels
## Using machine learning algorithms, the model predicts the likelihood of heart disease, providing actionable insights to improve health outcomes.

# Instructions to Run the Project
1. Prerequisites
- Python 3.12.5 (or compatible version)
- Pipenv installed (pip install pipenv)
- Required libraries listed in requirements.txt.
2. Clone the Repository
- git clone <repository-url>  
- cd <repository-folder>  
3. Set Up the Virtual Environment with Pipenv
- pipenv install --dev  
- pipenv shell  
4. Run the Project
(a) Train the Model
  - python train.py  
(b) Test the Model
 - python predict.py  
(c) Run the API (Optional)
 - python app.py  
- Access the API at http://127.0.0.1:8000.

5. Explore Results
- Analysis and visualizations are in the notebooks/EDA/.
 - Performance metrics are saved in the results/Model_Training/.
