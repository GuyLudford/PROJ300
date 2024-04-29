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
    frame = cv2.imread("C:/Users/Guy/Documents/PROJ300/Person Recognition Testing/Test Images/Screenshot 2024-04-27 124952.png")
    #detected_bbox = (x, y, w, h)  # Example bounding box

    # Load stored images and extract SIFT features
    stored_images_folder = 'C:/Users/Guy/Documents/PROJ300/Person Recognition Testing/Person Images'  # List of stored image IDs
    stored_descriptors = {}
    for image_filename in os.listdir(stored_images_folder):
        image_path = os.path.join(stored_images_folder, image_filename)
        stored_image = load_stored_image(image_path)
        if stored_image is not None:
            # Extract SIFT features for the stored image (you can modify this part)
            _, stored_descriptor = extract_sift_features(stored_image)
            stored_descriptors[image_filename] = {
                'head': stored_descriptor,
                'torso': stored_descriptor,
                'upper_legs': stored_descriptor,
                'lower_legs': stored_descriptor,
            }
        else:
            print(f"Skipping {image_filename} due to loading error.")

    # Extract SIFT features for the detected person
    detected_image = frame
    keypoints, detected_descriptor = extract_sift_features(detected_image)
    detected_descriptors = {
        'head': detected_descriptor,
        'torso': detected_descriptor,
        'upper_legs': detected_descriptor,
        'lower_legs': detected_descriptor,
    }

    # Compare features and find the closest fit
    closest_fit_id = compare_with_stored_images_sift(detected_descriptors, stored_descriptors)
    print(f"Detected person is most similar to ID {closest_fit_id}")
    return [int(x) for x in re.findall(r'\d+', closest_fit_id)]
