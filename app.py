from flask import Flask, render_template, request, jsonify
import os
import base64
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('camera.html')

# Ensure this directory exists where images will be saved
UPLOAD_FOLDER = 'photos'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/save-photos', methods=['POST'])
def save_photos():
    data = request.get_json()
    folder_name = data.get('folderName')
    images = data.get('images', [])

    # Create a folder for the images if it doesn't exist
    folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    saved_files = []
    for index, image_data in enumerate(images):
        # Generate a unique filename for each image
        image_filename = f'photo_{index + 1}.png'
        image_path = os.path.join(folder_path, image_filename)

        # Decode the Base64 image data
        image_data = image_data.split(',')[1]  # Remove the base64 metadata prefix
        with open(image_path, 'wb') as image_file:
            image_file.write(base64.b64decode(image_data))

        saved_files.append(image_filename)

    return jsonify({
        'message': 'Photos saved successfully',
        'saved_files': saved_files
    }), 200

# Route to fetch all photos grouped by folder
@app.route('/photos', methods=['GET'])
def get_photos():
    photos_by_folder = {}
    for folder_name in os.listdir(UPLOAD_FOLDER):
        folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
        if os.path.isdir(folder_path):
            photos_by_folder[folder_name] = os.listdir(folder_path)
    
    return jsonify(photos_by_folder), 200

if __name__ == '__main__':
    app.run(debug=True)
