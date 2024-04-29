##Creating Function Definitions for Statistics Creation
import numpy as np
from scipy.signal import savgol_filter
import json

def StartingClimb(bboxData, keypoints, RouteID):
    #calculate which route climber establishes on,
    #when both hands are on one colorset for a route (bboxes in matching holds)

    start_holds = []

    if "starthold" in  bboxData["objects"]:
        #identify where startingHolds are
        for obj in bbox_data["objects"]:
            route_id = obj["route_id"]
            if (route_id == RouteID) and (obj["starthold"] is True):
                start_holds.append(obj)

        #get hand Positions
        effector_positions = []
        effector_nums = [9, 10] #LH, RH
        for effector_num in effector_nums:
            effector_positions.append(get_all_end_effectors(keypoints, effector_num, steps))

        effectorStartingFrames = []

        # Initialize a dictionary to track the last frame each hand was in a start hold
        last_frame_hand1_in_start_hold = {}
        last_frame_hand2_in_start_hold = {}

        # Iterate through the frames
        for framecounter, (effector_position1, effector_position2) in enumerate(zip(*effector_positions), start=1):
            hand1_in_start_hold = False
            hand2_in_start_hold = False
            
            # Check if either hand is in any of the start holds
            for obj in start_holds:
                if pointInBox(effector_position1, obj["bbox"]):
                    hand1_in_start_hold = True
                    last_frame_hand1_in_start_hold[obj["id"]] = framecounter
                if pointInBox(effector_position2, obj["bbox"]):
                    hand2_in_start_hold = True
                    last_frame_hand2_in_start_hold[obj["id"]] = framecounter
            
            # If both hands are in start holds within 3 frames of each other, record the frame
            if hand1_in_start_hold and hand2_in_start_hold:
                for obj_id in last_frame_hand1_in_start_hold:
                    if obj_id in last_frame_hand2_in_start_hold:
                        frame_diff = abs(last_frame_hand1_in_start_hold[obj_id] - last_frame_hand2_in_start_hold[obj_id])
                        if frame_diff <= 3:
                            median_frame = (last_frame_hand1_in_start_hold[obj_id] + last_frame_hand2_in_start_hold[obj_id]) // 2
                            effectorStartingFrames.append(median_frame)

        if len(effectorStartingFrames) > 1: #removes outliers and finds singular median frame for climb starting
            mean_frame = sum(sorted(effectorStartingFrames)[len(effectorStartingFrames) // 20:-len(effectorStartingFrames) // 20]) // len(effectorStartingFrames)
            return int(mean_frame)
        else:
            return int(effectorStartingFrames[0])
            

    else:
        return 0

def cutFrames(original_dict, x):
    modified_dict = {key: value for key, value in original_dict.items() if int(key.split("_")[1]) >= x}
    return modified_dict


#####################################################################################################################

def recordAttempt(database, numeric_climber_id, route_id, outcome, date, gymID, grade):
    # Log for the climber, which route, Success or fail / Increment Attempts

    sessionID = get_session_id(database, numeric_climber_id, date, gymID)

    if numeric_climber_id is not None:
        if "Climbers" in database:
            existing_climber_ids = {climber["ID"] for climber in database["Climbers"]}
            if numeric_climber_id in existing_climber_ids:
                # Update existing climber's data
                for climber in database["Climbers"]:
                    if climber["ID"] == str(numeric_climber_id):
                        sessions = list(climber["sessions:"].keys())
                        if str(sessionID) in list(climber["sessions:"].keys()):
                            route_data = climber["sessions:"][str(sessionID)]["routes"].get(str(route_id))
                            if route_data:
                                route_data["attempts"] += 1
                                if outcome == "success":
                                    route_data["successes"] += 1
                            else:
                                climber["sessions:"][str(sessionID)]["routes"][route_id] = {
                                    "Grade": grade,
                                    "attempts": 1,
                                    "successes": 1 if outcome == "success" else 0
                                }
                        else:
                            climber["sessions:"][sessionID] = {
                                "Date": date,
                                "GymID": gymID,
                                "routes": {
                                    route_id: {
                                        "Grade": grade,
                                        "attempts": 1,
                                        "successes": 1 if outcome == "success" else 0
                                    }
                                }
                            }
                        break
            else:
                # New climber
                database["Climbers"].append({
                    "ID": str(numeric_climber_id),
                    "sessions:": {
                        sessionID: {
                            "Date": date,
                            "GymID": gymID,
                            "routes": {
                                route_id: {
                                    "Grade": grade,
                                    "attempts": 1,
                                    "successes": 1 if outcome == "success" else 0
                                }
                            }
                        }
                    }
                })
        else:
            # Initialize climber's data
            database["Climbers"] = [
                {
                    "ID": str(numeric_climber_id),
                    "sessions:": {
                        sessionID: {
                            "Date": date,
                            "GymID": gymID,
                            "routes": {
                                route_id: {
                                    "Grade": grade,
                                    "attempts": 1,
                                    "successes": 1 if outcome == "success" else 0
                                }
                            }
                        }
                    }
                }
            ]
    else:
        print("Invalid Climber ID format.")

    with open("Statistics.json", "w") as statistics_file:
        json.dump(database, statistics_file, indent=4)


def get_session_id(database, climber_id, date, gymID):
    if "Climbers" in database:
        for climber in database["Climbers"]:
            if climber["ID"] == str(climber_id):
                for sessionID, session_data in climber.get("sessions:", {}).items():
                    if session_data.get("Date") == date and session_data.get("GymID") == gymID:
                        return sessionID

        # No matching session found, calculate the next session ID
        existing_session_ids = [int(sessionID) for sessionID in climber.get("sessions:", {})]
        next_session_id = max(existing_session_ids, default=0) + 1
        return str(next_session_id)
    else:
        # Initialize climber's data
        return "1"  # Default session ID if no climber data exists



######################################################################################################################
    
def routeGrade(bbox_data, route_id):
    for obj in bbox_data:
        if obj.get("route_id") == route_id:
            return obj.get("grade")
    return None

######################################################################################################################

def finishRoute(bboxData, keypoints, RouteID):
    #check 2 hands match on final hold of the route,
    effector_positions = []
    steps = 3
    effector_nums = [9, 10] #LH, RH
    for effector_num in effector_nums:
        effector_positions.append(get_all_end_effectors(keypoints, effector_num, steps))

    Outcome = {
        "finish_route": False,
        "dab": False}
    
    dab = checkDab(bboxData, effector_positions, RouteID)#check time on other holds... might want changing to movement based

    if dab:
       Outcome["dab"] = True 
    
    top_hold_bbox = findTopHold(bboxData, RouteID) #find top hold of route

    print("top_hold_bbox", top_hold_bbox)
    for effector_position1, effector_position2 in zip(*effector_positions): #check top hold is touched with two hands
        if (pointInBox(effector_position1, top_hold_bbox)) or (pointInBox(effector_position1, top_hold_bbox)):
            Outcome["finish_route"] = True

    return Outcome
            

def findTopHold(bboxData, RouteID):
    #Finds the Top hold of any given route
    highest_bbox = float('inf')

    top_hold = []

    print(RouteID)

    for obj in bboxData["objects"]:
        route_id = obj["route_id"]
        x_min, y_min, x_max, y_max = obj["bbox"]
        if (route_id == RouteID) and (y_min < highest_bbox):
            highest_bbox = y_min
            top_hold = (x_min, y_min, x_max, y_max)
        
    return top_hold

def checkDab(bboxData, effector_positions, RouteID):

    #movement based approach could be more appropriate, detect when significant sike in movement is as a reach for hold, then detect from there.
    touched_holds_density = {}
    for effector_position1, effector_position2 in zip(*effector_positions):
        for obj in bboxData["objects"]:
            route_id = obj["route_id"]
            if pointInBox(effector_position1, obj["bbox"]): # calculate number of frames touching each type of hold
                touched_holds_density[route_id] = touched_holds_density.get(route_id, 0) + 1

    total_touched_holds = sum(touched_holds_density.values())
    for route in touched_holds_density:
        if (route != RouteID) and (touched_holds_density[route] > (total_touched_holds/3)):
            return True
        else:
            return False

                

######################################################################################################################

def identifyRoute(bboxData, keypoints):
    #For Climb, identify which route the climber is on

    #Simplest way to do this is figure out which routes the climbers hands spend the most time in.
    steps = 3
    effector_nums = [9, 10, 15, 16] #LH, RH, LF, RF

    #keypoints = keypoints[7:].T

    # get effector_positions for all frames:
    effector_positions = []
    for effector_num in effector_nums:
        effector_positions.append(get_all_end_effectors(keypoints, effector_num, steps))            
    
    # then check for each position if contained in bounding box

    id_counts = {}

    #print(effector_positions)
    
    for effector in effector_positions:
        for effector_position in effector:
            for obj in bboxData["objects"]:
                #print(effector_position)
                if pointInBox(effector_position, obj["bbox"]): #return true if end effector is in bbox.
                    #print("effector in bbox", obj["color"])
                    id_counts[obj["route_id"]] = id_counts.get(obj["route_id"], 0) + 1

    max_id = max(id_counts, key=id_counts.get)

    return max_id

def pointInBox(point, box):
    x, y = point
    x_min, y_min, x_max, y_max = box
    return x_min <= x <= x_max and y_min <= y <= y_max     
    
######################################################################################################################

def detectClimbs(Keypoints): ##effectively fall calculation - finds when all end effectors are moving downwards
    steps = 3
    labels = ['LH', 'RH', 'LF', 'RF']
    all_smoothed_heights = {label: [] for label in labels}
    effector_nums = [9, 10, 15, 16]  # LH, RH, LF, RF
    threshold = 3
    consecutive_frames = 3
    
    for i, effector_num in enumerate(effector_nums):
        effector_positions = get_all_end_effectors(Keypoints, effector_num, steps) ##finds all end effectors for all frames
        heights = np.array([y for x, y in effector_positions])
        smoothed_heights = smooth_heights(heights, window_length=5, polyorder=2) ## smooths effector positions for fall calculation
        all_smoothed_heights[labels[i]] = smoothed_heights

    #print(all_smoothed_heights)
    fall_frames = identify_falls(all_smoothed_heights, threshold, consecutive_frames) #find frames of significant drops

    #print(fall_frames)

    max_frames = len(Keypoints)
    print("maxframes", max_frames)
    
    frame_ranges = [[0, fall_frames[0]] if fall_frames else [0, max_frames]] #set range to maxframes if no falls found
    for i in range(len(fall_frames) - 1): #convert falling frames to ranges of a climbattempt
        frame_ranges.append([fall_frames[i], fall_frames[i + 1]])

    if not(max_frames in frame_ranges[-1]):
        frame_ranges.append([frame_ranges[-1][1], max_frames]) ##appends to end of video to account for any climbs that may happen then footage stops before fall.

    return frame_ranges

def get_all_end_effectors(kpts, effector_num, steps):
    effector_positions = []
    for frame, keypoints in kpts.items():
        keypoints_np = np.array(keypoints)
        keypoints_np = keypoints_np[7:].T
        if keypoints_np.size > 0:
            x_coord, y_coord = keypoints_np[steps * effector_num], keypoints_np[steps * effector_num + 1]
            effector_positions.append((x_coord, y_coord))
        else:
            effector_positions.append((None, None))
    return effector_positions

# Function to smooth the end effector height data using Savitzky-Golay filter
def smooth_heights(all_heights, window_length, polyorder):
    smoothed_heights = savgol_filter(all_heights, window_length, polyorder, axis=0)
    return smoothed_heights


def identify_falls(all_smoothed_heights, threshold = 10, consecutive_frames = 10):
    drops = {}
    currentdrops = []
    labels = []
    for array in all_smoothed_heights:
        labels.append(array)
        #print(array)
        for i in range(1, len(all_smoothed_heights[array]) - consecutive_frames + 1):
            if all(all_smoothed_heights[array][j-1] - all_smoothed_heights[array][j] > threshold for j in range(i, i + consecutive_frames)):
                currentdrops.append(i) #If notable drop then append
        drops[array] = currentdrops
        currentdrops = []
        #print(drops)
    
    bodyDrop = []
    for counter, array in enumerate(drops):
        for i in range(0, len(drops[array])):
            store = 0
            for k in range(len(labels)):
                for j in range(0, len(drops[labels[(counter+1+k)%len(labels)]])):
                    if is_within_range(drops[array][i], drops[labels[(counter+1+k)%len(labels)]][j], 10):
                        store = store + 1
                        break
            if store >= len(labels):
                bodyDrop.append(drops[array][i])

    bodyDrop = group_close_numbers(bodyDrop)
    
    return bodyDrop

def is_within_range(value1, value2, x):
    absolute_difference = abs(value1 - value2)
    return absolute_difference <= x

def group_close_numbers(numbers, threshold=10):

    # Sort the list
    sorted_numbers = sorted(numbers)
    
    # Initialize variables
    grouped_numbers = []
    try:
        current_group = [sorted_numbers[0]]
        
        # Iterate through the sorted list
        for i in range(1, len(sorted_numbers)):
            if sorted_numbers[i] - current_group[-1] <= threshold:
                # Numbers are close, add to the current group
                current_group.append(sorted_numbers[i])
            else:
                # Numbers are not close, calculate average and add to grouped_numbers
                average = sum(current_group) / len(current_group)
                grouped_numbers.append(average)
                current_group = [sorted_numbers[i]]
        
        # Add the last group
        average = sum(current_group) / len(current_group)
        grouped_numbers.append(average)
    except:
        grouped_numbers = []
    
    return grouped_numbers



