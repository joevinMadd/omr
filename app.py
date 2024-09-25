from flask import Flask, render_template, request, jsonify
import os
import time
import uuid
from omr2 import omr
from datetime import datetime  # Ensure this is imported at the top of your file
import pandas as pd

app = Flask(__name__)

@app.route('/')
def camera():
    # Define the base directory
    base_directory = os.path.join(os.getcwd(), 'uploads')
    folder_paths = {}

    # Loop through folders to collect CSV files
    for folder_name in os.listdir(base_directory):
        folder_path = os.path.join(base_directory, folder_name)
        if os.path.isdir(folder_path):
            # List all CSV files in this folder
            csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
            folder_paths[folder_name] = {
                'folder_path': folder_path,
                'csv_files': csv_files
            }

    # Render the template with folder_paths
    return render_template('camera.html', folder_paths=folder_paths)

UPLOAD_FOLDER = 'uploads'

# Create a route for saving photos
@app.route('/save-photos', methods=['POST'])
def save_photos():
    folder_name = request.form['folderName']
    folder_path = os.path.join(UPLOAD_FOLDER, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    photos = request.files.getlist('images')
    
    for photo in photos:
        # Create a unique filename using a combination of timestamp and UUID
        unique_filename = f"{int(time.time())}_{uuid.uuid4().hex[:8]}_{photo.filename}"
        photo.save(os.path.join(folder_path, unique_filename))

    return jsonify({'status': 'success'}), 200

# Create a route for uploading CSV file
@app.route('/upload-csv', methods=['POST'])
def upload_csv():
    folder_name = request.form['folderName']
    folder_path = os.path.join(UPLOAD_FOLDER, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    csv_file = request.files['csvFile']
    csv_file.save(os.path.join(folder_path, csv_file.filename))

    return jsonify({'status': 'success'}), 200

# Route to fetch saved photos (for displaying in the chart)
@app.route('/photos', methods=['GET'])
def get_photos():
    photos_by_folder = {}
    for folder_name in os.listdir(UPLOAD_FOLDER):
        folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
        if os.path.isdir(folder_path):
            photos = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
            photos_by_folder[folder_name] = photos

    return jsonify(photos_by_folder)

@app.route('/scan', methods=['POST'])
def scan_route():
    data = request.get_json()
    folder_path = data.get('folderPath')

    if os.path.exists(folder_path):
        csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]
        
        if not csv_files:
            return jsonify({'message': 'No CSV files found in the specified folder.'}), 404
        
        results = []
        all_data = []  # To store all the data for the CSVs
        start_time = time.time()
        
        for csv_file in csv_files:
            result_csv = omr(csv_file, folder_path)  # Call the omr function
            
            # Load the results CSV to return data
            if result_csv:
                df = pd.read_csv(result_csv)
                all_data.extend(df.to_dict(orient='records'))  # Extend records for later display
                results.append(result_csv)

        elapsed_time = time.time() - start_time
        
        return jsonify({
            'message': f'Scanned folder: {folder_path}. Processed CSV files.',
            'results': results,
            'data': all_data,  # Return the combined data for display
            'elapsed_time': elapsed_time
        })
    
    else:
        return jsonify({'message': 'Folder does not exist.'}), 404



if __name__ == '__main__':
    app.run(debug=True)
