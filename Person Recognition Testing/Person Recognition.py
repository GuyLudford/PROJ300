import cv2
import numpy as np
import os

# Step 2: Feature Extraction using SIFT
def extract_sift_features(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(gray_image, None)
    return keypoints, descriptors

# Step 3: Comparison with Stored Images (SIFT Matching)
def compare_with_stored_images_sift(detected_descriptors, stored_descriptors):
    bf = cv2.BFMatcher()
    best_match_id = None
    best_similarity = float('-inf')

    for stored_id, stored_descriptor in stored_descriptors.items():
        similarity_sum = 0
        for region in ['head', 'torso', 'upper_legs', 'lower_legs']:
            detected_hist = detected_descriptors[region]
            stored_hist = stored_descriptor[region]
            matches = bf.knnMatch(detected_hist, stored_hist, k=2)
            good_matches = [m for m, n in matches if m.distance < 0.75 * n.distance]
            similarity_sum += len(good_matches)

        # Calculate overall similarity as the sum of individual region similarities
        similarity = similarity_sum / 4

        if similarity > best_similarity:
            best_similarity = similarity
            best_match_id = stored_id

    return best_match_id

def load_stored_image(image_path):
    try:
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)  # Load image in color
        if image is None:
            print(f"Error loading image from {image_path}")
            return None
        return image
    except Exception as e:
        print(f"Error loading image: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Load your frame and bounding box data
    frame = cv2.imread('C:/Users/Guy/Documents/PROJ300/Person Recognition Testing/Test Images/Screenshot 2024-04-27 124901.png')#Take in bbox of climber)
    #detected_bbox = (x, y, w, h)  # Example bounding box


    height, width = frame.shape[:2]
    quarter_width = width // 4
    quarter_height = height
    
    # Define the bounding box coordinates for each quarter
    head_coords = (0, 0, quarter_width, quarter_height)
    torso_coords = (quarter_width, 0, 2 * quarter_width, quarter_height)
    upper_legs_coords = (2 * quarter_width, 0, 3 * quarter_width, quarter_height)
    lower_legs_coords = (3 * quarter_width, 0, width, quarter_height)

    coordinates_list = [head_coords, torso_coords, upper_legs_coords, lower_legs_coords]

    #Load stored images and extract SIFT features
    stored_images_folder = 'C:/Users/Guy/Documents/PROJ300/Person Recognition Testing/Person Images'  # List of stored image IDs
    stored_descriptors = {}
    for image_filename in os.listdir(stored_images_folder):
        image_path = os.path.join(stored_images_folder, image_filename)
        stored_image = load_stored_image(image_path)
        if stored_image is not None:

            height, width = stored_image.shape[:2]
            quarter_width = width // 4
            quarter_height = height
            
            # Define the bounding box coordinates for each quarter
            head_coords = (0, 0, quarter_width, quarter_height)
            torso_coords = (quarter_width, 0, 2 * quarter_width, quarter_height)
            upper_legs_coords = (2 * quarter_width, 0, 3 * quarter_width, quarter_height)
            lower_legs_coords = (3 * quarter_width, 0, width, quarter_height)

            coordinates_list = [head_coords, torso_coords, upper_legs_coords, lower_legs_coords]
            
            for i, (x, y, w, h) in enumerate(coordinates_list):
                cropped_section = stored_image[y:y+h, x:x+w]
                _, stored_descriptor = extract_sift_features(cropped_section)
                section_name = f'section_{i}'
                stored_descriptors[image_filename][section_name] = stored_descriptor
        else:
            print(f"Skipping {image_filename} due to loading error.")

    # Extract SIFT features for the detected person
    detected_image = frame
    detected_descriptors = {}
    for i, (x, y, w, h) in enumerate(coordinates_list):
        cropped_section = detected_image[y:y+h, x:x+w]
        _, detected_descriptor = extract_sift_features(detected_image)
        section_name = f'section_{i}'
        detected_descriptors[section_name] = detected_descriptor

    # Compare features and find the closest fit
    closest_fit_id = compare_with_stored_images_sift(detected_descriptors, stored_descriptors)
    print(f"Detected person is most similar to ID {closest_fit_id}")
