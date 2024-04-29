# app.py
from flask import Flask, render_template, request, redirect, url_for
import json
from DrawBboxes import draw_bounding_boxes

app = Flask(__name__, static_folder = 'C:/Users/Guy/Documents/PROJ300/Webapp Testing')

# Load data from data.json
with open('bounding_boxes.json', 'r') as f:
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
    with open('bounding_boxes.json', 'w') as f:
        json.dump(data, f, indent=4)
    draw_bounding_boxes("ClimbingHoldImg3.jpg", "bounding_boxes.json", "ClimbingImage.jpg")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)


