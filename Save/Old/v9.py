#######################################################################################################################
############################## ------ MEASURE TIME EXECUTION  ------ ##################################################
from operator import index
import timeit
start = timeit.default_timer()

#######################################################################################################################
############################## ------ PERMUTATION FUNCTION  ------ ####################################################
import itertools

#######################################################################################################################
############################## ------ LOUNGE_ARRAY --> df_lounge  ------ ##############################################
import pandas as pd
import re

df_lounge = pd.read_csv('lounge.csv', sep=';', header=None)
numberOfLounge = len(df_lounge.iloc[:, 0])
arr_lounge = []
# print(df_taxi)

for var_lounge in range(0, numberOfLounge):
    try:
        arr_lounge.append([df_lounge[1][var_lounge], int(df_lounge[8][var_lounge]), int(df_lounge[3][var_lounge])])
    except:
        arr_lounge.append([df_lounge[1][var_lounge], 1, 1])


# After running this code, you will not receive any_case
def findPassenger(nameOfFlight):
    for temp_lounge in arr_lounge:
        if temp_lounge[0] == nameOfFlight:
            return temp_lounge[1], temp_lounge[2]
    
    # print("Fault at finding Passenger")
    return -1, -1

#######################################################################################################################
############################## ------ TAXI_ARRAY --> df_taxi ------ ###################################################
df_taxi = pd.read_csv('taxi.csv', sep=';', header=None)
# print(df_taxi)

# Find the average and maximum value taxi for each aircraft ----> FOR ONLY OBJECTIVE FUNCTION 
def findTaxi(position):
    for searchTaxi in range(0, 104):
        if df_taxi[0][searchTaxi] == position:

            return float(df_taxi[1][searchTaxi]), float(df_taxi[2][searchTaxi])
    
    # if it cannot return above
    print("Position wasnot exist in finding TAXI at", position)
    return -1, -1

#######################################################################################################################
############################## ------ INITIAL PARAMETERS - FROM MISS.TRANG ------ #####################################
arr_APU = ["123", "234"]
w_1 = 1
w_2 = 1
w_3 = 1
w_4 = 1

# VARIABLES FOR OBJECTIVE FUNCTION 
n_flights_apron = 0         # for R_1 --> global variable
n_flights_waiting = 1       # for R_3 --> will be zero

#######################################################################################################################
############################## ------ PARAMETERS SYSTEM ------ ########################################################
# this variable for the time each aircraft will be towed to the backup site
# maybe will be changed in next time (FIX)
time_break = 10
count_loop = 0

#######################################################################################################################
############################## ------ 86 TERMINALS WITH 4 KINDS OF CORRESPONDING LEVELS ------ ########################
arr_level_case1 = []
arr_level_case2 = []
arr_level_case3 = []
arr_level_case4 = []

arr_pos_case1 = [3, 36, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68]
arr_pos_case2 = [1, 2, 31, 32, 33, 34, 37, 38, 40, 41, 42, 43, 51, 52, 53, 54, 71, 72, 73, 74,
              75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 91, 92, 93, 100, 101, 102, 103, 104]
arr_pos_case3 = [4, 5, 6, 7, 8, 9, 14, 15,
              16, 17, 18, 19, 20, 21, 22, 25, 26, 27]
arr_pos_case4 = [11, 12, 13]

# Array contained level and the flight previous-- ["No flight previous" ,nameOfFlight, kindOfFlight]
for i in range(0, len(arr_pos_case1)):
    arr_level_case1.append([-5,"-","-"])
for i in range(0, len(arr_pos_case2)):
    arr_level_case2.append([-5,"-","-"])
for i in range(0, len(arr_pos_case3)):
    arr_level_case3.append([-5,"-","-"])
for i in range(0, len(arr_pos_case4)):
    arr_level_case4.append([-5,"-","-"])


#######################################################################################################################
############################## ------ SUB_FUNC FOR PROCESSING DATA ------ #############################################
# FUNC: Get the FIRST VALUE in a element of array to sort
def takeOne(elem):
    return elem[0]

# FUNC: Check the next day 
def next_day(string):
    for i in range(0, len(string)):
        if string[i] == '+':
            # print("next_day")
            return True
    return False

# FUNC: Get the time from string TIME
def decode_time(_string):
    if len(_string) == 3:
        return int(_string[0]) * 60 + int(_string[1:3])
    elif len(_string) == 4:
        return int(_string[0:2]) * 60 + int(_string[2:4])

#######################################################################################################################
############################## ------ DATA FRAME ARRAY --> df ------ ##################################################
# NOTE: DATA INPUT MUST BE SORTED
# 1. Read data from file "input.csv"
df = pd.read_csv('input.csv', sep=';', header=None)
numberOfFlights = len(df.iloc[:, 0])
# print(df)

# 2. Initial array contained data
arr_codeFlights = []    # colum index = 3 
arr_schedule = []       # colum index = 4
arr_timeDeparture = []  # colum index = 5
arr_timeArrival = []    # colum index = 6
arr_last_colum = []     # colum index = 7

# 3. DATA PROCESSCING
# FUNC: ARR_CODEFLIGHTS ARRAY #######################################################
for i in range(0, numberOfFlights):

    string = df[3][i][0:2] # always 2 first letters
    test_string = df[3][i] # temp string 
    res = [int(i) for i in test_string.split() if i.isdigit()] # get all numbers from the index 3 

    if len(res) == 0:
        arr_codeFlights.append([test_string, str("-")])
    elif len(res) == 1:
        arr_codeFlights.append([string+str(res[0]), str("-")])
    elif len(res) == 2:
        arr_codeFlights.append([string+str(res[0]), string+str(res[1])])
    else:
        print("Fault at decode arr_codeFlights")


# FUNC: ARR_SCHEDULE ARRAY ##########################################################
for x in range(0, numberOfFlights):
    temp = df[4][x]
    if len(temp) != 7 and len(temp) != 11:
        print("Fault at decode arr_arr_schedule at index:", x+1, "with",  temp)

    if len(temp) == 7:
        if temp[0:3] == "SGN":
            arr_schedule.append('3')
        else:
            arr_schedule.append('4')
    else:
        if temp[4:7] == "SGN":
            arr_schedule.append('1')
        else:
            arr_schedule.append('2')

# FUNC: ARR_TIMEDEPARTURE ARRAY #####################################################
for x in range(0, numberOfFlights):
    # next_day(str(df[6][x]))
    time = re.findall('[0-9]+', str(df[5][x]))
    try:
        time[0]
    except:
        arr_timeDeparture.append(-1)
    else:
        arr_timeDeparture.append(decode_time(time[0]))

# FUNC: if next flight -> add 1 day to this flight
for search in range(0, len(arr_timeDeparture)):
    if next_day(str(df[5][search])) == True:
        arr_timeDeparture[search] += 1440

# FUNC: ARR_TIMEARRIVAL ARRAY #######################################################

for x in range(0, numberOfFlights):
    # next_day(str(df[6][x]))
    time = re.findall('[0-9]+', str(df[6][x]))
    try:
        time[0]
    except:
        arr_timeArrival.append(-1)
    else:
        arr_timeArrival.append(decode_time(time[0]))

# FUNC: if next flight -> add 1 day to this flight
for search in range(0, len(arr_timeArrival)):
    if next_day(str(df[6][search])) == True:
        arr_timeArrival[search] += 1440

# FUNC: THE LAST_COLUM ARRAY ########################################################
for last in range(0, numberOfFlights):
    arr_last_colum.append(df[7][last])

# Testing get data from input.csv ###################################################
# for idx in range(0, numberOfFlights):
    # print(idx, arr_codeFlights[idx], arr_schedule[idx], arr_timeDeparture[idx], arr_timeArrival[idx], arr_last_colum[idx])

def isValidFlight(position):
    if len(df[1][position]) != 4 and len(df[1][position]) != 9:
        # print("[Fault_001]", position, ", codeFlight:", df[1][position])
        return False

    countValid = 0
    arr_validFlight = []
    if len(df[1][position]) == 4:
        arr_validFlight.append(df[1][position][0:4])
    if len(df[1][position]) == 9:
        arr_validFlight.append(df[1][position][5:9])

    for valid in arr_validFlight:
        try:
            testNumber = int(valid[1:4])
        except:
            # print("[Fault_001]", position, ", codeFlight:", df[1][position])
            return False

        if valid == "A320" or valid == "A321" or (valid[0:1] == "A" and 340 < testNumber < 600) or (valid[0:1] == "B" and 200 < testNumber < 800):
            countValid += 1
    
    if countValid == len(arr_validFlight):
        return True
    else: 
        # print("[Fault_001]", position, ", codeFlight:", df[1][position])
        return False

#######################################################################################################################
############################## ------ OBJECTIVE FUNCTION ----- ########################################################
def Objective_Function(kindOfFlight, time, position, isVN):
    # print("test_objective_value:", kindOfFlight, time, position, isVN)
    global w_1, w_2, w_3, w_4, count_loop, n_flights_apron, numberOfFlights
    count_loop += 1

    # This value will change in below algorithm 
    R_Apron = n_flights_apron/numberOfFlights

    avg_Taxi, max_Taxi = findTaxi(position)
    R_Taxi = float(avg_Taxi/max_Taxi)

    R_Hold = n_flights_waiting/numberOfFlights
    
    actualAreaPassenger, maxAreaPassenger = findPassenger(isVN)
    R_Service = (maxAreaPassenger - actualAreaPassenger) / maxAreaPassenger
    
    return w_1*R_Apron + w_2*R_Taxi + w_3*R_Hold + w_4*R_Service + 1

#######################################################################################################################
############################## ------ SUB-FUNCTION FOR FINDING TERMINAL ----- #########################################
# FUNC: 
def get_level_from_position(position):
    index = 0
    for pos in arr_pos_case1:
        if position == pos:
            return arr_level_case1[index][0]
        index += 1
    
    index = 0
    for pos in arr_pos_case2:
        if position == pos:
            return arr_level_case2[index][0]
        index += 1
    
    index = 0
    for pos in arr_pos_case3:
        if position == pos:
            return arr_level_case3[index][0]
        index += 1
    
    index = 0
    for pos in arr_pos_case4:
        if position == pos:
            return arr_level_case4[index][0]
        index += 1

    print("Fault at getting level of flight")    
    return -10

# FUNC: Find the terminal, and update with newlevel, new kindOfFlight, new noFlight --> get flight -> update new level and new flight 
def update_level(position, newlevel, curr_kindFlight, curr_flightNo):
    for index in range(0, len(arr_pos_case1)):
        if position == arr_pos_case1[index]:
            arr_level_case1[index][0] = newlevel
            arr_level_case1[index][1] = curr_kindFlight
            arr_level_case1[index][2] = curr_flightNo
            return
    
    for index in range(0, len(arr_pos_case2)):
        if position == arr_pos_case2[index]:
            arr_level_case2[index][0] = newlevel
            arr_level_case2[index][1] = curr_kindFlight
            arr_level_case2[index][2] = curr_flightNo
            return
    
    for index in range(0, len(arr_pos_case3)):
        if position == arr_pos_case3[index]:
            arr_level_case3[index][0] = newlevel
            arr_level_case3[index][1] = curr_kindFlight
            arr_level_case3[index][2] = curr_flightNo
            return

    for index in range(0, len(arr_pos_case4)):
        if position == arr_pos_case4[index]:
            arr_level_case4[index][0] = newlevel
            arr_level_case4[index][1] = curr_kindFlight
            arr_level_case4[index][2] = curr_flightNo
            return

    print("The position wasnot found for updating at:", position, newlevel, df[1][indexFlight][0:4], arr_codeFlights[indexFlight][0])
    return -1

# FUNC: 
def get_previous_flight(position):
    for index in range(0, len(arr_pos_case1)):
        if position == arr_pos_case1[index]:
            return arr_level_case1[index][1], arr_level_case1[index][2]

    for index in range(0, len(arr_pos_case2)):
        if position == arr_pos_case2[index]:
            return arr_level_case2[index][1], arr_level_case2[index][2]

    for index in range(0, len(arr_pos_case3)):
        if position == arr_pos_case3[index]:
            return arr_level_case3[index][1], arr_level_case3[index][2]

    for index in range(0, len(arr_pos_case4)):
        if position == arr_pos_case4[index]:
            return arr_level_case4[index][1], arr_level_case4[index][2]

    print("Fault at finding previous flight")    
    return -3, -4

def update_n_Apron(timeCurrent):
    global n_flights_apron
    numberOfApron = 0
    for look in arr_priority_3:
        temp_level = get_level_from_position(look)
        if (temp_level + time_break) > timeCurrent:
            numberOfApron += 1
    n_flights_apron = numberOfApron

#######################################################################################################################
############################## ------ FIND TERMINAL FUNCTION ----- ####################################################
# NOTE: ARRAY CONTAINED THE PRIORITY
arr_priority_1 = [4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17]
arr_priority_2 = [8, 9, 15, 16, 17, 18, 19, 20, 21, 22]
arr_priority_3 = [4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 20, 21, 22]

# This function is ONLY the mission for "FIND THE TERMINAL"  (Donot change anything)
# Hence -> MUST return "POSITION AND LEVEL"
def find_terminal(kindOfFlight, isVN, time_A, time_D, last_colum, arr_avoid):
    # 1. Check the priority of "APU"
    mode_APU = False
    temp_APU = re.sub("[^0-9]", "", isVN)       # get the number from a string "isVN"
    for idx in range(0, len(arr_APU)):
        if temp_APU == arr_APU[idx]:
            mode_APU = True
            break

    # 2. var_time to determining exactly time for finding terminal
    var_time = time_D
    if time_A != -1:
        var_time = time_A

    # 3. Run the code with the priority first -- [If terminal was found in this case, it will return IMMEDIATELY]
    _position = -2
    _level = -2
    min_objective = 5

    modeSkip = False
    if (((time_A != -1) and (60 < (time_D - time_A) < 90)) or (time_A == -1)) and (kindOfFlight != "A320") and (kindOfFlight != "A321"):
        if isVN[0:2] == "VN":
            for idx in arr_priority_1: # idx = position 
                # Skip ONLY 1 loop if index in arr_avoid
                for test_avoid in arr_avoid:
                    if idx == test_avoid:
                        modeSkip = True
                        break

                if modeSkip == False:
                    temp_level = get_level_from_position(idx)                                # <FIX>
                    temp_objective = Objective_Function(kindOfFlight, var_time, idx, isVN)   # <FIX>      
                    if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                        min_objective = Objective_Function(kindOfFlight, var_time, idx, isVN)
                        _position = idx
                        _level = get_level_from_position(idx)
                
                if modeSkip == True:
                    modeSkip = False
        else:
            for idx in arr_priority_2:
                # Skip ONLY 1 loop if index in arr_avoid
                for test_avoid in arr_avoid:
                    if idx == test_avoid:
                        modeSkip = True
                        break

                if modeSkip == False:
                    temp_level = get_level_from_position(idx)                                # <FIX>
                    temp_objective = Objective_Function(kindOfFlight, var_time, idx, isVN)   # <FIX>      
                    if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                        min_objective = temp_objective
                        
                        _position = idx
                        _level = get_level_from_position(idx)
                
                if modeSkip == True:
                    modeSkip = False
        
        if _position != -2:
            update_n_Apron(time_D)
            return _position, _level, min_objective
    
    # 4. Run the code without the priority
    _position = -2
    _level = -2
    min_objective = 5

    if kindOfFlight == "A320":
        for lookup in arr_pos_case1:
            # Skip ONLY 1 loop if index in arr_avoid
            for test_avoid in arr_avoid:
                if lookup == test_avoid:
                    modeSkip = True
                    break
                
            if modeSkip == False:
                temp_level = get_level_from_position(lookup)                                # <FIX>
                temp_objective = Objective_Function(kindOfFlight, var_time, lookup, isVN)   # <FIX>
                if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                    min_objective = temp_objective
                    _position = lookup
                    _level = temp_level
            
            if modeSkip == True:
                modeSkip = False

    if (kindOfFlight == "A321") or (kindOfFlight == "A320"):
        for lookup in arr_pos_case2:
            if (mode_APU == True) and (lookup == 37 or lookup == 38 or lookup == 40 or lookup == 41 or lookup == 42 or lookup == 43):
                continue
            else:
                # Skip ONLY 1 loop if index in arr_avoid
                for test_avoid in arr_avoid:
                    if lookup == test_avoid:
                        modeSkip = True
                        break
                
                if modeSkip == False:
                    temp_level = get_level_from_position(lookup)                                # <FIX>
                    temp_objective = Objective_Function(kindOfFlight, var_time, lookup, isVN)   # <FIX>
                    if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                        min_objective = temp_objective
                        _position = lookup
                        _level = temp_level

                if modeSkip == True:
                    modeSkip = False

    if (kindOfFlight[0] == "B" and 400 <= int(kindOfFlight[1:4]) <= 747) or (kindOfFlight[0] == "A" and 340 <= int(kindOfFlight[1:4]) <= 600) or (kindOfFlight == "A321") or (kindOfFlight == "A320"):
        for lookup in arr_pos_case3:
            # Skip ONLY 1 loop if index in arr_avoid
            for test_avoid in arr_avoid:
                if lookup == test_avoid:
                    modeSkip = True
                    break
            
            if modeSkip == False:
                temp_level = get_level_from_position(lookup)                                # <FIX>
                temp_objective = Objective_Function(kindOfFlight, var_time, lookup, isVN)   # <FIX>
                if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                    min_objective = temp_objective
                    _position = lookup
                    _level = temp_level
            
            if modeSkip == True:
                modeSkip = False

    # MAYBE delete this condition because flights in this array is the biggest type 
    if (kindOfFlight[0] == "B" and 787 <= int(kindOfFlight[1:4]) <= 900) or (kindOfFlight[0] == "B" and 200 <= int(kindOfFlight[1:4]) <= 777) or (kindOfFlight[0] == "B" and 400 <= int(kindOfFlight[1:4]) <= 747) or (kindOfFlight[0] == "A" and 340 <= int(kindOfFlight[1:4]) <= 600) or (kindOfFlight == "A321") or (kindOfFlight == "A320"):

        for lookup in arr_pos_case4:
            # Skip ONLY 1 loop if index in arr_avoid
            for test_avoid in arr_avoid:
                if lookup == test_avoid:
                    modeSkip = True
                    break
            
            if modeSkip == False:
                temp_level = get_level_from_position(lookup)                                # <FIX>
                temp_objective = Objective_Function(kindOfFlight, var_time, lookup, isVN)   # <FIX>
                if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                    min_objective = temp_objective
                    _position = lookup
                    _level = temp_level
            
            if modeSkip == True:
                modeSkip = False

    update_n_Apron(time_D)
    if min_objective == 5:
        print("\nFind terminal:", kindOfFlight, isVN, time_A, time_D, last_colum)    
        # print("It cannot find a suitable terminal:", _position, _level, min_objective)
        print("time:", time_A, time_D)
        print(get_level_from_position(11))    
        print(get_level_from_position(12))
        print(get_level_from_position(13))
        # if _position == 11:
        #     print("case 11 and - level: ", _level, kindOfFlight, isVN, time_A, time_D, last_colum)
        # elif _position == 12:
        #     print("case 12 and - level: ", _level, kindOfFlight, isVN, time_A, time_D, last_colum)
        # elif _position == 13:
        #     print("case 13 and - level: ", _level, kindOfFlight, isVN, time_A, time_D, last_colum)


    return _position, _level, min_objective

#######################################################################################################################
############################## ------ GENETIC ALGORITHM ------ ########################################################

def combination_function(init__list, status_case, var_indexFlight):
    if status_case == 1:
        temp_var_indexFlight = var_indexFlight
        # 1. Array and variables for get optimised permutation
        temp_list = init__list
        minValueOfAllObjectiveFunction = 100
        
        # Array contained position after permutation process 
        arr_pos_optimise = []
        arr_initValue = []
        
        # Array and varibales for temp_purpose below
        indexOfPermutation = 0  
        indexReturnPermutation = 0
        arr_temp_purpose = []
        arr_temp2_purpose = []

        # 2. Create array contain [1,2,3,4,....] and permutation to get the case of optimised case in temp_list below
        for create in range(0, len(init__list)):
            arr_temp_purpose.append(create)

        per_temp = itertools.permutations(arr_temp_purpose) # <Permutation and adding to array "arr_temp2_purpose">
        for val in per_temp:
            arr_temp2_purpose.append(val)
        
        # 3. PERMUTATION PROCESS WITH temp_list (init_list)
        per = itertools.permutations(temp_list)
        for val in per:
            # 3.1 Next permutation index
            indexOfPermutation += 1     

            # 3.2 Initial variable for each permutation
            temp_value_minimum = 0
            arr_temp_pos_optimise = []

            # 3.3 Calculate the value a certain case -> return best value of minimum 
            for insideLoop in val:
                # 3.3.1. Find a suitable position   
                pos, level, final_l = find_terminal(insideLoop[0], insideLoop[1], insideLoop[2], insideLoop[3], insideLoop[4], arr_temp_pos_optimise)

                # 3.3.2. Increase temp_value_minimum for finding optimise method
                temp_value_minimum += final_l

                # 3.3.3. Add this flight into case_optimise array and saving all the pos into temp_array_avoid_pos array
                arr_temp_pos_optimise.append(pos)

                # 3.3.4 Add initial value to "arr_initValue"
                if indexOfPermutation == 1:
                    arr_initValue.append(final_l)

            # 3.4 Check the "temp_value_minimum". It's the best case? 
            if temp_value_minimum < minValueOfAllObjectiveFunction:
                indexReturnPermutation = indexOfPermutation
                minValueOfAllObjectiveFunction = temp_value_minimum
                arr_pos_optimise = arr_temp_pos_optimise
        
        # 4. Add case_optimise into pos_optimise
        for adder in range(0, len(arr_pos_optimise)):
            # 4.1. Temp variable for easier way 
            tempIndex =  temp_var_indexFlight + arr_temp2_purpose[indexReturnPermutation - 1][adder]   
    
            # 4.2. Update again level with time_Departure
            newlevel = arr_timeDeparture[tempIndex]

            update_level(arr_pos_optimise[adder], newlevel, df[1][tempIndex][0:4], arr_codeFlights[tempIndex][0]) 

            # 4.3. Add the flight to the result
            arr_result.append([tempIndex, df[1][tempIndex][0:4], arr_codeFlights[tempIndex][0], arr_timeArrival[tempIndex], arr_timeDeparture[tempIndex], arr_pos_optimise[adder], df[1][tempIndex][0:4], arr_codeFlights[tempIndex][1], arr_initValue[adder], final_l])

    elif len(init__list) == 1:
        arr_tt = []

        if status_case == 2:
            ##--------------------- PHASE 1 ---------------------## <the first flight in input.csv>
            # 1. Find a suitable position
            pos, level, final_l = find_terminal(init__list[0][0], init__list[0][1], init__list[0][2], init__list[0][3], init__list[0][4], arr_tt)

            # 2 UPDATE time_A and time_D
            time_A = -1
            if level != 0:
                time_A = level
            time_D = arr_timeDeparture[var_indexFlight] # maybe time_D = time_minute    

            # 3 Get the previous flight 
            kind_Light_Arrival, flightNo_Arrival = get_previous_flight(pos)

            # 4. UPDATE NEW LEVEL HERE 
            newlevel = time_D
            update_level(pos, newlevel, df[1][var_indexFlight][0:4], arr_codeFlights[var_indexFlight][0])

            # 5. Add the flight to the result
            arr_result.append([var_indexFlight, kind_Light_Arrival, flightNo_Arrival, time_A, time_D, pos, df[1][var_indexFlight][0:4], arr_codeFlights[var_indexFlight][0], -9, final_l])
            
            ##--------------------- PHASE 2 ---------------------##  Getting "ONLY" the second flight to queue waiting array
            # 1. Get the name of flight for adding into queue arr_waiting
            flightNO_temp = ''
            if len(df[1][var_indexFlight]) == 4:
                flightNO_temp = df[1][var_indexFlight]
            elif len(df[1][var_indexFlight]) == 9:
                flightNO_temp = df[1][var_indexFlight][5:9]
            else:                                                                   # <FIX> -- maybe NO delete this line
                print("Get len df [1][index] fault at:", df[1][var_indexFlight])    # <FIX> -- maybe NO delete this line
            
            # 2. Adding here
            arr_waiting_flight.append(                          
                [arr_timeArrival[var_indexFlight], arr_codeFlights[var_indexFlight][1], flightNO_temp, str(arr_last_colum[var_indexFlight])])

            # 3. ALWAYS SORT WHEN ADD FLIGHT TO WAITING_FLIGHT
            try:
                arr_waiting_flight.sort(key=takeOne)  # OKAY
            except:
                print("Fault sorted")

        elif status_case == 3:
            # 1. Find a suitable position
            pos, level, final_l = find_terminal(df[1][var_indexFlight][0:4], arr_codeFlights[var_indexFlight][0], -1, arr_timeDeparture[var_indexFlight], str(arr_last_colum[var_indexFlight]), arr_tt)
            
            # 2 UPDATE time_A and time_D
            time_A = -1
            if level != 0:
                time_A = level
            time_D = arr_timeDeparture[var_indexFlight] # maybe time_D = time_minute    

            # 3. Get the previous flight 
            kind_Light_Arrival, flightNo_Arrival = get_previous_flight(pos)

            # 4. UPDATE NEW LEVEL HERE 
            newlevel = time_D
            update_level(pos, newlevel, df[1][var_indexFlight][0:4], arr_codeFlights[var_indexFlight][0]) 

            # 5. Adding the result_array
            arr_result.append([var_indexFlight, kind_Light_Arrival, flightNo_Arrival, time_A, time_D, pos, df[1][var_indexFlight][0:4], arr_codeFlights[var_indexFlight][0], -9, final_l])
            
            ###########################
            temp_var_indexFlight = var_indexFlight
            # 1. Array and variables for get optimised permutation
            temp_list = init__list
            minValueOfAllObjectiveFunction = 100
            
            # Array contained position after permutation process 
            arr_pos_optimise = []
            arr_initValue = []
            
            # Array and varibales for temp_purpose below
            indexOfPermutation = 0  
            indexReturnPermutation = 0
            arr_temp_purpose = []
            arr_temp2_purpose = []

            # 2. Create array contain [1,2,3,4,....] and permutation to get the case of optimised case in temp_list below
            for create in range(0, len(init__list)):
                arr_temp_purpose.append(create)

            per_temp = itertools.permutations(arr_temp_purpose) # <Permutation and adding to array "arr_temp2_purpose">
            for val in per_temp:
                arr_temp2_purpose.append(val)
            
            # 3. PERMUTATION PROCESS WITH temp_list (init_list)
            per = itertools.permutations(temp_list)
            for val in per:
                # 3.1 Next permutation index
                indexOfPermutation += 1     

                # 3.2 Initial variable for each permutation
                temp_value_minimum = 0
                arr_temp_pos_optimise = []

                # 3.3 Calculate the value a certain case -> return best value of minimum 
                for insideLoop in val:
                    # 3.3.1. Find a suitable position   
                    pos, level, final_l = find_terminal(insideLoop[0], insideLoop[1], insideLoop[2], insideLoop[3], insideLoop[4], arr_temp_pos_optimise)                

                    # 3.3.2. Increase temp_value_minimum for finding optimise method
                    temp_value_minimum += final_l

                    # 3.3.3. Add this flight into case_optimise array and saving all the pos into temp_array_avoid_pos array
                    arr_temp_pos_optimise.append(pos)

                    # 3.3.4 Add initial value to "arr_initValue"
                    if indexOfPermutation == 1:
                        arr_initValue.append(final_l)

                # 3.4 Check the "temp_value_minimum". It's the best case? 
                if temp_value_minimum < minValueOfAllObjectiveFunction:
                    indexReturnPermutation = indexOfPermutation
                    minValueOfAllObjectiveFunction = temp_value_minimum
                    arr_pos_optimise = arr_temp_pos_optimise
            
            # 4. Add case_optimise into pos_optimise
            for adder in range(0, len(arr_pos_optimise)):
                # 4.1. Temp variable for easier way 
                tempIndex =  temp_var_indexFlight + arr_temp2_purpose[indexReturnPermutation - 1][adder]   
        
                # 4.2. Update again level with time_Departure
                newlevel = arr_timeDeparture[tempIndex]

                update_level(arr_pos_optimise[adder], newlevel, df[1][tempIndex][0:4], arr_codeFlights[tempIndex][0]) 

                # 4.3. Add the flight to the result
                arr_result.append([tempIndex, df[1][tempIndex][0:4], arr_codeFlights[tempIndex][0], arr_timeArrival[tempIndex], arr_timeDeparture[tempIndex], arr_pos_optimise[adder], df[1][tempIndex][0:4], arr_codeFlights[tempIndex][1], arr_initValue[adder], final_l])



        elif status_case == 4:
            print("case 4 wasnot implemented, never get here")
        
        else:
            print("Fault at getting status_case, never get here")
    
    else:

        if status_case == 2:
            print("status_case 2")
            # TODO:

        elif status_case == 3:
            # 1. Find a suitable position
            pos, level, final_l = find_terminal(df[1][var_indexFlight][0:4], arr_codeFlights[var_indexFlight][0], -1, arr_timeDeparture[var_indexFlight], str(arr_last_colum[var_indexFlight]), arr_tt)
            
            # 2 UPDATE time_A and time_D
            time_A = -1
            if level != 0:
                time_A = level
            time_D = arr_timeDeparture[var_indexFlight] # maybe time_D = time_minute    

            # 3. Get the previous flight 
            kind_Light_Arrival, flightNo_Arrival = get_previous_flight(pos)

            # 4. UPDATE NEW LEVEL HERE 
            newlevel = time_D
            update_level(pos, newlevel, df[1][var_indexFlight][0:4], arr_codeFlights[var_indexFlight][0]) 

            # 5. Adding the result_array
            arr_result.append([var_indexFlight, kind_Light_Arrival, flightNo_Arrival, time_A, time_D, pos, df[1][var_indexFlight][0:4], arr_codeFlights[var_indexFlight][0], -9, final_l])




        # REMOVE ALL ELEMENTS IN ARRAY
        try:
            temp_list.clear()
        except:
            print("Fault at removing temp_list in combination function")

    # REMOVE ALL ELEMENTS IN ARRAY FOR RE-USE THIS ARRAY <MUST BE IN PYTHON>
    try:
        init__list.clear()
    except:
        print("Fault at removing init__list in combination function")
    
    return
#######################################################################################################################
############################## ------ ALGORITHM ARRANGEMENT ------ ####################################################

# ARRAY CONTAIN RESULT INFORMATION 
arr_result = []             # the final result array
arr_waiting_flight = []     # waiting flights


# VARIABLES FOR ALGORITHM
indexFlight = 0
arr_tempMission = []
temp_indexFlight = 0
modeOne = modeTwo = modeThree = False

# TIME IS FROM 1 TO 1440     <FIX>
for time_minute in range(0, 1440):
    while (time_minute == arr_timeDeparture[indexFlight]) or (arr_timeDeparture[indexFlight] == -1):
        # IGNORE FLIGHT IF IT'S INVALID
        while isValidFlight(indexFlight) == False:
            indexFlight += 1

        # [?--SGN--?] ------ CASE 1 - STAGE 1 -> ADD FLIGHT INTO "arr_tempMission"
        while (time_minute == arr_timeDeparture[indexFlight]) and (arr_schedule[indexFlight] == '1'): # if arr_schedule[indexFlight] == '1':
            # 1. IGNORE FLIGHT IF IT'S INVALID
            while isValidFlight(indexFlight) == False:
                indexFlight += 1
            
            # 2. Add flight into arr_tempMission
            arr_tempMission.append([df[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], arr_timeArrival[indexFlight], arr_timeDeparture[indexFlight], str(arr_last_colum[indexFlight])])
            
            # 3. Saving the initial index of the loop 
            if modeOne == False:
                modeOne = True
                temp_indexFlight = indexFlight      # Get the first index of the loop while <IMPORTANCE>

            # 4. Next flight
            indexFlight += 1
        
        # --------- CASE 1 - STAGE 2 -> CALL GENETIC ALGORITHM
        if modeOne == True:
            combination_function(arr_tempMission, 1, temp_indexFlight)
            modeOne = False
    
        # [SGN--?--SGN] ------ CASE 2 - STAGE 1 -> ADD FLIGHT INTO "arr_tempMission"
        # while (time_minute == arr_timeDeparture[indexFlight]) and (arr_schedule[indexFlight] == '2'): 
        if arr_schedule[indexFlight] == '2':
            # IGNORE FLIGHT IF IT'S INVALID
            while isValidFlight(indexFlight) == False:
                indexFlight += 1

            # # 1. Add flight into arr_tempMission and TURN ON "modeTwo"
            arr_tempMission.append([df[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], -1, arr_timeDeparture[indexFlight], str(arr_last_colum[indexFlight])])
            modeTwo = True

            # 2. Next flight and get the temp_indexFlight
            temp_indexFlight = indexFlight
            indexFlight += 1


        # --------- CASE 2 - STAGE 2 -> CALL GENETIC ALGORITHM <COMBINATION FUNCTION>
        if modeTwo == True:
            combination_function(arr_tempMission, 2, temp_indexFlight)
            modeTwo = False

        # [SGN--?] ------ CASE 3 - STAGE 1 -> ADD FLIGHT INTO "arr_tempMission"
        while (time_minute == arr_timeDeparture[indexFlight]) and (arr_schedule[indexFlight] == '3'): 
        # if arr_schedule[indexFlight] == '3':          // TODO:, tiếp tục ở đây
            # IGNORE FLIGHT IF IT'S INVALID
            while isValidFlight(indexFlight) == False:
                indexFlight += 1

            # 1. Add flight into arr_tempMission and TURN ON "modeThree"
            arr_tempMission.append([df[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], -1, arr_timeDeparture[indexFlight], str(arr_last_colum[indexFlight])])
            modeThree = True

            # 2. Next flight and get the temp_indexFlight
            temp_indexFlight = indexFlight
            indexFlight += 1

        # --------- CASE 3 - STAGE 2 -> CALL GENETIC ALGORITHM <COMBINATION FUNCTION>
        if modeThree == True:
            combination_function(arr_tempMission, 3, temp_indexFlight)
            modeThree = False

        # [?--SGN] ------ CASE 4 -> ADD FLIGHT INTO "arr_waiting_flight"
        if arr_schedule[indexFlight] == '4':
            # 1. Add flight to waiting array
            arr_waiting_flight.append([arr_timeArrival[indexFlight], arr_codeFlights[indexFlight][0], df[1][indexFlight],str(arr_last_colum[indexFlight])])
            
            # 2. Next flight
            indexFlight += 1   

    ########################################################################################################
    ########################################################################################################
    # ADD "flight in queue" to "the head of flight" 
    try:
        while time_minute == arr_waiting_flight[0][0]:  
            # 1. Find a suitable position
            arr_tt = []
            pos, level, final_l = find_terminal(arr_waiting_flight[0][2], arr_waiting_flight[0][1], -1, arr_waiting_flight[0][0], arr_waiting_flight[0][3], arr_tt)
            
            # 2. UPDATE NEW LEVEL HERE 
            newlevel = arr_waiting_flight[0][0]
            update_level(pos, newlevel, arr_waiting_flight[0][2], arr_waiting_flight[0][1])

            # 3. Remove the first element in waiting flights array
            arr_waiting_flight.remove([arr_waiting_flight[0][0], arr_waiting_flight[0][1], arr_waiting_flight[0][2], arr_waiting_flight[0][3]])     
    except:
        print("Fault at processing waiting flight", time_minute)     

#######################################################################################################################
############################## ------ DISPLAY THE RESULT AND STATISTICS ------ ########################################
# print("--------Waiting flights------------")
# for row in arr_waiting_flight:
#     print(row)

# print("--------Result---------------")
# for row in arr_result:
#     print(row)

print("\n--------Statistics---------------")
stop = timeit.default_timer()
print('Time: ', stop - start)  
print("The loop:", count_loop)