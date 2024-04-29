import subprocess
import os
import cv2

#find video footage and methods
Footages = find_video_files('Video Footage')

for footage in footages:
    clippedFrame = extract_first_frame(footage)

    #delete old bbox data and saved images...

    #Run bbox finding
    arguments = ['--source', clippedFrame, '--device', 'cpu', '--nosave']
    command = ['py', '-3.10', "Hold Finder\detect.py"] + arguments
    #returns BBOX data in it's own folder and saves image
    #Clipped frame already stored in its own folder

    try:
        # Execute the command and wait for completion
        subprocess.run(command, check=True)
        print(f"BBOX calculation execution completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error executing script '{script_name}': {e}")

    
#These should be two seperate functions to be run when called by user. this one should delete
##############################################################################

Images = find_image_files(Blank Wall Images)
for image in images: # for all wall images in folder, run for file and matching file clippedframe name...

    #find bbox folder
    camera_number = get_camera_number(image)
    bbox_filename = f"BoundingBoxes_Camera{camera_number}.json"
    bbox_path = os.path.join(BboxData, bbox_filename)

    #Launch Flask App
    arguments = ['--image', image, '--bbox', bbox_path]
    command = [flask --app app run] + arguments

    try:
        # Execute the command and wait for completion
        subprocess.run(command, check=True)
        print(f"Flask app execution completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error executing script '{script_name}': {e}")


##############################################################################
#once a day:
        

for video_file in os.listdir(video_folder):
    if video_file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):

        arguments = ['--source', video_file, '--device', 'cpu']
        command = ['py', '-3.10', "Pose Estimation\pose-estimate.py"] + arguments

        try:
            # Execute the command and wait for completion
            subprocess.run(command, check=True)
            print(f"Processed {video_file}. Results saved")
            # Delete processed video
            os.remove(os.path.join(video_folder, video_file))
            print(f"Deleted {video_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing script '{script_name}': {e}")


KeypointFiles = find_json_files(Keypoints)
for keypointsfile in KeypointsFiles

        gymID = get_or_create_statistics_file()

        OutputFile = "Statistics".json

        camera_number = get_camera_number(keypointsfile)
        bbox_filename = f"BoundingBoxes_Camera{camera_number}.json"
        bbox_path = os.path.join(BboxData, bbox_filename)
        arguments = ['--source', keypointsfile, bbox_path, OutputFile, gymID]
        command = ['py', '-3.10', "Logging.py"] + arguments

        try:
            # Execute the command and wait for completion
            subprocess.run(command, check=True)
            print(f"Anayalsed Climbing. Results saved")
            # Delete processed Pose Estimation Code
            os.remove(os.path.join(video_folder, video_file))
            print(f"Deleted {video_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing script '{script_name}': {e}")


# move to utilities
def find_video_files(folder_path):
    video_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                video_files.append(os.path.join(root, file))
    return video_files

def find_image_files(folder_path):
    image_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_files.append(os.path.join(root, file))
    return image_files

def find_json_files(folder_path):
    json_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files


def extract_first_frame(video_file):
    cap = cv2.VideoCapture(video_file)
    success, frame = cap.read()
    if success:
        # Get the camera number
        camera_number = get_camera_number(video_file)

        # Construct the output image path
        output_folder = 'Blank Wall Images'
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
        output_image_name = f"Cropped_Image_Camera{camera_number}.jpg"
        output_image_path = os.path.join(output_folder, output_image_name)
        cv2.imwrite(output_image_path, frame)
        return output_image_path
    else:
        print(f"Error reading {video_file}")
        return None

def get_or_create_statistics_file():
    filename = "Statistics.json"
    try:
        # Check if the file exists
        with open(filename, "r"):
            pass  # File exists
    except FileNotFoundError:
        # File doesn't exist, create it
        with open(filename, "w") as file:
            pass  # Create an empty file

    return filename


def read_gym_info(filename="GymInfo.txt"):
    try:
        with open(filename, "r") as file:
            gym_info = file.read().strip()  # Read the content and remove leading/trailing spaces
            return gym_info
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return None

def get_camera_number(source_filename):
    # Extract the camera number from the source filename
    # Assuming the format is SOMETHING_camera(NUM).filetype
    parts = os.path.splitext(os.path.basename(source_filename))[0].split("_")
    camera_number = parts[-1]  # The last part should be the camera number
    return camera_number
