from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib
import pandas as pd

# Load the trained model and scaler
model = joblib.load('model/diabetes_voting_model.pkl')
scaler = joblib.load('model/scaler.pkl')

app = Flask(__name__)
CORS(app)

def encode_input(data):
    # Encoding categorical variables
    gender = 1 if data['gender'].lower() == 'male' else 0  # Encode 'Male' as 1 and 'Female' as 0

    # Prepare the input data as a float array
    return np.array([[gender, float(data['age']), int(data['hypertension']),
                      int(data['heart_disease']), float(data['bmi']), 
                      float(data['HbA1c_level']), float(data['blood_glucose_level'])]])

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Check if all required fields are present
    required_fields = ['gender', 'age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Encode and prepare the input data
    input_data = encode_input(data)

    print("Input data:", input_data)  # Debugging statement

    try:
        # # Scale the input data - convert to DataFrame with the same columns as used for fitting
        # #gender,age,hypertension,heart_disease,bmi,HbA1c_level,blood_glucose_level,diabetes
        # input_data_df = pd.DataFrame(input_data, columns=['gender', 'age', 'hypertension', 'heart_disease', 'bmi', 'HbA1c_level', 'blood_glucose_level'])

        # print("***************created the data frame***************")
        # print(input_data_df)

        # # Ensure the DataFrame is correctly ordered and has the same features as used during scaling
        # input_data_scaled = scaler.transform(input_data_df)  # Scale the input data
        
        # print("**********after scaling*******")
        
        
        input_data = np.array(input_data).reshape(1, -1)
    
        # Scale the necessary columns
        input_data[:, [1, 4, 5, 6]] = scaler.transform(input_data[:, [1, 4, 5, 6]])
        # Make the prediction
        prediction = model.predict(input_data)

        
        
        # Return the result
        result = {"prediction": int(prediction[0])}
        print("********ending the try block**********\n\n\n")
        print(input_data)
        print(prediction)
        result = {"prediction": int(prediction[0])}
        return jsonify(result)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
