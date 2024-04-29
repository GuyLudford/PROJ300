from flask import Flask, render_template, request, redirect, url_for
import json
from DrawBboxes import draw_bounding_boxes
import argparse
import os

# Create an argument parser
parser = argparse.ArgumentParser(description='Flask app for bounding boxes')

# Add arguments for image file and bounding box file
parser.add_argument('--image', type=str, default='ClimbingHoldImg3.jpg', help='Path to the image file')
parser.add_argument('--bbox', type=str, default='bounding_boxes.json', help='Path to the bounding box JSON file')

# Parse the command-line arguments
args = parser.parse_args()

app = Flask(__name__, static_folder=os.path.dirname(os.path.abspath(__file__)))

# Load data from the specified bounding box JSON file
with open(args.bbox, 'r') as f:
    data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', data=data)

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    new_color = request.form.get('color')
    new_grade = request.form.get('grade')
    new_id = request.form.get('route_id')

    # Update the color and grade for the current object
    data['objects'][id]['color'] = new_color
    data['objects'][id]['grade'] = new_grade
    data['objects'][id]['route_id'] = new_id

    # Update the grade for all objects with the same route ID
    for obj in data['objects']:
        if obj['route_id'] == new_id:
            obj['grade'] = new_grade

    return redirect(url_for('index'))

@app.route('/save', methods=['POST'])
def save():
    with open(args.bbox, 'w') as f:
        json.dump(data, f, indent=4)
    draw_bounding_boxes(args.image, args.bbox, "ClimbingImage.jpg")
    print(f"Saved bounding boxes to: {args.bbox}")
    print(f"Created ClimbingImage.jpg")
    return redirect(url_for('index'))

@app.route('/shutdown', methods=['POST'])
def shutdown():
    # Stop the server
    os._exit(0)

if __name__ == '__main__':
    # Run the draw_bounding_boxes function on startup
    draw_bounding_boxes(args.image, args.bbox, "ClimbingImage.jpg")
    app.run(debug=False)


