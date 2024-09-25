from flask import Flask, render_template, request, jsonify, send_file
import os
import base64
from datetime import datetime
import csv
import time
import uuid
import omr, utilis

app = Flask(__name__)

@app.route('/')
def camera():
    # Define the base directory
    base_directory = 'C:/xampp/htdocs/omr/uploads'
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

app.route('/scan', methods=['POST'])
def scan_route():
    data = request.get_json()
    folder_path = data.get('folderPath')

    # Check if the folder exists
    if os.path.exists(folder_path):
        # List all CSV files in the specified folder
        csv_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.csv')]
        
        # Check if any CSV files were found
        if not csv_files:
            return jsonify({'message': 'No CSV files found in the specified folder.'}), 404
        
        # Loop through each CSV file and run the OMR process
        results = []
        for csv_file in csv_files:
            # Call the omr function for each CSV file
            result_csv = omr.omr(csv_file, folder_path)
            results.append(result_csv)  # Collect result paths

        return jsonify({'message': f'Scanned folder: {folder_path}. Processed CSV files.', 'results': results})
    
    else:
        return jsonify({'message': 'Folder does not exist.'}), 404


if __name__ == '__main__':
    app.run(debug=True)
