#######################################################################################################################
############################## ------ MEASURE TIME EXECUTION  ------ ##################################################
import timeit
start = timeit.default_timer()

#######################################################################################################################
############################## ------ COMBINATION FUNCTION  ------ ####################################################
import operator as op
from functools import reduce
def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom  # or / in Python 2

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
time_break = 30 
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
df = pd.read_csv('in.csv', sep=';', header=None)
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

#######################################################################################################################
############################## ------ OBJECTIVE FUNCTION ----- ########################################################
def Objective_Function(kindOfFlight, time, position, isVN):
    # print("test_objective_value:", kindOfFlight, time, position, isVN)
    global w_1, w_2, w_3, w_4, count_loop
    count_loop += 1

    # This value will change in below algorithm 
    R_Apron = n_flights_apron/numberOfFlights

    avg_Taxi, max_Taxi = findTaxi(position)
    R_Taxi = avg_Taxi/max_Taxi

    R_Hold = n_flights_waiting/numberOfFlights
    
    
    actualAreaPassenger, maxAreaPassenger = findPassenger(isVN)
    R_Service = (maxAreaPassenger - actualAreaPassenger) / maxAreaPassenger
    
    return w_1*R_Apron + w_2*R_Taxi + w_3*R_Hold + w_4*R_Service


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

# FUNC: Find the terminal, and update with newlevel, new kindOfFlight, new noFlight
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
    print("It cannot be updated:", position, newlevel, df[1][indexFlight][0:4], arr_codeFlights[indexFlight][0])
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
    numberOfApron = 0
    for look in arr_priority_3:
        temp_level = get_level_from_position(look)
        if temp_level > timeCurrent:
            numberOfApron += 1
    return numberOfApron

#######################################################################################################################
############################## ------ FIND TERMINAL FUNCTION ----- ####################################################
# NOTE: ARRAY CONTAINED THE PRIORITY
arr_priority_1 = [4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17]
arr_priority_2 = [8, 9, 15, 16, 17, 18, 19, 20, 21, 22]
arr_priority_3 = [4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 20, 21, 22]

# This function is ONLY the mission for "FIND THE TERMINAL"  (Donot change anything)
# Hence -> MUST return "POSITION AND LEVEL"
def find_terminal(kindOfFlight, isVN, time_A, time_D, last_colum):
    # print("\nFind terminal:", kindOfFlight, isVN, time_A, time_D, last_colum)
    # 1. var_time to determining exactly time for finding terminal
    var_time = 0
    if time_A != -1:
        var_time = time_A
    else:
        var_time = time_D

    _position = -2
    _level = -2
    min_objective = 5
    
    # 2. Check the status of priority
    mode_APU = False
    temp_APU = re.sub("[^0-9]", "", isVN)       # get the number from a string "isVN"
    for idx in range(0, len(arr_APU)):
        if temp_APU == arr_APU[idx]:
            mode_APU = True
            break

    # 3. Run the code with the priority first
    ## <If terminal was found in this case, it will return IMMEDIATELY>
    if (((time_A != -1) and (60 < (time_D - time_A) < 90)) or (time_A == -1)) and (kindOfFlight != "A320") and (kindOfFlight != "A321"):
        if isVN[0:2] == "VN":
            for idx in arr_priority_1: # idx = position 
                temp_level = get_level_from_position(idx)                                # <FIX>
                temp_objective = Objective_Function(kindOfFlight, var_time, idx, isVN)   # <FIX>      
                if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                    min_objective = Objective_Function(kindOfFlight, var_time, idx, isVN)
                    _position = idx
                    _level = get_level_from_position(idx)
        else:
            for idx in arr_priority_2:
                temp_level = get_level_from_position(idx)                                # <FIX>
                temp_objective = Objective_Function(kindOfFlight, var_time, idx, isVN)   # <FIX>      
                if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                    min_objective = Objective_Function(kindOfFlight, var_time, idx, isVN)
                    _position = idx
                    _level = get_level_from_position(idx)
        if _position != -2:
            # print("Priority:", _position, _level)
            # isAPRON(_position)
            update_n_Apron(time_D)
            return _position, _level
    
    # 4. Run the code without the priority
    _position = -2
    _level = -2
    min_objective = 5

    if kindOfFlight == "A320":
        for lookup in arr_pos_case1:
            temp_level = get_level_from_position(lookup)                                # <FIX>
            temp_objective = Objective_Function(kindOfFlight, var_time, lookup, isVN)   # <FIX>
            if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                min_objective = temp_objective
                _position = lookup
                _level = temp_level

    if (kindOfFlight == "A321") or (kindOfFlight == "A320"):
        for lookup in arr_pos_case2:
            if (mode_APU == True) and (lookup == 37 or lookup == 38 or lookup == 40 or lookup == 41 or lookup == 42 or lookup == 43):
                continue
            else:
                temp_level = get_level_from_position(lookup)                                # <FIX>
                temp_objective = Objective_Function(kindOfFlight, var_time, lookup, isVN)   # <FIX>
                if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                    min_objective = temp_objective
                    _position = lookup
                    _level = temp_level

    if (kindOfFlight[0] == "B" and 400 <= int(kindOfFlight[1:4]) <= 747) or (kindOfFlight[0] == "A" and 340 <= int(kindOfFlight[1:4]) <= 600) or (kindOfFlight == "A321") or (kindOfFlight == "A320"):
        for lookup in arr_pos_case3:
            temp_level = get_level_from_position(lookup)                                # <FIX>
            temp_objective = Objective_Function(kindOfFlight, var_time, lookup, isVN)   # <FIX>
            if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                min_objective = temp_objective
                _position = lookup
                _level = temp_level

    # MAYBE delete this condition because flights in this array is the biggest type 
    if (kindOfFlight[0] == "B" and 787 <= int(kindOfFlight[1:4]) <= 900) or (kindOfFlight[0] == "B" and 200 <= int(kindOfFlight[1:4]) <= 777) or (kindOfFlight[0] == "B" and 400 <= int(kindOfFlight[1:4]) <= 747) or (kindOfFlight[0] == "A" and 340 <= int(kindOfFlight[1:4]) <= 600) or (kindOfFlight == "A321") or (kindOfFlight == "A320"):
        for lookup in arr_pos_case4:
            temp_level = get_level_from_position(lookup)                                # <FIX>
            temp_objective = Objective_Function(kindOfFlight, var_time, lookup, isVN)   # <FIX>
            if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                min_objective = temp_objective
                _position = lookup
                _level = temp_level
    
    update_n_Apron(time_D)
    # print("Return pos and level: ", _position, _level)
    return _position, _level
#######################################################################################################################
############################## ------ GENETIC ALGORITHM ------ ########################################################

def combination_function(init__list):


    return
#######################################################################################################################
############################## ------ ALGORITHM ARRANGEMENT ------ ####################################################

# ARRAY CONTAIN RESULT INFORMATION 
arr_result = []             # the final result array
arr_waiting_flight = []     # waiting flights
happen_ed = []              # array of history          <FIX> -- may be delete

# VARIABLES FOR ALGORITHM
indexFlight = 0
arr_tempMission = []

# TIME IS FROM 1 TO 1440     <FIX>
for time_minute in range(0, 1440):
    while (time_minute == arr_timeDeparture[indexFlight]) or (arr_timeDeparture[indexFlight] == -1):
        # case 1: ?-SGN-?
        if arr_schedule[indexFlight] == '1':
            # 1. Find a suitable position            
            pos, level = find_terminal(df[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], arr_timeArrival[indexFlight], arr_timeDeparture[indexFlight], str(arr_last_colum[indexFlight]))
            
            # 2. Add the flight to the result
            arr_result.append([indexFlight, df[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], arr_timeArrival[indexFlight], arr_timeDeparture[indexFlight], pos, df[1][indexFlight][0:4], arr_codeFlights[indexFlight][1]])

            # 3. Update again level
            newlevel = arr_timeDeparture[indexFlight]
            update_level(pos, newlevel, df[1][indexFlight][0:4], arr_codeFlights[indexFlight][0]) 

            # 4. Next flight
            indexFlight += 1

            # 5. Add to the history 
            happen_ed.append("1")
    
        # case 2: SGN-?-SGN
        if arr_schedule[indexFlight] == '2':
            ##--------------------- PHASE 1 ---------------------##
            # 1. Find a suitable position
            pos, level = find_terminal(df[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], -1, arr_timeDeparture[indexFlight], str(arr_last_colum[indexFlight]))

            # 2. Add the flight to a just found position
            # 2.1 UPDATE time_A and time_D
            time_A = 0
            if level == 0:
                time_A = -1
            else:
                time_A = level
            time_D = arr_timeDeparture[indexFlight] # maybe time_D = time_minute    

            # 2.2 Get the previous flight 
            kind_Light_Arrival, flightNo_Arrival = get_previous_flight(pos)

            # 3. UPDATE NEW LEVEL HERE 
            newlevel = time_D
            update_level(pos, newlevel, df[1][indexFlight][0:4], arr_codeFlights[indexFlight][0])

            # 4. Adding the result_array
            arr_result.append([indexFlight, kind_Light_Arrival, flightNo_Arrival, time_A, time_D, pos, df[1][indexFlight][0:4], arr_codeFlights[indexFlight][0]])
            
            ##--------------------- PHASE 2 ---------------------##
            ### Getting "ONLY" the second flight to queue
            flightNO_temp = ''
            if len(df[1][indexFlight]) == 4:
                flightNO_temp = df[1][indexFlight]
            elif len(df[1][indexFlight]) == 9:
                flightNO_temp = df[1][indexFlight][5:9]
            else:                                       # <FIX> -- maybe delete this line
                print("Get len df [1][index] fault")    # <FIX> -- maybe delete this line
            
            ### Adding 
            arr_waiting_flight.append(                          
                [arr_timeArrival[indexFlight], arr_codeFlights[indexFlight][1], flightNO_temp, str(arr_last_colum[indexFlight])])

            ### ALWAYS SORT WHEN ADD FLIGHT TO WAITING_FLIGHT
            try:
                arr_waiting_flight.sort(key=takeOne)  # OKAY
            except:
                print("Fault sorted")

            # 5. Next flight
            indexFlight += 1

            # 6. Add to the history 
            happen_ed.append("2")
    
        # case 3: SGN-?
        if arr_schedule[indexFlight] == '3':
            # 1. Find a suitable position
            pos, level = find_terminal(df[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], -1, arr_timeDeparture[indexFlight], str(arr_last_colum[indexFlight]))
            
            # 2. Add the flight to a just found position
            # 2.1 UPDATE time_A and time_D
            time_A = 0
            if level == 0:
                time_A = -1
            else:
                time_A = level
            time_D = arr_timeDeparture[indexFlight] # maybe time_D = time_minute    

            # 2.2 Get the previous flight 
            kind_Light_Arrival, flightNo_Arrival = get_previous_flight(pos)

            # 3. UPDATE NEW LEVEL HERE 
            newlevel = time_D
            update_level(pos, newlevel, df[1][indexFlight][0:4], arr_codeFlights[indexFlight][0]) 

            # 4. Adding the result_array
            arr_result.append([indexFlight, kind_Light_Arrival, flightNo_Arrival, time_A, time_D, pos, df[1][indexFlight][0:4], arr_codeFlights[indexFlight][0]])

            # 5. Next flight 
            indexFlight += 1

            # 6. Add to the history 
            happen_ed.append("3")      

        # case 4: ?-SGN
        if arr_schedule[indexFlight] == '4':
            # 1. Add flight to waiting array
            arr_waiting_flight.append(
                [arr_timeArrival[indexFlight], arr_codeFlights[indexFlight][0], df[1][indexFlight],str(arr_last_colum[indexFlight])])
            
            # 2. Next flight
            indexFlight += 1  

            # 3. Add to the history 
            happen_ed.append("4")  

    ########################################################################################################
    ########################################################################################################
    # ADD "flight in queue" to "the head of flight" 
    try:
        while time_minute == arr_waiting_flight[0][0]:  
            # 1. Find a suitable position
            pos, level = find_terminal(arr_waiting_flight[0][2], arr_waiting_flight[0][1], -1, arr_waiting_flight[0][0], arr_waiting_flight[0][3])
            
            # 2. UPDATE NEW LEVEL HERE 
            newlevel = arr_waiting_flight[0][0]
            update_level(pos, newlevel, arr_waiting_flight[0][2], arr_waiting_flight[0][1])

            # 3. Remove the first element in waiting flights array
            temp_1 = arr_waiting_flight[0][0]
            temp_2 = arr_waiting_flight[0][1]
            temp_3 = arr_waiting_flight[0][2]
            temp_4 = arr_waiting_flight[0][3]
            arr_waiting_flight.remove([temp_1, temp_2, temp_3, temp_4])     
    except:
        print("Fault at processing waiting flight", time_minute)     

#######################################################################################################################
############################## ------ DISPLAY THE RESULT AND STATISTICS ------ ########################################
# print("--------History---------------")
# for row in happen_ed:
#     print(row)

# print("--------Waiting flights------------")
# for row in arr_waiting_flight:
#     print(row)

print("--------Result---------------")
for row in arr_result:
    print(row)

print("\n--------Statistics---------------")
stop = timeit.default_timer()
print('Time: ', stop - start)  
print("The loop:", count_loop)