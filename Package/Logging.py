from utilities import *
import json
from datetime import datetime

def load_keypoints(filename):
    with open(filename) as keypoints_file:
        return json.load(keypoints_file)

def load_bboxes(filename):
    with open(filename) as bboxes_file:
        return json.load(bboxes_file)

def load_statistics(filename):
    try:
        with open(filename, "r") as statistics_file:
            return json.load(statistics_file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, initialize an empty dictionary
        return {}




parser = argparse.ArgumentParser(description="Process keypoints, bounding boxes, and statistics.")
parser.add_argument("keypoints_file", help="Path to the keypoints JSON file")
parser.add_argument("bboxes_file", help="Path to the bounding boxes JSON file")
parser.add_argument("statistics_file", help="Path to the statistics JSON file")
parser.add_argument("gymID", help="Name of the Gym")

args = parser.parse_args()

keypoints_data = load_keypoints(args.keypoints_file)
bbox_data = load_bboxes(args.bboxes_file)
statistics = load_statistics(args.statistics_file)

date = datetime.now().strftime("%m/%d/%y")
sessionID = 1 #create a sessionID (will be linked to Date etc,

gymID = args.gymID

for person in keypoints_data: #need to identify person in Pose estimation JSON Creation
    

    ClimbAttempts = detectClimbs(keypoints_data[person])

    print(ClimbAttempts)

    for attempt in ClimbAttempts:
        ##attempt outputs the frame range for the attempt like [0, 130] or [130, 200]

        print("Attempt", attempt)

        person_attempt = {frame_name: bbox_data for frame_name, bbox_data in keypoints_data[person].items()
                          if attempt[0] <= int(frame_name.split('_')[1]) <= attempt[1]}
        #person_attempt contains the absolute keypoints for the climber within the attempt range

        #determine the route that's being climbed
        route_id = identifyRoute(bbox_data, person_attempt)

        print("Route Identified", route_id)

        Starting_route_frame = StartingClimb(bbox_data, person_attempt, route_id)
        
        person_attempt_trimmed = cutFrames(person_attempt, Starting_route_frame)

        print("Start of Route identified")

        #probably no need to run each of these sequentially... Will see on computation time...

        route_outcome = finishRoute(bbox_data, person_attempt_trimmed, route_id)

        print("Outcome Calculated", route_outcome)

        recordAttempt(statistics, person, route_id, 'success', date, gymID)
        
        recordAttempt(statistics, person, 3, 'success', date, gymID)

        if route_outcome["finish_route"]:
            if route_outcome["dab"]: 
                recordAttempt(statistics, person, route_id, 'dab', date, gymID)
            else:
                recordAttempt(statistics, person, route_id, 'success', date, gymID)

        else:
            recordAttempt(statistics, person, route_id, 'fail', date, gymID)

        print("outcome Recorded")
            

#Thats it!
