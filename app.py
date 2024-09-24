from flask import Flask, render_template, request, jsonify
import os
import base64
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('camera.html')

BASE_DIR = 'photos'  # Base directory for saved photos

@app.route('/save-photos', methods=['POST'])
def save_photos():
    data = request.json
    folder_name = data['folderName']
    images = data['images']

    folder_path = os.path.join(BASE_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist

    saved_files = []
    for index, image in enumerate(images):
        # Generate a unique filename using the current timestamp
        unique_filename = f"{folder_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{index}.png"
        image_data = image.split(",")[1]  # Remove the data URL part
        with open(os.path.join(folder_path, unique_filename), "wb") as f:
            f.write(base64.b64decode(image_data))  # Save image

        saved_files.append(unique_filename)

    return jsonify(saved_files), 200

@app.route('/photos', methods=['GET'])
def get_photos():
    # Logic to return saved photos (similar to what you currently have)
    folders = {}
    for folder_name in os.listdir(BASE_DIR):
        folder_path = os.path.join(BASE_DIR, folder_name)
        if os.path.isdir(folder_path):
            folders[folder_name] = os.listdir(folder_path)
    return jsonify(folders)


if __name__ == '__main__':
    app.run(debug=True)
