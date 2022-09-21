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
    POSITION_REWARD_RATE = 0.9
    SPEED_REWARD_RATE = 0.9
    ADDITIONAL_SPEED_RATE = 0
    DIRECTION_REWARD_RATE = 0.2
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

##### START: Ideal Route Data Map #####
    dataMap = [
        [-2.036935985,-5.94333601,0,4,0.2,0,0,0,0,0,0],
        [-1.738064468,-5.989463568,1,4,0.2,0,0,0,0,0,0],
        [-1.4393695,-6.036723137,2,4,0.2,0,0,0,0,0,0],
        [-1.140888035,-6.085307598,3,4,0.3,0,0,0,0,0,0],
        [-0.8426246047,-6.135216951,4,4,0.4,0,0,1,0.9,0.9,0.2],
        [-0.5444198996,-6.185476542,5,4,0.4,0,0,1,0.9,0.9,0.2],
        [-0.2462899014,-6.236176491,6,4,0.4,0,0,1,0.9,0.9,0.2],
        [0.05152494833,-6.28869009,7,4,0.45,0,1,1,0.9,0.9,0.2],
        [0.3483338952,-6.346576452,8,3.8,0.45,0,1,1,0.9,0.9,0.2],
        [0.643691808,-6.41149354,9,3.8,0.45,0,1,1,0.9,0.9,0.2],
        [0.9376374185,-6.482528448,10,3.8,0.45,0,1,1,0.9,0.9,0.2],
        [1.230414033,-6.55824995,11,3.6,0.45,0,1,1,0.9,0.9,0.2],
        [1.525754511,-6.622694016,12,3.6,0.45,0,1,1,0.9,0.9,0.2],
        [1.827323496,-6.639290571,13,3.6,0.45,0,1,1,0.9,0.9,0.2],
        [2.128892899,-6.618226051,14,3.2,0.2,0,0,0,0,0,0],
        [2.42604804,-6.563058615,15,3.1,0.1,0,0,0,0,0,0],
        [2.71370995,-6.470383883,16,2.8,0.1,1,0,0,0,0,0],
        [2.986755013,-6.340842009,17,2.5,0.1,1,0,0,0,0,0],
        [3.239823461,-6.175666332,18,2.8,0.2,1,0,0,0,0,0],
        [3.472265482,-5.982369661,19,3.2,0.2,1,0,0,0,0,0],
        [3.693007469,-5.775682926,20,4,0.3,1,0,0,0,0,0],
        [3.90444684,-5.559537411,21,4,0.3,1,0,0,0,0,0],
        [4.102475524,-5.331040382,22,4,0.4,1,0,0,0,0,0],
        [4.286980987,-5.091476917,23,4,0.4,1,0,0,0,0,0],
        [4.468530416,-4.849627495,24,3.5,0.45,1,1,0,0,0,0],
        [4.643745899,-4.603174448,25,3.5,0.45,1,1,0,0,0,0],
        [4.799426556,-4.344087601,26,3.5,0.45,1,1,0,0,0,0],
        [4.913359404,-4.064393044,27,3.5,0.4,1,0,0,0,0,0],
        [4.97567606,-3.768771529,28,3.8,0.4,1,0,0,0,0,0],
        [4.990587473,-3.466975451,29,4,0.4,1,0,0,0,0,0],
        [4.966310501,-3.165669084,30,3.8,0.3,1,0,0,0,0,0],
        [4.918224096,-2.867137551,31,3.8,0.2,1,0,0,0,0,0],
        [4.859284401,-2.570557475,32,3.2,0.1,1,0,0,0,0,0],
        [4.77715683,-2.279561996,33,3.2,0.1,0,0,0,0,0,0],
        [4.701304913,-1.986860037,34,3.2,0.2,0,0,0,0,0,0],
        [4.636876106,-1.691394508,35,3.5,0.3,0,0,0,0,0,0],
        [4.577201366,-1.394939482,36,3.5,0.3,0,0,1,0.9,0.9,0.2],
        [4.53563714,-1.095528007,37,3.5,0.4,0,0,1,0.9,0.9,0.2],
        [4.543611526,-0.7937583029,38,3,0.4,0,1,1,0.9,0.9,0.2],
        [4.607089043,-0.4983371496,39,2.5,0.45,0,1,1,0.9,0.9,0.2],
        [4.716185093,-0.2165487404,40,2.5,0.4,0,1,1,0.9,0.9,0.2],
        [4.864802122,0.04658450186,41,2.7,0.3,0,0,1,0.9,0.9,0.2],
        [5.046972513,0.2877318002,42,2.7,0.3,0,0,1,0.9,0.9,0.2],
        [5.259093523,0.5029039569,43,2.8,0.3,0,0,0,0,0,0],
        [5.259093523,0.5029039569,44,3,0.2,0,0,0,0,0,0],
        [5.5010674,0.6839075387,45,3.1,0.1,0,0,0,0,0,0],
        [5.762109518,0.8364308476,46,3.1,0.1,0,0,0,0,0,0],
        [6.030410528,0.9759470522,47,3.1,0.1,1,0,0,0,0,0],
        [6.306141853,1.099986523,48,3.1,0.1,1,0,0,0,0,0],
        [6.591607571,1.199551553,49,3.2,0.2,1,0,0,0,0,0],
        [6.881825924,1.284536928,50,3.5,0.3,1,0,0,0,0,0],
        [7.158332348,1.405496091,51,3.5,0.4,1,0,0,0,0,0],
        [7.401469946,1.584732473,52,3,0.4,1,1,1,0.9,0.9,0.2],
        [7.611213923,1.802215993,53,2.5,0.45,1,1,1,0.9,0.9,0.2],
        [7.785490274,2.049084544,54,2.4,0.45,1,1,1,0.9,0.9,0.2],
        [7.923514366,2.31792593,55,2.5,0.45,1,1,1,0.9,0.9,0.2],
        [8.02316308,2.603202939,56,2.5,0.4,1,1,1,0.9,0.9,0.2],
        [8.08055234,2.899960518,57,2.6,0.3,1,0,0,0,0,0],
        [8.094262838,3.201897502,58,2.6,0.3,1,0,0,0,0,0],
        [8.06656909,3.50287509,59,2.6,0.2,1,0,0,0,0,0],
        [8.00179553,3.798136473,60,2.7,0.1,1,0,0,0,0,0],
        [7.905530453,4.084710479,61,2.7,0.1,0,0,0,0,0,0],
        [7.786100864,4.362487555,62,2.6,0.2,0,0,0,0,0,0],
        [7.64009738,4.627154589,63,2.6,0.2,0,0,0,0,0,0],
        [7.465439081,4.873879671,64,2.5,0.3,0,0,0,0,0,0],
        [7.268836498,5.103580952,65,2.5,0.3,0,0,0,0,0,0],
        [7.060459852,5.322726965,66,2.4,0.3,0,0,0,0,0,0],
        [6.847865343,5.537786961,67,2.4,0.4,0,0,0,0,0,0],
        [6.625417471,5.74258709,68,2.5,0.4,0,0,0,0,0,0],
        [6.388648033,5.930606127,69,2.6,0.4,0,0,0,0,0,0],
        [6.136788607,6.097854376,70,2.8,0.4,0,0,0,0,0,0],
        [5.870970011,6.241891384,71,3.2,0.4,0,0,0,0,0,0],
        [5.593230009,6.361319065,72,3.2,0.4,0,0,0,0,0,0],
        [5.305620432,6.454447985,73,3.8,0.4,0,0,0,0,0,0],
        [5.010941505,6.522075415,74,3.8,0.4,0,0,0,0,0,0],
        [4.712703943,6.572042465,75,4,0.3,0,0,0,0,0,0],
        [4.412917376,6.611585617,76,4,0.3,0,0,0,0,0,0],
        [4.111389875,6.634212017,77,3.8,0.3,0,0,0,0,0,0],
        [3.809063077,6.639834404,78,3.8,0.3,0,0,0,0,0,0],
        [3.506811023,6.630667686,79,3.5,0.3,0,0,0,0,0,0],
        [3.204898953,6.613333941,80,3.5,0.3,0,0,0,0,0,0],
        [2.903116941,6.593855381,81,3.3,0.2,0,0,0,0,0,0],
        [2.601729989,6.569056511,82,3.3,0.2,0,0,0,0,0,0],
        [2.301701546,6.531422138,83,3.3,0.1,0,0,0,0,0,0],
        [2.005920529,6.468984127,84,3.3,0.1,1,0,0,0,0,0],
        [1.721157551,6.367913961,85,3.5,0.1,1,0,0,0,0,0],
        [1.456016958,6.222998619,86,3.6,0.1,1,0,0,0,0,0],
        [1.228810847,6.02520442,87,3.6,0.1,1,0,0,0,0,0],
        [1.032373101,5.795286894,88,3.6,0.1,0,0,0,0,0,0],
        [0.8291173726,5.571383476,89,3.6,0.1,0,0,0,0,0,0],
        [0.6197642162,5.353159904,90,3.6,0.1,0,0,0,0,0,0],
        [0.4078982221,5.13737154,91,3.8,0.1,0,0,0,0,0,0],
        [0.1942995638,4.923299313,92,4,0.1,0,0,0,0,0,0],
        [-0.02390980721,4.713939905,93,4,0.1,0,0,0,0,0,0],
        [-0.2506375387,4.513866901,94,4,0.2,0,0,0,0,0,0],
        [-0.4888878092,4.327690601,95,4,0.2,0,0,0,0,0,0],
        [-0.7386728525,4.157300591,96,4,0.2,0,0,0,0,0,0],
        [-0.9981980324,4.002122879,97,3.6,0.2,0,0,0,0,0,0],
        [-1.265850008,3.861425996,98,3.6,0.2,0,0,0,0,0,0],
        [-1.540815532,3.735619545,99,3.5,0.3,0,0,0,0,0,0],
        [-1.822248518,3.625038624,100,3.5,0.3,0,0,0,0,0,0],
        [-2.109308064,3.530017376,101,4,0.4,0,0,0,0,0,0],
        [-2.401389003,3.451795459,102,4,0.4,0,0,0,0,0,0],
        [-2.697199583,3.389089465,103,4,0.4,0,0,0,0,0,0],
        [-2.995718002,3.340865493,104,3.8,0.4,0,0,0,0,0,0],
        [-3.296191573,3.306867003,105,3.6,0.4,0,0,0,0,0,0],
        [-3.597955942,3.287316442,106,3.6,0.3,0,0,0,0,0,0],
        [-3.900317073,3.285915017,107,3.6,0.2,0,0,0,0,0,0],
        [-4.201757431,3.309132457,108,3.8,0.2,0,0,0,0,0,0],
        [-4.501722574,3.347500086,109,3.8,0.1,0,0,0,0,0,0],
        [-4.803642988,3.36053443,110,3.8,0.1,0,0,0,0,0,0],
        [-5.104934931,3.335668445,111,3.8,0.1,1,0,0,0,0,0],
        [-5.403936625,3.29065454,112,3.8,0.1,1,0,0,0,0,0],
        [-5.698654652,3.223231435,113,3.5,0.2,1,0,0,0,0,0],
        [-5.985719681,3.128429532,114,3.5,0.2,1,0,0,0,0,0],
        [-6.261255026,3.004058003,115,3.5,0.3,1,0,0,0,0,0],
        [-6.521104574,2.8495574,116,3.5,0.3,1,0,0,0,0,0],
        [-6.761330843,2.666049957,117,3.7,0.4,1,0,0,0,0,0],
        [-6.978301525,2.455597043,118,3.7,0.4,1,0,0,0,0,0],
        [-7.168851852,2.220948994,119,3.7,0.4,1,0,0,0,0,0],
        [-7.333338976,1.967303514,120,3.7,0.4,1,0,0,0,0,0],
        [-7.476794481,1.701131523,121,3.7,0.4,1,0,0,0,0,0],
        [-7.608717442,1.429019988,122,4,0.3,1,0,0,0,0,0],
        [-7.726512909,1.15054673,123,4,0.3,1,0,0,0,0,0],
        [-7.825145006,0.8647176027,124,4,0.3,1,0,0,0,0,0],
        [-7.905004263,0.5730820894,125,4,0.2,1,0,0,0,0,0],
        [-7.967764854,0.2772855014,126,4,0.2,1,0,0,0,0,0],
        [-8.01783371,-0.02094178274,127,4,0.2,1,0,0,0,0,0],
        [-8.057097673,-0.320769608,128,4,0.1,1,0,0,0,0,0],
        [-8.082846403,-0.6220587492,129,4,0.1,0,0,0,0,0,0],
        [-8.094869852,-0.9242066741,130,4,0.1,0,0,0,0,0,0],
        [-8.093004942,-1.226586998,131,4,0.1,1,0,0,0,0,0],
        [-8.080519199,-1.528728008,132,3.8,0.1,1,0,0,0,0,0],
        [-8.055050611,-1.830036521,133,3.8,0.1,1,0,0,0,0,0],
        [-8.013290405,-2.129516959,134,3.7,0.1,1,0,0,0,0,0],
        [-7.954392672,-2.42610395,135,3.7,0.1,1,0,0,0,0,0],
        [-7.878217459,-2.718727946,136,3.5,0.1,1,0,0,0,0,0],
        [-7.788170099,-3.007396936,137,3.5,0.2,1,0,0,0,0,0],
        [-7.681349277,-3.2902565,138,3.2,0.3,1,0,0,0,0,0],
        [-7.555041313,-3.564965487,139,3.2,0.3,1,0,0,0,0,0],
        [-7.409707546,-3.83010745,140,3.2,0.3,1,0,0,0,0,0],
        [-7.250068665,-4.086897612,141,3.2,0.4,1,0,0,0,0,0],
        [-7.071657419,-4.330975056,142,3.2,0.4,1,0,0,0,0,0],
        [-6.872511625,-4.558440447,143,3.5,0.3,1,0,0,0,0,0],
        [-6.653365612,-4.766705036,144,3.5,0.2,1,0,0,0,0,0],
        [-6.415413618,-4.953125477,145,3.5,0.1,1,0,0,0,0,0],
        [-6.161219597,-5.116795778,146,3.5,0.1,0,0,0,0,0,0],
        [-5.894645929,-5.259450912,147,3.7,0.1,0,0,0,0,0,0],
        [-5.617578506,-5.38043952,148,4,0.2,0,0,0,0,0,0],
        [-5.328897953,-5.469967604,149,4,0.2,0,0,0,0,0,0],
        [-5.03255558,-5.529980421,150,4,0.2,0,0,0,0,0,0],
        [-4.733617067,-5.575635433,151,4,0.2,0,0,0,0,0,0],
        [-4.433925629,-5.616093159,152,4,0.2,0,0,0,0,0,0],
        [-4.134026527,-5.654986858,153,4,0.2,0,0,0,0,0,0],
        [-3.834110022,-5.693745136,154,4,0.2,0,0,0,0,0,0],
        [-3.534282565,-5.733186007,155,4,0.2,0,0,0,0,0,0],
        [-3.23450458,-5.772996426,156,4,0.2,0,0,0,0,0,0],
        [-2.934818506,-5.813499451,157,4,0.2,0,0,0,0,0,0],
        [-2.635298491,-5.855208635,158,4,0.2,0,0,0,0,0,0],
        [-2.335991502,-5.898420095,159,4,0.2,0,0,0,0,0,0],
        [-2.036935985,-5.94333601,160,4,0.2,0,0,0,0,0,0]
    ]

    # Find the closet data point
    closeDataPointPositionDist = 9999
    closeDataPointPositionSpeed = 4
    closeDataPointPositionCenterDiff = 0
    closeDataPointPositionIsLeftInd = -1
    ignoreOffTrackInd = 0
    overwriteRewardRateInd = 0
    for eachData in dataMap:
        x2 = eachData[0]
        y2 = eachData[1]
        positionDist = math.sqrt((x2 - x)**2 + (y2 - y)**2)
        if positionDist < closeDataPointPositionDist:
            ignoreOffTrackInd = eachData[6]
            overwriteRewardRateInd = eachData[7]
            overwritePositionRate = eachData[8]
            overwriteSpeedRate = eachData[9]
            overwriteDirectionRate = eachData[10]
            closeDataPointPositionDist = positionDist
            closeDataPointPositionSpeed = eachData[3]*(1 + ADDITIONAL_SPEED_RATE)
            if (closeDataPointPositionSpeed > 4):
                closeDataPointPositionSpeed = 4
            closeDataPointPositionCenterDiff = eachData[4]*track_width
            closeDataPointPositionIsLeftInd = eachData[5]
##### END: Ideal Route Data Map #####

##### START:  Overwrite reward rates #####
    if (overwriteRewardRateInd == 1):
        POSITION_REWARD_RATE = overwritePositionRate
        SPEED_REWARD_RATE = overwriteSpeedRate
        DIRECTION_REWARD_RATE = overwriteDirectionRate
##### END:  Overwrite reward rates #####


##### START: POSITION REWARD #####
    # Reward for closing to the center line and Initial reward
    #centerDistRewardBase =  HUNDRED_SIX_BASE
    #centerDistRewardPower = HUNDRED_SIX_POWER
    #positionReward = ((1 - (distance_from_center / (track_width/2)))*centerDistRewardBase)**centerDistRewardPower
    
    positionDistRewardBase =  HUNDRED_TWO_BASE
    positionDistRewardPower = HUNDRED_TWO_POWER
    positionReward = (((1 - (closeDataPointPositionDist / track_width))*positionDistRewardBase)**positionDistRewardPower)/2
    if (is_left_of_center and closeDataPointPositionIsLeftInd == 1) or (not is_left_of_center and closeDataPointPositionIsLeftInd == 0):
        positionReward = (((1 - abs(closeDataPointPositionCenterDiff - distance_from_center) / (track_width / 2))*positionDistRewardBase)**positionDistRewardPower)/2
        positionReward+=50
        
##### END: POSITION REWARD #####
    
##### START: SPEED REWARD #####
    # Power base speed reword calculatiomn
    speedRewardBase = HUNDRED_EIGHT_BASE
    speedRewardPower = HUNDRED_EIGHT_POWER
    targetSpeed = closeDataPointPositionSpeed
    if (speed > targetSpeed):
        speedReward=speedRewardBase**speedRewardPower
    else:
        speedReward=((1-(targetSpeed - speed)/targetSpeed)*speedRewardBase)**speedRewardPower
##### END: SPEED REWARD #####
        
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
    progressBase = HUNDRED_TEN_BASE
    progressPower = HUNDRED_TEN_POWER
    progressReward = ((progress/100)*progressBase)**progressPower
##### END: Progress reward #####

##### START: STEP REWARD #####
    # Total num of steps we want the car to finish the lap, it will vary depends on the track length
    stepRewardFactor = 0
    baseNumSteps = 300
    if (steps < baseNumSteps):
        stepsProgress = (steps / baseNumSteps) * 100
        stepsProgressDiff = stepsProgress - progress
        progressStepDiff = progress - stepsProgress
        
        # Only apply the progress reward when steps faster than expected
        if (stepsProgressDiff) > 5:
            stepRewardFactor = 0.01
        elif (stepsProgressDiff) > 3:
            stepRewardFactor = 0.1
        elif (stepsProgressDiff) > 1:
            stepRewardFactor = 0.7
        elif (stepsProgressDiff) > 0:
            stepRewardFactor = 0.9
        else:
            stepRewardFactor = 1 + (progressStepDiff/100)*STEP_REWARD_RATE
    else:
        stepRewardFactor = 0.001
##### END: STEP REWARD #####

    reward=(POSITION_REWARD_RATE*positionReward+SPEED_REWARD_RATE*speedReward+DIRECTION_REWARD_RATE*directionReward+progressReward*PROGRESS_REWARD_RATE)*stepRewardFactor
    
    if not all_wheels_on_track and ignoreOffTrackInd == 0:
        reward*=0.7
        
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
    #print('waypoints: ', waypoints)
    print('x: ', x)
    print('y: ', y)
    print('speed: ', speed)
    print('is_offtrack: ', is_offtrack)
    print('is_left_of_center', is_left_of_center)
    print('distance_from_center', distance_from_center)
    print('direction_diff: ', direction_diff)
    print('directionReward: ', directionReward)
    print('positionReward: ', positionReward)
    print('progressReward: ', progressReward)
    print('speedReward: ', speedReward)
    print('stepRewardFactor: ', stepRewardFactor)
    print('reward: ', reward)
    
    return float(reward)