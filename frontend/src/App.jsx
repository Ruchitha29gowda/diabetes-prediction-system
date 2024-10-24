import React, { useState } from 'react';
import './App.css'

function App() {
  // State to store form data and the prediction result
  const [formData, setFormData] = useState({
    gender: '',
    age: '',
    hypertension: '',
    heart_disease: '',
    bmi: '',
    HbA1c_level: '',
    blood_glucose_level: '',
  });

  const [prediction, setPrediction] = useState(null);

  // Handle form data changes
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Send POST request to the Flask API
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      const result = await response.json();
      setPrediction(result.prediction);
      console.log("Result is : "+result.prediction); // Fixed logging to use result.prediction
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="App">
      <h1>Diabetes Prediction</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" name="gender" placeholder="Gender: Male/Female" onChange={handleChange} />

        <input type="text" name="age" placeholder="Age" onChange={handleChange} />

        <input type="text" name="hypertension" placeholder="Hypertension" onChange={handleChange} />

        <input type="text" name="heart_disease" placeholder="Heart Disease" onChange={handleChange} />

        <input type="text" name="bmi" placeholder="BMI" onChange={handleChange} />

        <input type="text" name="HbA1c_level" placeholder="HbA1c Level" onChange={handleChange} />

        <input type="text" name="blood_glucose_level" placeholder="Blood Glucose Level" onChange={handleChange} />

        <button type="submit">Predict</button>
      </form>

      {prediction !== null && (
        <div id='results'>
          <h2>Prediction Result: {prediction === 1 ? "Diabetic" : "Non-Diabetic"}</h2>
        </div>
      )}
    </div>
  );
}

export default App;
