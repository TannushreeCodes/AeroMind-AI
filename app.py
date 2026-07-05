# Import Flask and required libraries
from flask import Flask, render_template, request # For web application and handling HTTP requests
import pickle # To load the trained ML model
import numpy as np # For numerical array operations

# Initialize Flask application
app = Flask(__name__)

# Load the pre-trained model from model.pkl file
model = pickle.load(open('model.pkl', 'rb'))

def get_aqi_category(aqi):
     # Function to return AQI category and color based on EPA standards
    if aqi <= 50:
        return 'good', '🟢 Good - Air quality is satisfactory'
    elif aqi <= 100:
        return 'moderate', '🟡 Moderate - Air quality is acceptable' 
    elif aqi <= 150:
        return 'unhealthy-sensitive', '🟠 Unhealthy for Sensitive Groups'
    elif aqi <= 200:
        return 'unhealthy', '🔴 Unhealthy - Everyone may experience effects'
    elif aqi <= 300:
        return 'very-unhealthy', '🟣 Very Unhealthy - Health alert'
    else:
         else:
        return 'hazardous', '⚫ Hazardous - Emergency coditions'

# Define route for home page
@app.route('/')
def home():
    """Renders the main page with input form"""
    return render_template('index.html')

# Define route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    """Handles form submission and returns AQI prediction"""
    try:
        # Extract input values from form and convert to float
        pm25 = float(request.form['PM2.5']) # Fine particulate matter
        pm10 = float(request.form['PM10']) # Coarse particulate matter
        no2 = float(request.form['NO2']) # Nitrogen Dioxide
        so2 = float(request.form['SO2']) # Sulfur Dioxide
        co = float(request.form['CO']) # Carbon Monoxide
        o3 = float(request.form['O3']) # Ozone

        # Create numpy array for model input - must be 2D array
        features = np.array([[pm25, pm10, no2, so2, co, o3]])

        # Generate prediction using loaded model
        prediction = model.predict(features)
        output = round(prediction[0], 2) # Round to 2 decimal places

        # Get category and health message based on predicted AQI
        category, category_text = get_aqi_category(output)

        # Render template with prediction results
        return render_template('index.html',
                             prediction_text=f'Predicted AQI: {output}',
                             category=category,
                             category_text=category_text)

    except Exception as e:
        # Handle errors gracefully - invalid input or missing fields
        return render_template('index.html',
                             prediction_text='Error: Please enter valid numerical values',
                             category='unhealthy',
                             category_text=str(e))

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True) # debug=True enables auto-reload on code changes