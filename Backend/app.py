from flask import Flask, redirect, render_template, request, jsonify
from ai import aifunction  # Import the aifunction from ai.py
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def takeinput():
    if request.method == 'POST':
        userinput = request.form['userinput']
        prediction = aifunction(userinput)  # Assuming aifunction is defined elsewhere
        return render_template("index.html", prediction=prediction, userinput=userinput)
    return render_template("index.html")

@app.route('/generate')
def generate_summary():
    userinput = request.args.get('userinput', '')
    prediction = aifunction(userinput)  # Call aifunction from ai.py to get the prediction

    # Pass prediction to the template for rendering
    return render_template("result.html", userinput=userinput, prediction=prediction)

@app.route('/detection', methods=['POST'])
def detection():
    if request.method == 'POST':
        data = request.json
        userinput = data.get('userinput')  # Use .get() to safely retrieve data without causing errors
        if userinput is not None:
            prediction = aifunction(userinput)
            return jsonify({'prediction': prediction}), 200  # Return a JSON response with prediction and 200 status code
        else:
            return jsonify({'error': 'userinput not provided'}), 400  # Return an error response with 400 status code if userinput is not provided
    else:
        return jsonify({'error': 'Method Not Allowed'}), 405  # Return an error response with 405 status code if the method is not allowed
@app.route('/save_record', methods=['POST'])
def save_record():
    data = request.json
    content = data['content']
    is_fake = data['is_fake']
    
    # Append data to an Excel file
    df = pd.DataFrame({'Content': [content], 'IsFake': [is_fake]})
    df.to_excel('records.xlsx', index=False, header=not os.path.exists('records.xlsx'), mode='a')
    
    return jsonify({'message': 'Record saved successfully'})

if __name__ == "__main__":
     app.run( port=5000, debug=True)



