from flask import Flask, render_template, request, jsonify
import os
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('camera.html')

@app.route('/save-photo', methods=['POST'])
def save_photo():
    data = request.json
    folder_name = data.get('folderName')
    image_data = data.get('image')

    # Create folder if it doesn't exist
    folder_path = os.path.join('static', 'photos', folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # Save the image
    image_data = image_data.split(',')[1]
    image_path = os.path.join(folder_path, 'photo.png')
    with open(image_path, 'wb') as f:
        f.write(base64.b64decode(image_data))

    return jsonify({"message": "Photo saved"}), 200

@app.route('/photos/<folder_name>')
def get_photos(folder_name):
    folder_path = os.path.join('static', 'photos', folder_name)
    if not os.path.exists(folder_path):
        return jsonify([])

    photos = os.listdir(folder_path)
    return jsonify(photos)

@app.route('/photos')
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
