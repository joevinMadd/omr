from flask import Flask, render_template, request, jsonify
import os
import base64
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('camera.html')

def save_photos():
    data = request.get_json()
    folder_name = data['folderName']
    images = data['images']

    # Ensure the folder exists
    folder_path = os.path.join('static', 'photos', folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    saved_files = []

    # Loop through each image and save it with a unique filename
    for image_data in images:
        # Create a unique filename using timestamp
        unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}.png"
        image_path = os.path.join(folder_path, unique_filename)

        # Decode the base64 image and save it
        img_data = base64.b64decode(image_data.split(',')[1])
        with open(image_path, 'wb') as f:
            f.write(img_data)
        
        saved_files.append(unique_filename)

    return jsonify({'message': 'Photos saved', 'saved_files': saved_files}), 200

# Route to list photos in all folders
@app.route('/photos', methods=['GET'])
def get_photos():
    photos_directory = os.path.join('static', 'photos')
    if not os.path.exists(photos_directory):
        return jsonify({})

    folders = {}
    for folder_name in os.listdir(photos_directory):
        folder_path = os.path.join(photos_directory, folder_name)
        if os.path.isdir(folder_path):
            folders[folder_name] = os.listdir(folder_path)

    return jsonify(folders)


if __name__ == '__main__':
    app.run(debug=True)
