import cv2
import json

def draw_bounding_boxes(image_path, json_path, output_path):

    predefined_colors = { #BGR
    'Black': (0, 0, 0),
    'White': (255, 255, 255),
    'Green': (0, 128, 0),
    'Yellow': (0, 255, 255),
    'Red': (0, 0, 255),
    'Orange': (0, 165, 255),
    'Pink': (203, 192, 255),
    'Blue': (255, 0, 0),
    'Purple': (128, 0, 128),
    'Beige': (220, 245, 245),
    'unknown':(0,0,0),
    'Grey':(128, 128, 128)
}
    
    # Read the image
    image = cv2.imread(image_path)

    # Load bounding box data from JSON
    with open(json_path, 'r') as json_file:
        data = json.load(json_file)

    # Draw bounding boxes and labels
    for obj in data['objects']:
        x1, y1, x2, y2 = obj['bbox']
        color = predefined_colors[obj["color"]]  # Red color for bounding boxes
        thickness = 2
        cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
        cv2.putText(image, f"{obj['id']}", (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

    # Save the modified image
    cv2.imwrite(output_path, image)
