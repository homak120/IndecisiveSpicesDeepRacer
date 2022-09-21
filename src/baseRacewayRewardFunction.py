import math
def reward_function(params):

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params["speed"]
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    progress = params['progress']
    is_crashed = params['is_crashed']
    is_offtrack = params['is_offtrack']
    is_reversed = params['is_reversed']
    steps = params['steps']
    x = params['x']
    y = params['y']
    is_left_of_center = params['is_left_of_center']
    
    reward=0
    
    # Control panel
    POSITION_REWARD_RATE = 0.3
    RIGHT_SIDE_REWARD_RATE = 0.3
    CENTER_DIST_REWARD_RATE = 0.3
    SPEED_REWARD_RATE = 0.8
    ADDITIONAL_SPEED_RATE = 0
    DIRECTION_REWARD_RATE = 0.3
    PROGRESS_REWARD_RATE = 0.5
    STEP_REWARD_RATE = 2.0
    
    HUNDRED_TEN_BASE = 1.584893192461113
    HUNDRED_TEN_POWER = 10
    HUNDRED_EIGHT_BASE = 1.778279410038923
    HUNDRED_EIGHT_POWER = 8
    HUNDRED_SIX_BASE = 2.1544346900318843
    HUNDRED_SIX_POWER = 6
    HUNDRED_FOUR_BASE = 3.162277660168379
    HUNDRED_FOUR_POWER = 4
    HUNDRED_TWO_BASE = 10
    HUNDRED_TWO_POWER = 2

##### START: SPEED REWARD #####
    # Power base speed reword calculatiomn
    speedRewardBase = HUNDRED_FOUR_BASE
    speedRewardPower = HUNDRED_FOUR_POWER
    targetSpeed = 4
    speedReward = 0
    if abs(targetSpeed - speed) < 2:
        speedReward=((1-abs(targetSpeed - speed)/2)*speedRewardBase)**speedRewardPower
##### END: SPEED REWARD #####

##### START: CENTER DISTANCE REWARD #####
    centerDistReward = 0
    centerDistRewardBase = HUNDRED_TWO_BASE
    centerDistRewardPOWER = HUNDRED_TWO_POWER
    centerDistReward = ((1 - distance_from_center/(track_width/2))*centerDistRewardBase)**centerDistRewardPOWER
##### END: CENTER DISTANCE REWARD #####

##### START: DIRECTION REWARD #####
    # Calculate the direction of the center line based on the closest waypoints
    directionReward = 0
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
       
    # power base reward for angle difference
    directionBase = HUNDRED_TEN_BASE
    directionPower = HUNDRED_TEN_POWER
    if direction_diff < 15:
        directionReward=((1-direction_diff/15)*directionBase)**directionPower
##### END: DIRECTION REWARD #####

##### START: Progress reward #####
    progressBase = HUNDRED_FOUR_BASE
    progressPower = HUNDRED_FOUR_POWER
    progressReward = ((progress/100)*progressBase)**progressPower
##### END: Progress reward #####

##### START: STEP REWARD #####
    # Total num of steps we want the car to finish the lap, it will vary depends on the track length
    stepRewardFactor = 0
    baseNumSteps = 400
    if (steps < baseNumSteps):
        stepsProgress = (steps / baseNumSteps) * 100
        stepRewardFactor = progress - stepsProgress
    
##### END: STEP REWARD #####

    reward= SPEED_REWARD_RATE*speedReward + DIRECTION_REWARD_RATE*directionReward + CENTER_DIST_REWARD_RATE*centerDistReward + (progressReward*PROGRESS_REWARD_RATE)**stepRewardFactor
        
    if is_crashed or is_offtrack or is_reversed:
        reward = 0

    is_left_of_center_ind = 0
    if is_left_of_center:
        is_left_of_center_ind = 1
        

    print('SIM_DATA_LOG:', x, ',', y, ',', heading, ',', speed, ',', distance_from_center, ',', is_left_of_center_ind, ',', closest_waypoints[1], ',', steps)
    print('steps: ', steps)
    print('progress: ', progress)
    print('closest_waypoints: ', closest_waypoints)
    print('track_width: ', track_width)
    print('waypoints: ', waypoints)
    print('x: ', x)
    print('y: ', y)
    print('speed: ', speed)
    print('is_offtrack: ', is_offtrack)
    print('is_left_of_center', is_left_of_center)
    print('distance_from_center', distance_from_center)
    print('speedReward: ', speedReward)
    print('progressReward: ', progressReward)
    
    print('stepRewardFactor: ', stepRewardFactor)
    print('reward: ', reward)
    
    return float(reward)