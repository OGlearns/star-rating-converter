from flask import Flask, request, jsonify, render_template
import csv
import io

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/convert_ratings', methods=['POST'])
def convert_ratings():
    try:
        # Get the uploaded file from the request
        uploaded_file = request.files['file']

        # Read the CSV file into a list of dictionaries
        csv_data = []
        csv_reader = csv.DictReader(io.StringIO(uploaded_file.read().decode('utf-8')))

        fieldnames = csv_reader.fieldnames
        
        # Ensure the 'ratings' column exists
        if 'rating' not in fieldnames:
            return jsonify({'error': 'Column "rating" not found in the CSV file.'})
        
        for row in csv_reader:
            csv_data.append(row)

        # Convert the ratings to a 10-point system
        for row in csv_data:
            row['rating'] = str(int(row['rating']) * 2)

        # Prepare the updated CSV data
        updated_csv = io.StringIO()
        csv_writer = csv.DictWriter(updated_csv, fieldnames=csv_data[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(csv_data)

        # Create a response with the updated CSV data
        response = jsonify({'updated_csv': updated_csv.getvalue()})
        response.headers['Content-Disposition'] = 'attachment; filename=updated_ratings.csv'
        response.headers['Content-Type'] = 'text/csv'
        return response

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == "__main__":
    app.run(debug=True)
