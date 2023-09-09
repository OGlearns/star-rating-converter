from flask import Flask, request, jsonify, render_template, send_file
import pandas as pd
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/convert_ratings', methods=['POST'])
def convert_ratings():
    try:

        # Get the uploaded file from the request
        uploaded_file = request.files['file']

        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(uploaded_file)

        # Ensure the 'rating' column exists
        if 'rating' not in df.columns:
            return jsonify({'error': 'Column "rating" not found in the CSV file.'})

        # Double the values in the 'rating' column
        df['rating'] = df['rating'] * 2

        # Prepare the updated CSV data
        updated_csv = BytesIO()
        df.to_csv(updated_csv, index=False)

        # Return the updated CSV file
        updated_csv.seek(0)
        return send_file(updated_csv, as_attachment=True, attachment_filename=uploaded_file.filename, mimetype='text/csv')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
