import os
import base64
from flask import Flask, request, jsonify, send_from_directory
from PIL import Image
from io import BytesIO

app = Flask(__name__)

# Folder where photos will be saved
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/save-photo', methods=['POST'])
def save_photo():
    data = request.json
    folder_name = data['folderName']
    image_data = data['image'].split(',')[1]  # Remove the base64 header

    # Create folder if it doesn't exist
    folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Decode the base64 image and save it as a PNG file
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    file_name = f"{len(os.listdir(folder_path)) + 1}.png"
    file_path = os.path.join(folder_path, file_name)
    image.save(file_path)

    return jsonify({'message': 'Photo saved successfully!'})

@app.route('/photos/<folder_name>', methods=['GET'])
def list_photos(folder_name):
    folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
    if not os.path.exists(folder_path):
        return jsonify([])

    # List all files in the folder
    photos = os.listdir(folder_path)
    return jsonify(photos)

@app.route('/photos/<folder_name>/<filename>', methods=['GET'])
def get_photo(folder_name, filename):
    folder_path = os.path.join(UPLOAD_FOLDER, folder_name)
    return send_from_directory(folder_path, filename)

if __name__ == '__main__':
    app.run(debug=True)
