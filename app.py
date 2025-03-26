# app.py
from flask import Flask, render_template, jsonify
import os
import re

app = Flask(__name__)

# Configuration - use absolute paths based on the application's root directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGE_FOLDER = os.path.join(BASE_DIR, 'static', 'Heatmap_images')
NOISY_PRUNED_FOLDER = os.path.join(IMAGE_FOLDER, 'Real_authenticity', 'noisy_pruned_model')
BASE_MODEL_FOLDER = os.path.join(IMAGE_FOLDER, 'Real_authenticity', 'base_model')
ORIGINAL_FOLDER = os.path.join(IMAGE_FOLDER, 'Real_authenticity', 'original_images')

# Ensure all directories exist
def ensure_dir(directory):
    if not os.path.exists(directory):
        print(f"Warning: Directory does not exist: {directory}")

for directory in [BASE_MODEL_FOLDER, NOISY_PRUNED_FOLDER, ORIGINAL_FOLDER]:
    ensure_dir(directory)

@app.route('/')
def index():
    """Main page of the application."""
    return render_template('index.html')

@app.route('/api/image-info')
def get_image_info():
    """API endpoint to get image information and max index."""
    # Get list of files in base model directory
    try:
        if not os.path.exists(BASE_MODEL_FOLDER):
            return jsonify({
                'max_index': 0,
                'indices': [],
                'error': f"Directory not found: {BASE_MODEL_FOLDER}"
            })
            
        files = os.listdir(BASE_MODEL_FOLDER)
        
        # Extract indices from file names
        pattern = re.compile(r'heatmap_img_idx(\d+)\.png')
        indices = []
        for file in files:
            match = pattern.match(file)
            if match:
                indices.append(int(match.group(1)))
        
        # Get max index
        max_index = max(indices) if indices else 0
        
        return jsonify({
            'max_index': max_index,
            'indices': sorted(indices)
        })
    except Exception as e:
        print(f"Error getting image info: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)