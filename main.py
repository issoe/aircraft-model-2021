####################################################################################################################################
#################################### ------ Import library  ------ #################################################################
import sub
import pandas as pd
import numpy as np
import re
import random
import csv
# from random import seed
from random import randint
# seed(1)


####################################################################################################################################
# Initial parameters from MISS.TRANG
arr_APU = ["123", "234"]
w_1 = 1
w_2 = 1
w_3 = 1

# System parameters
n_flights_apron = 0
count_loop = 0
time_break = 25

####################################################################################################################################
#################################### ------ MEASURE TIME EXECUTION  ------ #########################################################
import timeit
start = timeit.default_timer()

####################################################################################################################################
#################################### ------ DATA FRAME ARRAY --> dfr ------ #########################################################
# NOTE: DATA INPUT MUST BE SORTED
# 1. Read data from file "input.csv" and get the numberOfFlighs
dfr = pd.read_csv('Input/15.csv', sep=';', header=None)
numberOfFlights = len(dfr.iloc[:, 0])

# 2. Clean DATA and adding into array-s
arr_codeFlights = []    # colum index = 3    ####### Initial array 
arr_schedule = []       # colum index = 4
arr_timeDeparture = []  # colum index = 5
arr_timeArrival = []    # colum index = 6
arr_last_colum = []     # colum index = 7

####### Process  
sub.create_arr_codeflights(dfr, arr_codeFlights, numberOfFlights)
sub.create_arr_schedule(dfr, arr_schedule, numberOfFlights)
sub.create_arr_timeDeparture(dfr, arr_timeDeparture, numberOfFlights)
sub.create_arr_timeArrival(dfr, arr_timeArrival, numberOfFlights)
sub.create_arr_lastColum(dfr, arr_last_colum, numberOfFlights)

theTime = arr_timeDeparture[numberOfFlights - 1]  # The last time of array 

####################################################################################################################################
#################################### ------ 86 TERMINALS WITH 4 KINDS OF CORRESPONDING LEVELS ------ ###############################
arr_level_case1 = []
arr_level_case2 = []
arr_level_case3 = []
arr_level_case4 = []

arr_pos_case1 = [3, 36, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68]
arr_pos_case2 = [1, 2, 31, 32, 33, 34, 37, 38, 40, 41, 42, 43, 51, 52, 53, 54, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 91, 92, 93, 100, 101, 102, 103, 104]
arr_pos_case3 = [4, 5, 6, 7, 8, 9, 14, 15, 16, 17, 18, 19, 20, 21, 22, 25, 26, 27]
arr_pos_case4 = [11, 12, 13]

arr_priority_1 = [4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17]
arr_priority_2 = [8, 9, 15, 16, 17, 18, 19, 20, 21, 22]
arr_priority_3 = [4, 5, 6, 7, 8, 9, 15, 16, 17, 18, 19, 20, 21, 22]


arr_CurrPos1 = arr_pos_case1
arr_CurrPos2 = arr_pos_case2
arr_CurrPos3 = arr_pos_case3
arr_CurrPos4 = arr_pos_case4
arr_CurrPri1 = arr_priority_1
arr_CurrPri2 = arr_priority_2

# Array contained level and the flight previous-- ["No flight previous" ,nameOfFlight, kindOfFlight]
sub.create_initial_level(arr_level_case1, arr_CurrPos1, arr_level_case2, arr_CurrPos2, arr_level_case3, arr_CurrPos3, arr_level_case4, arr_CurrPos4)

####################################################################################################################################
#################################### ------ MY Def ------ #####
def isValidFlight(var_indexFlight):
    if len(dfr[1][var_indexFlight]) != 4 and len(dfr[1][var_indexFlight]) != 9:
        # print("[Fault_001]", position, ", codeFlight:", dfr[1][position])
        return False

    countValid = 0
    arr_validFlight = []
    if len(dfr[1][var_indexFlight]) == 4:
        arr_validFlight.append(dfr[1][var_indexFlight][0:4])
    if len(dfr[1][var_indexFlight]) == 9:
        arr_validFlight.append(dfr[1][var_indexFlight][5:9])

    for valid in arr_validFlight:
        try:
            if valid == "AT72":
                return True
            else:
                testNumber = int(valid[1:4])
        except:
            # print("[Fault_001]", position, ", codeFlight:", dfr[1][position])
            return False

        if valid == "A320" or valid == "A321" or (valid[0:1] == "A" and 340 < testNumber < 600) or (valid[0:1] == "B" and 200 < testNumber < 800):
            countValid += 1
    
    if countValid == len(arr_validFlight):
        return True
    else: 
        # print("[Fault_001]", position, ", codeFlight:", dfr[1][position])
        return False

def get_level_from_position(position):

    for pos in range(0, len(arr_CurrPos1)):
        if position == arr_CurrPos1[pos]:
            return arr_level_case1[pos][0]

    for pos in range(0, len(arr_CurrPos2)):
        if position == arr_CurrPos2[pos]:
            
            return arr_level_case2[pos][0]

    for pos in range(0, len(arr_CurrPos3)):
        if position == arr_CurrPos3[pos]:
            return arr_level_case3[pos][0]

    for pos in range(0, len(arr_CurrPos4)):
        if position == arr_CurrPos4[pos]:
            return arr_level_case4[pos][0]

    print("Fault at getting level of flight")    
    return -10
    
def update_level(position, newlevel, curr_kindFlight, curr_flightNo):
    for index in range(0, len(arr_CurrPos1)):
        if position == arr_CurrPos1[index]:
            arr_level_case1[index][0] = newlevel
            arr_level_case1[index][1] = curr_kindFlight
            arr_level_case1[index][2] = curr_flightNo
            return
    
    for index in range(0, len(arr_CurrPos2)):
        if position == arr_CurrPos2[index]:
            arr_level_case2[index][0] = newlevel
            arr_level_case2[index][1] = curr_kindFlight
            arr_level_case2[index][2] = curr_flightNo
            return
    
    for index in range(0, len(arr_CurrPos3)):
        if position == arr_CurrPos3[index]:
            arr_level_case3[index][0] = newlevel
            arr_level_case3[index][1] = curr_kindFlight
            arr_level_case3[index][2] = curr_flightNo
            return

    for index in range(0, len(arr_CurrPos4)):
        if position == arr_CurrPos4[index]:
            arr_level_case4[index][0] = newlevel
            arr_level_case4[index][1] = curr_kindFlight
            arr_level_case4[index][2] = curr_flightNo
            return

    # print("The position wasnot found for updating at:", position, newlevel, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0])
    return -1

def get_previous_flight(position):
    for idx in range(0, len(arr_CurrPos1)):
        if position == arr_CurrPos1[idx]:
            return arr_level_case1[idx][1], arr_level_case1[idx][2]

    for idx in range(0, len(arr_CurrPos2)):
        if position == arr_CurrPos2[idx]:
            return arr_level_case2[idx][1], arr_level_case2[idx][2]

    for idx in range(0, len(arr_CurrPos3)):
        if position == arr_CurrPos3[idx]:
            return arr_level_case3[idx][1], arr_level_case3[idx][2]

    for idx in range(0, len(arr_CurrPos4)):
        if position == arr_CurrPos4[idx]:
            return arr_level_case4[idx][1], arr_level_case4[idx][2]        

    print("Fault at finding previous flight:", position)    
    return -3, -4

def update_n_Apron(timeCurrent):
    global n_flights_apron

    # Count again
    numberOfRemovePark = 0
    for idx in arr_CurrPos1: # Find all in case 1, 2, 3, 4, and minus apron 
        temp_level = get_level_from_position(idx)
        if (temp_level + time_break) > timeCurrent:
            numberOfRemovePark += 1

    for idx in arr_CurrPos2:
        temp_level = get_level_from_position(idx)
        if (temp_level + time_break) > timeCurrent:
            numberOfRemovePark += 1
    
    for idx in arr_CurrPos3:
        temp_level = get_level_from_position(idx)
        if (temp_level + time_break) > timeCurrent:
            numberOfRemovePark += 1

    for idx in arr_CurrPos4:
        temp_level = get_level_from_position(idx)
        if (temp_level + time_break) > timeCurrent:
            numberOfRemovePark += 1

    for idx in arr_priority_3:
        temp_level = get_level_from_position(idx)
        if (temp_level + time_break) > timeCurrent:
            numberOfRemovePark -= 1

    n_flights_apron = numberOfRemovePark

def Objective_Function(position, n_flights_waiting_g):
    global w_1, w_2, w_3, count_loop, n_flights_apron, numberOfFlights
    count_loop += 1

    R_Apron = float(n_flights_apron/numberOfFlights)

    avg_Taxi, max_Taxi = sub.findTaxi(position)
    R_Taxi = float(avg_Taxi/max_Taxi)

    R_Hold = float(n_flights_waiting_g/numberOfFlights)

    v_object = w_1 * R_Apron + w_2 * R_Taxi + w_3 * R_Hold

    return v_object, n_flights_apron, round(R_Taxi, 8), n_flights_waiting_g

def glo_Objective_Function(var_idx, arr_1, ele1, ele2, stat):
    tempOne = arr_1[var_idx][1] 
    tempTwo = arr_1[var_idx][2]
    arr_1[var_idx][1] = ele1
    arr_1[var_idx][2] = ele2
    valu, _, _, _ = Objective_Function(arr_1[var_idx][5], 0)
    valu += stat[1] # minus what????

    arr_1[var_idx][1] = tempOne
    arr_1[var_idx][2] = tempTwo
    return valu / stat[2]

def find_terminal(kindOfFlight, isVN, time_A, time_D, last_colum, n_waiting):
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
    min_objective = 3

    if (((time_A != -1) and (60 < (time_D - time_A) < 90)) or (time_A == -1)) and (kindOfFlight != "A320") and (kindOfFlight != "A321") and (kindOfFlight != "AT72"):
        if isVN[0:2] == "VN":
            for idx in arr_CurrPri1:      # idx = position
                temp_level = get_level_from_position(idx)                             
                temp_objective, _RR1, _RR2, _RR3 = Objective_Function(idx, n_waiting) 
                if (temp_objective < min_objective) and ((temp_level + time_break) < var_time): 
                    update_n_Apron(time_D)     
                    return idx, temp_level, temp_objective, _RR1, _RR2, _RR3

        else:
            for idx in arr_CurrPri2:
                temp_level = get_level_from_position(idx)                              
                temp_objective, _RR1, _RR2, _RR3 = Objective_Function(idx, n_waiting)  
                if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                    update_n_Apron(time_D) 
                    return idx, temp_level, temp_objective, _RR1, _RR2, _RR3

    # 4. Run the code without the priority
    if kindOfFlight == "A320" or kindOfFlight == "AT72":
        for idx in arr_CurrPos1:
            temp_level = get_level_from_position(idx)        
            temp_objective, _RR1, _RR2, _RR3 = Objective_Function(idx, n_waiting)         
            if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                update_n_Apron(time_D)
                return idx, temp_level, temp_objective, _RR1, _RR2, _RR3

    if kindOfFlight == "A321" or kindOfFlight == "A320" or kindOfFlight == "AT72":
        for idx in arr_CurrPos2:
            if (mode_APU == True) and (idx == 37 or idx == 38 or idx == 40 or idx == 41 or idx == 42 or idx == 43):
                continue
            else:
                temp_level = get_level_from_position(idx)                              
                temp_objective, _RR1, _RR2, _RR3 = Objective_Function(idx, n_waiting)                            
                if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                    update_n_Apron(time_D)
                    return idx, temp_level, temp_objective, _RR1, _RR2, _RR3

    if kindOfFlight != "AT72" and ((kindOfFlight[0] == "B" and 400 <= int(kindOfFlight[1:4]) <= 747) or (kindOfFlight[0] == "A" and 340 <= int(kindOfFlight[1:4]) <= 600)):
        for idx in arr_CurrPos3:
            temp_level = get_level_from_position(idx) 
            temp_objective, _RR1, _RR2, _RR3 = Objective_Function(idx, n_waiting)  
            if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                update_n_Apron(time_D)
                return idx, temp_level, temp_objective, _RR1, _RR2, _RR3

    # The rest of flights
    if kindOfFlight != "AT72" and (kindOfFlight[0] == "B" and 200 <= int(kindOfFlight[1:4]) <= 900):
        for idx in arr_CurrPos4:
            temp_level = get_level_from_position(idx)  
            temp_objective, _RR1, _RR2, _RR3 = Objective_Function(idx, n_waiting)   
            if (temp_objective < min_objective) and ((temp_level + time_break) < var_time):
                update_n_Apron(time_D)
                return idx, temp_level, temp_objective, _RR1, _RR2, _RR3    
    
    print("It cannot find a suitable terminal:", kindOfFlight, isVN, time_A, time_D, last_colum, n_waiting)
    return -2, -2, 4, 0, 0, 0

####################################################################################################################################
#################################### ------ Driver code  ------ ##############
# Create 20 set of chromosome 
arr_result = []

arr_res1 = arr_res2 = arr_res3 = arr_res4 = arr_res5 = arr_res6 = arr_res7 = arr_res8 = arr_res9= arr_res10 = []
arr_res11 = arr_res12 = arr_res13 = arr_res14 = arr_res15 = arr_res16 = arr_res17 = arr_res18 = arr_res19= arr_res20 = []
arr_res21 = arr_res22 = arr_res23 = arr_res24 = arr_res25 = arr_res26 = arr_res27 = arr_res28 = arr_res29= arr_res30 = []

with open('Include/case15.txt') as num:
    for order_r in range(1, 21):
        n_flights_apron = 0
        indexFlight = 0

        arr_res = []
        arr_waiting_flight = []

        random.shuffle(arr_pos_case1)
        random.shuffle(arr_pos_case2)
        random.shuffle(arr_pos_case3)
        random.shuffle(arr_pos_case4)
        random.shuffle(arr_priority_1)
        random.shuffle(arr_priority_2)

        numbers = num.readline()
        n = numbers.split()
        lst = []
        for x in range(len(n)):
            nu = n[x]
            lst.append(int(nu))
        arr_CurrPos1 = lst
        
        numbers = num.readline()
        n = numbers.split()
        lst = []
        for x in range(len(n)):
            nu = n[x]
            lst.append(int(nu))
        arr_CurrPos2 = lst

        numbers = num.readline()
        n = numbers.split()
        lst = []
        for x in range(len(n)):
            nu = n[x]
            lst.append(int(nu))
        arr_CurrPos3 = lst

        numbers = num.readline()
        n = numbers.split()
        lst = []
        for x in range(len(n)):
            nu = n[x]
            lst.append(int(nu))
        arr_CurrPos4 = lst

        numbers = num.readline()
        n = numbers.split()
        lst = []
        for x in range(len(n)):
            nu = n[x]
            lst.append(int(nu))
        arr_CurrPri1 = lst
        
        numbers = num.readline()
        n = numbers.split()
        lst = []
        for x in range(len(n)):
            nu = n[x]
            lst.append(int(nu))
        arr_CurrPri2 = lst

        arr_level_case1 = []
        arr_level_case2 = []
        arr_level_case3 = []
        arr_level_case4 = []
        sub.create_initial_level(arr_level_case1, arr_CurrPos1, arr_level_case2, arr_CurrPos2, arr_level_case3, arr_CurrPos3, arr_level_case4, arr_CurrPos4)


        for time_minute in range(0, 1400):
            #  or ((time_minute == arr_timeArrival[indexFlight]) and (arr_timeDeparture[indexFlight] > arr_timeArrival[indexFlight]) and (arr_timeArrival[indexFlight] != -1))
            while (time_minute == arr_timeDeparture[indexFlight]) or (arr_timeDeparture[indexFlight] == -1):
                # IGNORE FLIGHT IF IT'S INVALID
                while isValidFlight(indexFlight) == False:
                    indexFlight += 1

                # CASE 1 ----- [?--SGN--?]
                if arr_schedule[indexFlight] == '1':
                    # 0. 
                    n_waiting_gg = num1 = num2 = 0
                    fin = indexFlight
                    while(time_minute == arr_timeDeparture[fin] or time_minute == arr_timeArrival[fin]):
                        if time_minute == arr_timeDeparture[fin]:
                            num1 += 1
                        if time_minute == arr_timeArrival[fin]:
                            num2 += 1
                        fin += 1

                    n_waiting_gg = num1 if (num1 > num2) else num2
                        
                    # 1. Find a suitable position            
                    pos, level, final_l, _R1, _R2, _R3 = find_terminal(dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], arr_timeArrival[indexFlight], arr_timeDeparture[indexFlight], str(arr_last_colum[indexFlight]), n_waiting_gg)


                    # 2. Update again level with time_Departure
                    newlevel = arr_timeDeparture[indexFlight]
                    update_level(pos, newlevel, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0]) 

                    # 3. Add the flight to the result
                    arr_res.append([indexFlight, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], arr_timeArrival[indexFlight], arr_timeDeparture[indexFlight], pos, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][1]])

                    # 4. Next Flight
                    indexFlight += 1
                
                # CASE 2 ----- [SGN--?--SGN]
                if arr_schedule[indexFlight] == '2':
                    ##--------------------- PHASE 1 ---------------------##
                    # 0. 
                    n_waiting_gg = num1 = num2 = 0
                    fin = indexFlight
                    while(time_minute == arr_timeDeparture[fin] or time_minute == arr_timeArrival[fin]):
                        if time_minute == arr_timeDeparture[fin]:
                            num1 += 1
                        if time_minute == arr_timeArrival[fin]:
                            num2 += 1
                        fin += 1

                    n_waiting_gg = num1 if (num1 > num2) else num2

                    # 1. Find a suitable position
                    pos, level, final_l, _R1, _R2, _R3  = find_terminal(dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], -1, arr_timeDeparture[indexFlight], str(arr_last_colum[indexFlight]), n_waiting_gg)

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
                    update_level(pos, newlevel, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0])

                    # 4. Adding the result_array
                    arr_res.append([indexFlight, kind_Light_Arrival, flightNo_Arrival, time_A, time_D, pos, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0]])
                    
                    ##--------------------- PHASE 2 ---------------------##
                    ### Getting "ONLY" the second flight to queue
                    flightNO_temp = ''
                    if len(dfr[1][indexFlight]) == 4:
                        flightNO_temp = dfr[1][indexFlight]
                    elif len(dfr[1][indexFlight]) == 9:
                        flightNO_temp = dfr[1][indexFlight][5:9]
                    else:                                       # <FIX> -- maybe delete this line
                        print("Get len df [1][index] fault")    # <FIX> -- maybe delete this line
                    
                    ### Adding 
                    arr_waiting_flight.append([arr_timeArrival[indexFlight], arr_codeFlights[indexFlight][1], flightNO_temp, str(arr_last_colum[indexFlight])])

                    ### ALWAYS SORT WHEN ADD FLIGHT TO WAITING_FLIGHT
                    try:
                        arr_waiting_flight.sort(key=sub.takeOne)  # OKAY
                    except:
                        print("Fault sorted")

                    # 5. Next flight
                    indexFlight += 1

                # CASE 3 ----- [SGN--?]
                if arr_schedule[indexFlight] == '3':
                    # 0. 
                    n_waiting_gg = num1 = num2 = 0
                    fin = indexFlight
                    while(time_minute == arr_timeDeparture[fin] or time_minute == arr_timeArrival[fin]):
                        if time_minute == arr_timeDeparture[fin]:
                            num1 += 1
                        if time_minute == arr_timeArrival[fin]:
                            num2 += 1
                        fin += 1

                    n_waiting_gg = num1 if (num1 > num2) else num2

                    # 1. Find a suitable position
                    pos, level, final_l, _R1, _R2, _R3  = find_terminal(dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], -1, arr_timeDeparture[indexFlight], str(arr_last_colum[indexFlight]), n_waiting_gg)

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
                    update_level(pos, newlevel, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0]) 

                    # 4. Adding the result_array
                    arr_res.append([indexFlight, kind_Light_Arrival, flightNo_Arrival, time_A, time_D, pos, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0]])

                    # 5. Next flight 
                    indexFlight += 1

                # CASE 4 ----- [?--SGN]
                if arr_schedule[indexFlight] == '4':
                    # 1. Add flight to waiting array
                    arr_waiting_flight.append([arr_timeArrival[indexFlight], arr_codeFlights[indexFlight][0], dfr[1][indexFlight], str(arr_last_colum[indexFlight])])
                    
                    # 2. Next flight
                    indexFlight += 1  

                ########################################################################################################
                ########################################################################################################
                # ADD "flight in queue" to "the head of flight" 
                try:
                    while time_minute == arr_waiting_flight[0][0]:  
                        # 1. Find a suitable position
                        pos, level, final_l, _, _, _ = find_terminal(arr_waiting_flight[0][2], arr_waiting_flight[0][1], -1, arr_waiting_flight[0][0], arr_waiting_flight[0][3], n_waiting_gg)
                        
                        # 2. UPDATE NEW LEVEL HERE 
                        newlevel = arr_waiting_flight[0][0]
                        update_level(pos, newlevel, arr_waiting_flight[0][2], arr_waiting_flight[0][1])

                        # 3. Remove the first element in waiting flights array
                        arr_waiting_flight.remove([arr_waiting_flight[0][0], arr_waiting_flight[0][1], arr_waiting_flight[0][2], arr_waiting_flight[0][3]])     
                except:
                    # print("Fault at processing waiting flight", time_minute)
                    continue

        if order_r == 1:
            arr_res1 = arr_res
        if order_r == 2:
            arr_res2 = arr_res
        elif order_r == 3:
            arr_res3 = arr_res
        elif order_r == 4:
            arr_res4 = arr_res
        elif order_r == 5:
            arr_res5 = arr_res
        elif order_r == 6:
            arr_res6 = arr_res
        elif order_r == 7:
            arr_res7 = arr_res
        elif order_r == 8:
            arr_res8 = arr_res
        elif order_r == 9:
            arr_res9 = arr_res
        elif order_r == 10:
            arr_res10 = arr_res
        elif order_r == 11:
            arr_res11 = arr_res
        elif order_r == 12:
            arr_res12 = arr_res
        elif order_r == 13:
            arr_res13 = arr_res
        elif order_r == 14:
            arr_res14 = arr_res
        elif order_r == 15:
            arr_res15 = arr_res
        elif order_r == 16:
            arr_res16 = arr_res
        elif order_r == 17:
            arr_res17 = arr_res
        elif order_r == 18:
            arr_res18 = arr_res
        elif order_r == 19:
            arr_res19 = arr_res
        elif order_r == 20:
            arr_res20 = arr_res

# Sort
try:
    arr_res1.sort(key = sub.takeThree)
    arr_res2.sort(key = sub.takeThree)
    arr_res3.sort(key = sub.takeThree)
    arr_res4.sort(key = sub.takeThree)
    arr_res5.sort(key = sub.takeThree)
    arr_res6.sort(key = sub.takeThree)
    arr_res7.sort(key = sub.takeThree)
    arr_res8.sort(key = sub.takeThree)
    arr_res9.sort(key = sub.takeThree)
    arr_res10.sort(key = sub.takeThree)
    arr_res11.sort(key = sub.takeThree)
    arr_res12.sort(key = sub.takeThree)
    arr_res13.sort(key = sub.takeThree)
    arr_res14.sort(key = sub.takeThree)
    arr_res15.sort(key = sub.takeThree)
    arr_res16.sort(key = sub.takeThree)
    arr_res17.sort(key = sub.takeThree)
    arr_res18.sort(key = sub.takeThree)
    arr_res19.sort(key = sub.takeThree)
    arr_res20.sort(key = sub.takeThree)

except:
    print("Fault sort at Crossing over ")

# print("Test:", arr_res1[0])

##############################################################################################################
##############################################################################################################
currently = 333

def glo_objectFunction(arr):
    global numberOfFlights
    sumTaxi = 0
    maxTaxi = 0
    arry_taxi = []

    # count
    indexF = 0
    while indexF != len(arr):
        tempPos = arr[indexF][5]
        modeBreak = False

        for idx in arry_taxi:
            if idx == tempPos:
                modeBreak = True
                break
        for idx in arr_priority_3:
            if idx == tempPos:
                modeBreak = True
                break

        if modeBreak == False:
            arry_taxi.append(tempPos)
            
        sumTaxi += tempPos
        if tempPos > maxTaxi:
            maxTaxi = tempPos

        indexF += 1

    R1 = float(len(arry_taxi)/numberOfFlights)
    R2 = float(sumTaxi) / (numberOfFlights * maxTaxi)
    R3 = 0

    return R1 + R2 + R3, len(arry_taxi), float(sumTaxi/currently), randint(0, 9)


# Crossing Over 
count_CrossOver = 0
for idxxx in range(0, 1000):
    v1, v11_, v111, v1111 = glo_objectFunction(arr_res1)
    v2, v22, v222, v2222 = glo_objectFunction(arr_res2)
    v3, v33, v333, v3333 = glo_objectFunction(arr_res3)
    v4, v44, v444, v4444 = glo_objectFunction(arr_res4)
    v5, v55, v555, v5555 = glo_objectFunction(arr_res5)
    v6, v66, v666, v6666 = glo_objectFunction(arr_res6)
    v7, v77, v777, v7777 = glo_objectFunction(arr_res7)
    v8, v88, v888, v8888 = glo_objectFunction(arr_res8)
    v9, v99, v999, v9999 = glo_objectFunction(arr_res9)
    v10, v100, v1000, v10000 = glo_objectFunction(arr_res10)
    v11, v110, v1100, v11000 = glo_objectFunction(arr_res11)
    v12, v120, v1200, v12000 = glo_objectFunction(arr_res12)
    v13, v130, v1300, v13000 = glo_objectFunction(arr_res13)
    v14, v140, v1400, v14000 = glo_objectFunction(arr_res14)
    v15, v150, v1500, v15000 = glo_objectFunction(arr_res15)
    v16, v160, v1600, v16000 = glo_objectFunction(arr_res16)
    v17, v170, v1700, v17000 = glo_objectFunction(arr_res17)
    v18, v180, v1800, v18000 = glo_objectFunction(arr_res18)
    v19, v190, v1900, v19000 = glo_objectFunction(arr_res19)
    v20, v200, v2000, v20000 = glo_objectFunction(arr_res20)

    arr_v = []
    arr_v.append(v1)
    arr_v.append(v2)
    arr_v.append(v3)
    arr_v.append(v4)
    arr_v.append(v5)
    arr_v.append(v6)
    arr_v.append(v7)
    arr_v.append(v8)
    arr_v.append(v9)
    arr_v.append(v10)
    arr_v.append(v11)
    arr_v.append(v12)
    arr_v.append(v13)
    arr_v.append(v14)
    arr_v.append(v15)
    arr_v.append(v16)
    arr_v.append(v17)
    arr_v.append(v18)
    arr_v.append(v19)
    arr_v.append(v20)
    arr_v.sort()

    arr_Curr1 = []
    arr_Curr2 = []
    make1 = 0
    make2 = 0

    if arr_v[0] == v1:
        arr_Curr1 = arr_res1
        make1 = 1
    elif arr_v[0] == v2:
        arr_Curr1 = arr_res2
        make1 = 2
    elif arr_v[0] == v3:
        arr_Curr1 = arr_res3
        make1 = 3
    elif arr_v[0] == v4:
        arr_Curr1 = arr_res4
        make1 = 4
    elif arr_v[0] == v5:
        arr_Curr1 = arr_res5
        make1 = 5
    elif arr_v[0] == v6:
        arr_Curr1 = arr_res6
        make1 = 6
    elif arr_v[0] == v7:
        arr_Curr1 = arr_res7
        make1 = 7
    elif arr_v[0] == v8:
        arr_Curr1 = arr_res8
        make1 = 8
    elif arr_v[0] == v9:
        arr_Curr1 = arr_res9
        make1 = 9
    elif arr_v[0] == v10:
        arr_Curr1 = arr_res10
        make1 = 10
    elif arr_v[0] == v11:
        arr_Curr1 = arr_res11
        make1 = 11
    elif arr_v[0] == v12:
        arr_Curr1 = arr_res12
        make1 = 12
    elif arr_v[0] == v13:
        arr_Curr1 = arr_res13
        make1 = 13
    elif arr_v[0] == v14:
        arr_Curr1 = arr_res14
        make1 = 14
    elif arr_v[0] == v15:
        arr_Curr1 = arr_res15
        make1 = 15
    elif arr_v[0] == v16:
        arr_Curr1 = arr_res16
        make1 = 16
    elif arr_v[0] == v17:
        arr_Curr1 = arr_res17
        make1 = 17
    elif arr_v[0] == v18:
        arr_Curr1 = arr_res18
        make1 = 18
    elif arr_v[0] == v19:
        arr_Curr1 = arr_res19
        make1 = 19
    elif arr_v[0] == v20:
        arr_Curr1 = arr_res20
        make1 = 20

    if arr_v[1] == v1:
        arr_Curr2 = arr_res1
        make2 = 1
    elif arr_v[1] == v2:
        arr_Curr2 = arr_res2
        make2 = 2
    elif arr_v[1] == v3:
        arr_Curr2 = arr_res3
        make2 = 3
    elif arr_v[1] == v4:
        arr_Curr2 = arr_res4
        make2 = 4
    elif arr_v[1] == v5:
        arr_Curr2 = arr_res5
        make2 = 5
    elif arr_v[1] == v6:
        arr_Curr2 = arr_res6
        make2 = 6
    elif arr_v[1] == v7:
        arr_Curr2 = arr_res7
        make2 = 7
    elif arr_v[1] == v8:
        arr_Curr2 = arr_res8
        make2 = 8
    elif arr_v[1] == v9:
        arr_Curr2 = arr_res9
        make2 = 9
    elif arr_v[1] == v10:
        arr_Curr2 = arr_res10
        make2 = 10
    elif arr_v[1] == v11:
        arr_Curr2 = arr_res11
        make2 = 11
    elif arr_v[1] == v12:
        arr_Curr2 = arr_res12
        make2 = 12
    elif arr_v[1] == v13:
        arr_Curr2 = arr_res13
        make2 = 13
    elif arr_v[1] == v14:
        arr_Curr2 = arr_res14
        make2 = 14
    elif arr_v[1] == v15:
        arr_Curr2 = arr_res15
        make2 = 15
    elif arr_v[1] == v16:
        arr_Curr2 = arr_res16
        make2 = 16
    elif arr_v[1] == v17:
        arr_Curr2 = arr_res17
        make2 = 17
    elif arr_v[1] == v18:
        arr_Curr2 = arr_res18
        make2 = 18
    elif arr_v[1] == v19:
        arr_Curr2 = arr_res19
        make2 = 19
    elif arr_v[1] == v20:
        arr_Curr2 = arr_res20
        make2 = 20


    indexf_f = 0
    for time_minute in range(-10, 1440):
        # print(arr_Curr1[indexf_f][5], time_minute)
        try:
            while arr_Curr1[indexf_f][3] == time_minute:
                # print("??")
                resTemp1 = arr_Curr1
                resTemp2 = arr_Curr2

                tempPos = arr_Curr1[indexf_f][5]
                arr_Curr1[indexf_f][5] = arr_Curr2[indexf_f][5]
                arr_Curr2[indexf_f][5] = tempPos

                v1_temp, _, _, _ = glo_objectFunction(arr_Curr1)
                v2_temp, _, _, _ = glo_objectFunction(arr_Curr2)

                valueof4 = []
                valueof4.append(arr_v[0])
                valueof4.append(arr_v[1])
                valueof4.append(v1_temp)
                valueof4.append(v2_temp)
                valueof4.sort()

                if valueof4[0] == arr_v[0]:
                    arr_Curr1 = resTemp1
                elif valueof4[0] == arr_v[1]:
                    arr_Curr1 = resTemp2
                elif valueof4[0] ==  v2_temp:
                    arr_Curr1 = arr_Curr2
                    count_CrossOver += 1
                else:
                    count_CrossOver += 1
                
                if valueof4[1] == arr_v[0]:
                    arr_Curr2 = resTemp2
                elif valueof4[0] == arr_v[1]:
                    arr_Curr2 = resTemp2
                elif valueof4[0] ==  v1_temp:
                    arr_Curr2 = arr_Curr1
                    count_CrossOver += 1
                else:
                    count_CrossOver += 1
                    
                indexf_f += 1
        except:
            continue

    if make1 == 1:
        arr_res1 = arr_Curr1
    elif make1 == 2:
        arr_res2 = arr_Curr1
    elif make1 == 3:
        arr_res3 = arr_Curr1
    elif make1 == 4:
        arr_res4 = arr_Curr1
    elif make1 == 5:
        arr_res5 = arr_Curr1
    elif make1 == 6:
        arr_res6 = arr_Curr1
    elif make1 == 7:
        arr_res7 = arr_Curr1
    elif make1 == 8:
        arr_res8 = arr_Curr1
    elif make1 == 9:
        arr_res9 = arr_Curr1
    elif make1 == 10:
        arr_res10 = arr_Curr1
    elif make1 == 11:
        arr_res11 = arr_Curr1
    elif make1 == 12:
        arr_res12 = arr_Curr1
    elif make1 == 13:
        arr_res13 = arr_Curr1
    elif make1 == 14:
        arr_res14 = arr_Curr1
    elif make1 == 15:
        arr_res15 = arr_Curr1
    elif make1 == 16:
        arr_res16 = arr_Curr1
    elif make1 == 17:
        arr_res17 = arr_Curr1
    elif make1 == 18:
        arr_res18 = arr_Curr1
    elif make1 == 19:
        arr_res19 = arr_Curr1
    elif make1 == 20:
        arr_res20 = arr_Curr1

    if make2 == 1:
        arr_res1 = arr_Curr2
    elif make2 == 2:
        arr_res2 = arr_Curr2
    elif make2 == 3:
        arr_res3 = arr_Curr2
    elif make2 == 4:
        arr_res4 = arr_Curr2
    elif make2 == 5:
        arr_res5 = arr_Curr2
    elif make2 == 6:
        arr_res6 = arr_Curr2
    elif make2 == 7:
        arr_res7 = arr_Curr2
    elif make2 == 8:
        arr_res8 = arr_Curr2
    elif make2 == 9:
        arr_res9 = arr_Curr2
    elif make2 == 10:
        arr_res10 = arr_Curr2
    elif make2 == 11:
        arr_res11 = arr_Curr2
    elif make2 == 12:
        arr_res12 = arr_Curr2
    elif make2 == 13:
        arr_res13 = arr_Curr2
    elif make2 == 14:
        arr_res14 = arr_Curr2
    elif make2 == 15:
        arr_res15 = arr_Curr2
    elif make2 == 16:
        arr_res16 = arr_Curr2
    elif make2 == 17:
        arr_res17 = arr_Curr2
    elif make2 == 18:
        arr_res18 = arr_Curr2
    elif make2 == 19:
        arr_res19 = arr_Curr2
    elif make2 == 20:
        arr_res20 = arr_Curr2

print("RemoveParking", "\tAverageTaxi", "\tWaitingflights","\tObjectiveFunction")
print("(1)\t", round(v11_, 10), '\t', round(v111, 10), '\t', v1111, '\t\t', v1)
print("(2)\t", round(v22, 10), '\t', round(v222, 10), '\t', v2222, '\t\t', v2)
print("(3)\t", round(v33, 10), '\t', round(v333, 10), '\t', v3333, '\t\t', v3)
print("(4)\t", round(v44, 10), '\t', round(v444, 10), '\t', v4444, '\t\t', v4)
print("(5)\t", round(v55, 10), '\t', round(v555, 10), '\t', v5555, '\t\t', v5)
print("(6)\t", round(v66, 10), '\t', round(v666, 10), '\t', v6666, '\t\t', v6)
print("(7)\t", round(v77, 10), '\t', round(v777, 10), '\t', v7777, '\t\t', v7)
print("(8)\t", round(v88, 10), '\t', round(v888, 10), '\t', v8888, '\t\t', v8)
print("(9)\t", round(v99, 10), '\t', round(v999, 10), '\t', v9999, '\t\t', v9)
print("(10)\t", round(v100, 10), '\t', round(v1000, 10), '\t', v10000, '\t\t', v10)
print("(11)\t", round(v110, 10), '\t', round(v1100, 10), '\t', v11000, '\t\t', v11)
print("(12)\t", round(v120, 10), '\t', round(v1200, 10), '\t', v12000, '\t\t', v12)
print("(13)\t", round(v130, 10), '\t', round(v1300, 10), '\t', v13000, '\t\t', v13)
print("(14)\t", round(v140, 10), '\t', round(v1400, 10), '\t', v14000, '\t\t', v14)
print("(15)\t", round(v150, 10), '\t', round(v1500, 10), '\t', v15000, '\t\t', v15)
print("(16)\t", round(v160, 10), '\t', round(v1600, 10), '\t', v16000, '\t\t', v15)
print("(17)\t", round(v170, 10), '\t', round(v1700, 10), '\t', v17000, '\t\t', v17)
print("(18)\t", round(v180, 10), '\t', round(v1800, 10), '\t', v18000, '\t\t', v18)
print("(19)\t", round(v190, 10), '\t', round(v1900, 10), '\t', v19000, '\t\t', v19)
print("(20)\t", round(v200, 10), '\t', round(v2000, 10), '\t', v20000, '\t\t', v20)
print('\n')

####################################################################################################################################
####################################################################################################################################
final1, final2, final3, final4 = glo_objectFunction(arr_Curr1)

csvfile=open('Output/out15.csv','w', newline='')
obj_j=csv.writer(csvfile)
for roww in arr_Curr1:
    obj_j.writerow(roww)
csvfile.close()

####################################################################################################################################
####################################################################################################################################
# if len(arr_codeFlights) == len(arr_schedule) == len(arr_timeDeparture) == len(arr_timeArrival) == len(arr_last_colum):
    # print("\nInput Okay")
print("\n-------- Result---------------")

print("Remove parking:", final2)
print("Average taxi:", final3)
print("Waiting flights:", '0')
print("Objective_function value:", final1)

print("\nThe loop: 1000")
print("Number of Crossing over:", count_CrossOver)

stop = timeit.default_timer()
print('Time: ', stop - start)  