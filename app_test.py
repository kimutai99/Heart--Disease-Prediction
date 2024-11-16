import requests


url = 'http://localhost:8000/predict'

patient_values={
    "male": 1.0,
    "age": 39.0,
    "education": 4.0,
    "currentsmoker": 0.0,
    "cigsperday": 0.0,
    "bpmeds": 0.0,
    "prevalentstroke": 0.0,
    "prevalenthyp": 0.0,
    "diabetes": 0.0,
    "totchol": 195.0,
    "bmi": 26.97,
    "heartrate": 80.0,
    "glucose": 77.0,
}

response=requests.post(url,json=patient_values).json()
print(response)
