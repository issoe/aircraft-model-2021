####################################################################################################################################
#################################### ------ Import library  ------ #################################################################
# from Users.khanhquang.Downloads.AirCraft_MODEL.Again.sub import takeThree
import sub
import pandas as pd
import numpy as np
import re
import random


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

glo_value_ObjectiveFunction = 0
glo_count_CallObjective = 0
glo_removeParking = 0
arr_statictis = []
####################################################################################################################################
#################################### ------ MEASURE TIME EXECUTION  ------ #########################################################
import timeit
start = timeit.default_timer()

####################################################################################################################################
#################################### ------ DATA FRAME ARRAY --> dfr ------ #########################################################
# NOTE: DATA INPUT MUST BE SORTED
# 1. Read data from file "input.csv" and get the numberOfFlighs
dfr = pd.read_csv('input.csv', sep=';', header=None)
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
sub.create_initial_level(arr_level_case1, len(arr_pos_case1), arr_level_case2, len(arr_pos_case2), arr_level_case3, len(arr_pos_case3), arr_level_case4, len(arr_pos_case4))

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

for order_r in range(1, 21):
    n_flights_apron = 0
    indexFlight = 0
    glo_value_ObjectiveFunction = 0
    glo_count_CallObjective = 0
    glo_removeParking = 0

    arr_res = []
    arr_waiting_flight = []

    arr_level_case1 = []
    arr_level_case2 = []
    arr_level_case3 = []
    arr_level_case4 = []
    sub.create_initial_level(arr_level_case1, len(arr_pos_case1), arr_level_case2, len(arr_pos_case2), arr_level_case3, len(arr_pos_case3), arr_level_case4, len(arr_pos_case4))

    random.shuffle(arr_pos_case1)
    random.shuffle(arr_pos_case2)
    random.shuffle(arr_pos_case3)
    random.shuffle(arr_pos_case4)
    random.shuffle(arr_priority_1)
    random.shuffle(arr_priority_2)

    arr_CurrPos1 = arr_pos_case1
    arr_CurrPos2 = arr_pos_case2
    arr_CurrPos3 = arr_pos_case3
    arr_CurrPos4 = arr_pos_case4
    arr_CurrPri1 = arr_priority_1
    arr_CurrPri2 = arr_priority_2

    for time_minute in range(0, 1440):
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
                glo_value_ObjectiveFunction += final_l
                glo_count_CallObjective += 1

                # 2. Update again level with time_Departure
                newlevel = arr_timeDeparture[indexFlight]
                update_level(pos, newlevel, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0]) 

                # 3. Add the flight to the result
                arr_res.append([indexFlight, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], arr_timeArrival[indexFlight], arr_timeDeparture[indexFlight], pos, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][1], _R1, _R2, _R3, round(final_l, 8)])

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
                glo_value_ObjectiveFunction += final_l
                glo_count_CallObjective += 1

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
                arr_res.append([indexFlight, kind_Light_Arrival, flightNo_Arrival, time_A, time_D, pos, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], _R1, _R2, _R3, round(final_l, 8)])
                
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
                glo_value_ObjectiveFunction += final_l
                glo_count_CallObjective += 1

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
                arr_res.append([indexFlight, kind_Light_Arrival, flightNo_Arrival, time_A, time_D, pos, dfr[1][indexFlight][0:4], arr_codeFlights[indexFlight][0], _R1, _R2, _R3, round(final_l, 8)])

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
                print("Fault at processing waiting flight", time_minute)

    # Statistics
    glo_removeParking, sumTaxi = sub.count_removeParking(arr_CurrPos1, arr_CurrPos2, arr_CurrPos3, arr_CurrPos4, arr_level_case1, arr_level_case2, arr_level_case3, arr_level_case4, arr_priority_3)

    arr_statictis.append([glo_removeParking, glo_value_ObjectiveFunction, glo_count_CallObjective, sumTaxi])


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

# Crossing Over 
count_CrossOver = 0
indexFlight_t = 0
arr_result = arr_res1
arr_final_result = []

while arr_result[indexFlight_t][3] == -5:
    arr_final_result.append([indexFlight_t + 1, arr_result[indexFlight_t][1], arr_result[indexFlight_t][2], arr_result[indexFlight_t][3], arr_result[indexFlight_t][4], arr_result[indexFlight_t][5], arr_result[indexFlight_t][6], arr_result[indexFlight_t][7]])
    indexFlight_t += 1

for time_minute in range(0, 1440):
    while time_minute == arr_result[indexFlight_t][3]:        
        v1 = glo_Objective_Function(indexFlight_t, arr_res1, arr_res2[indexFlight_t][1], arr_res2[indexFlight_t][2], arr_statictis[0])
        v2 = glo_Objective_Function(indexFlight_t, arr_res2, arr_res1[indexFlight_t][1], arr_res1[indexFlight_t][2], arr_statictis[1])
        v3 = (arr_statictis[0][1])/arr_statictis[0][2]
        v4 = (arr_statictis[1][1])/arr_statictis[1][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res1 = arr_res2
            arr_statictis[0] = arr_statictis[1]
        elif max_value == v1 or max_value == v2:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res1, arr_res2)
            if max_value == v2:
                arr_statictis[0] = arr_statictis[1]
                arr_res1 = arr_res2

        v1 = glo_Objective_Function(indexFlight_t, arr_res3, arr_res4[indexFlight_t][1], arr_res4[indexFlight_t][2], arr_statictis[2])
        v2 = glo_Objective_Function(indexFlight_t, arr_res4, arr_res3[indexFlight_t][1], arr_res3[indexFlight_t][2], arr_statictis[3])
        v3 = (arr_statictis[2][1])/arr_statictis[2][2]
        v4 = (arr_statictis[3][1])/arr_statictis[3][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_statictis[1] = arr_statictis[3]
            arr_res2 = arr_res4
        elif max_value == v3:
            arr_res2 = arr_res3
            arr_statictis[1] = arr_statictis[2]
        elif max_value == v1:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res3, arr_res4)
            arr_res2 = arr_res3
            arr_statictis[1] = arr_statictis[2]
        else:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res3, arr_res4)
            arr_res2 = arr_res4
            arr_statictis[1] = arr_statictis[3]
            

        v1 = glo_Objective_Function(indexFlight_t, arr_res5, arr_res6[indexFlight_t][1], arr_res6[indexFlight_t][2], arr_statictis[4])
        v2 = glo_Objective_Function(indexFlight_t, arr_res6, arr_res5[indexFlight_t][1], arr_res5[indexFlight_t][2], arr_statictis[5])
        v3 = (arr_statictis[4][1])/arr_statictis[4][2]
        v4 = (arr_statictis[5][1])/arr_statictis[5][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res3 = arr_res6
            arr_statictis[2] = arr_statictis[5]
        elif max_value == v3:
            arr_res3 = arr_res5
            arr_statictis[2] = arr_statictis[4]
        elif max_value == v1:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res5, arr_res6)
            arr_res3 = arr_res5
            arr_statictis[2] = arr_statictis[4]
        else:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res5, arr_res6)
            arr_res3 = arr_res6
            arr_statictis[2] = arr_statictis[5]

        v1 = glo_Objective_Function(indexFlight_t, arr_res7, arr_res8[indexFlight_t][1], arr_res8[indexFlight_t][2], arr_statictis[6])
        v2 = glo_Objective_Function(indexFlight_t, arr_res8, arr_res7[indexFlight_t][1], arr_res7[indexFlight_t][2], arr_statictis[7])
        v3 = (arr_statictis[6][1])/arr_statictis[6][2]  
        v4 = (arr_statictis[7][1])/arr_statictis[7][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res4 = arr_res8
            arr_statictis[3] = arr_statictis[7]
        elif max_value == v3:
            arr_res4 = arr_res7
            arr_statictis[3] = arr_statictis[6]
        elif max_value == v1:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res7, arr_res8)
            arr_res4 = arr_res7
            arr_statictis[3] = arr_statictis[6]
        else:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res7, arr_res8)
            arr_res4 = arr_res8
            arr_statictis[3] = arr_statictis[7]

        v1 = glo_Objective_Function(indexFlight_t, arr_res9, arr_res10[indexFlight_t][1], arr_res10[indexFlight_t][2], arr_statictis[8])
        v2 = glo_Objective_Function(indexFlight_t, arr_res10, arr_res9[indexFlight_t][1], arr_res9[indexFlight_t][2], arr_statictis[9])
        v3 = (arr_statictis[8][1])/arr_statictis[8][2]  
        v4 = (arr_statictis[9][1])/arr_statictis[9][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res5 = arr_res10
            arr_statictis[4] = arr_statictis[9]
        elif max_value == v3:
            arr_res5 = arr_res9
            arr_statictis[4] = arr_statictis[8]
        elif max_value == v1:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res9, arr_res10)
            arr_res5 = arr_res9
            arr_statictis[4] = arr_statictis[8]
        else:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res9, arr_res10)
            arr_res5 = arr_res10
            arr_statictis[4] = arr_statictis[9]

        v1 = glo_Objective_Function(indexFlight_t, arr_res11, arr_res12[indexFlight_t][1], arr_res12[indexFlight_t][2], arr_statictis[10])
        v2 = glo_Objective_Function(indexFlight_t, arr_res12, arr_res11[indexFlight_t][1], arr_res11[indexFlight_t][2], arr_statictis[11])
        v3 = (arr_statictis[10][1])/arr_statictis[10][2]  
        v4 = (arr_statictis[11][1])/arr_statictis[11][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res6 = arr_res12
            arr_statictis[5] = arr_statictis[11]
        elif max_value == v3:
            arr_res6 = arr_res11
            arr_statictis[5] = arr_statictis[10]
        elif max_value == v1:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res11, arr_res12)
            arr_res6 = arr_res11
            arr_statictis[5] = arr_statictis[10]
        else:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res11, arr_res12)
            arr_res6 = arr_res12
            arr_statictis[5] = arr_statictis[11]

        v1 = glo_Objective_Function(indexFlight_t, arr_res13, arr_res14[indexFlight_t][1], arr_res14[indexFlight_t][2], arr_statictis[12])
        v2 = glo_Objective_Function(indexFlight_t, arr_res14, arr_res13[indexFlight_t][1], arr_res13[indexFlight_t][2], arr_statictis[13])
        v3 = (arr_statictis[12][1])/arr_statictis[12][2]  
        v4 = (arr_statictis[13][1])/arr_statictis[13][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res7 = arr_res14
            arr_statictis[6] = arr_statictis[13]
        elif max_value == v3:
            arr_res7 = arr_res13
            arr_statictis[6] = arr_statictis[12]
        elif max_value == v1:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res13, arr_res14)
            arr_res7 = arr_res13
            arr_statictis[6] = arr_statictis[12]
        else:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res13, arr_res14)
            arr_res7 = arr_res14
            arr_statictis[6] = arr_statictis[13]

        v1 = glo_Objective_Function(indexFlight_t, arr_res15, arr_res16[indexFlight_t][1], arr_res16[indexFlight_t][2], arr_statictis[14])
        v2 = glo_Objective_Function(indexFlight_t, arr_res16, arr_res15[indexFlight_t][1], arr_res15[indexFlight_t][2], arr_statictis[15])
        v3 = (arr_statictis[14][1])/arr_statictis[14][2]  
        v4 = (arr_statictis[15][1])/arr_statictis[15][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res8 = arr_res16
            arr_statictis[7] = arr_statictis[15]
        elif max_value == v3:
            arr_res8 = arr_res15
            arr_statictis[7] = arr_statictis[14]
        elif max_value == v1:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res15, arr_res16)
            arr_res8 = arr_res15
            arr_statictis[7] = arr_statictis[14]
        else:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res15, arr_res16)
            arr_res8 = arr_res16
            arr_statictis[7] = arr_statictis[15]    

        v1 = glo_Objective_Function(indexFlight_t, arr_res17, arr_res18[indexFlight_t][1], arr_res18[indexFlight_t][2], arr_statictis[16])
        v2 = glo_Objective_Function(indexFlight_t, arr_res18, arr_res17[indexFlight_t][1], arr_res17[indexFlight_t][2], arr_statictis[17])
        v3 = (arr_statictis[16][1])/arr_statictis[16][2]  
        v4 = (arr_statictis[17][1])/arr_statictis[17][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res9 = arr_res18
            arr_statictis[8] = arr_statictis[17]
        elif max_value == v3:
            arr_res9 = arr_res17
            arr_statictis[8] = arr_statictis[16]
        elif max_value == v1:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res17, arr_res18)
            arr_res9 = arr_res17
            arr_statictis[8] = arr_statictis[16]
        else:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res17, arr_res18)
            arr_res9 = arr_res18
            arr_statictis[8] = arr_statictis[17]

        v1 = glo_Objective_Function(indexFlight_t, arr_res19, arr_res20[indexFlight_t][1], arr_res20[indexFlight_t][2], arr_statictis[18])
        v2 = glo_Objective_Function(indexFlight_t, arr_res20, arr_res19[indexFlight_t][1], arr_res19[indexFlight_t][2], arr_statictis[19])
        v3 = (arr_statictis[18][1])/arr_statictis[18][2]  
        v4 = (arr_statictis[19][1])/arr_statictis[19][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res10 = arr_res20
            arr_statictis[9] = arr_statictis[19]
        elif max_value == v3:
            arr_res10 = arr_res19
            arr_statictis[9] = arr_statictis[18]
        elif max_value == v1:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res19, arr_res20)
            arr_res10 = arr_res19
            arr_statictis[9] = arr_statictis[18]
        else:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res19, arr_res20)
            arr_res10 = arr_res20
            arr_statictis[9] = arr_statictis[19]
        ################################################################

        v1 = glo_Objective_Function(indexFlight_t, arr_res1, arr_res2[indexFlight_t][1], arr_res2[indexFlight_t][2], arr_statictis[0])
        v2 = glo_Objective_Function(indexFlight_t, arr_res2, arr_res1[indexFlight_t][1], arr_res1[indexFlight_t][2], arr_statictis[1])
        v3 = (arr_statictis[0][1])/arr_statictis[0][2]
        v4 = (arr_statictis[1][1])/arr_statictis[1][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res1 = arr_res2
            arr_statictis[0] = arr_statictis[1]
        elif max_value == v1 or max_value == v2:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res1, arr_res2)
            if max_value == v2:
                arr_statictis[0] = arr_statictis[1]
                arr_res1 = arr_res2

        v1 = glo_Objective_Function(indexFlight_t, arr_res3, arr_res4[indexFlight_t][1], arr_res4[indexFlight_t][2], arr_statictis[2])
        v2 = glo_Objective_Function(indexFlight_t, arr_res4, arr_res3[indexFlight_t][1], arr_res3[indexFlight_t][2], arr_statictis[3])
        v3 = (arr_statictis[2][1])/arr_statictis[2][2]
        v4 = (arr_statictis[3][1])/arr_statictis[3][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_statictis[1] = arr_statictis[3]
            arr_res2 = arr_res4
        elif max_value == v3:
            arr_res2 = arr_res3
            arr_statictis[1] = arr_statictis[2]
        elif max_value == v1:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res3, arr_res4)
            arr_res2 = arr_res3
            arr_statictis[1] = arr_statictis[2]
        else:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res3, arr_res4)
            arr_res2 = arr_res4
            arr_statictis[1] = arr_statictis[3]
            

        v1 = glo_Objective_Function(indexFlight_t, arr_res5, arr_res6[indexFlight_t][1], arr_res6[indexFlight_t][2], arr_statictis[4])
        v2 = glo_Objective_Function(indexFlight_t, arr_res6, arr_res5[indexFlight_t][1], arr_res5[indexFlight_t][2], arr_statictis[5])
        v3 = (arr_statictis[4][1])/arr_statictis[4][2]
        v4 = (arr_statictis[5][1])/arr_statictis[5][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res3 = arr_res6
            arr_statictis[2] = arr_statictis[5]
        elif max_value == v3:
            arr_res3 = arr_res5
            arr_statictis[2] = arr_statictis[4]
        elif max_value == v1:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res5, arr_res6)
            arr_res3 = arr_res5
            arr_statictis[2] = arr_statictis[4]
        else:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res5, arr_res6)
            arr_res3 = arr_res6
            arr_statictis[2] = arr_statictis[5]

        v1 = glo_Objective_Function(indexFlight_t, arr_res7, arr_res8[indexFlight_t][1], arr_res8[indexFlight_t][2], arr_statictis[6])
        v2 = glo_Objective_Function(indexFlight_t, arr_res8, arr_res7[indexFlight_t][1], arr_res7[indexFlight_t][2], arr_statictis[7])
        v3 = (arr_statictis[6][1])/arr_statictis[6][2]  
        v4 = (arr_statictis[7][1])/arr_statictis[7][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res4 = arr_res8
            arr_statictis[3] = arr_statictis[7]
        elif max_value == v3:
            arr_res4 = arr_res7
            arr_statictis[3] = arr_statictis[6]
        elif max_value == v1:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res7, arr_res8)
            arr_res4 = arr_res7
            arr_statictis[3] = arr_statictis[6]
        else:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res7, arr_res8)
            arr_res4 = arr_res8
            arr_statictis[3] = arr_statictis[7]

        v1 = glo_Objective_Function(indexFlight_t, arr_res9, arr_res10[indexFlight_t][1], arr_res10[indexFlight_t][2], arr_statictis[8])
        v2 = glo_Objective_Function(indexFlight_t, arr_res10, arr_res9[indexFlight_t][1], arr_res9[indexFlight_t][2], arr_statictis[9])
        v3 = (arr_statictis[8][1])/arr_statictis[8][2]  
        v4 = (arr_statictis[9][1])/arr_statictis[9][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res5 = arr_res10
            arr_statictis[4] = arr_statictis[9]
        elif max_value == v3:
            arr_res5 = arr_res9
            arr_statictis[4] = arr_statictis[8]
        elif max_value == v1:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res9, arr_res10)
            arr_res5 = arr_res9
            arr_statictis[4] = arr_statictis[8]
        else:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res9, arr_res10)
            arr_res5 = arr_res10
            arr_statictis[4] = arr_statictis[9]

        ################################################################
        
        v1 = glo_Objective_Function(indexFlight_t, arr_res1, arr_res2[indexFlight_t][1], arr_res2[indexFlight_t][2], arr_statictis[0])
        v2 = glo_Objective_Function(indexFlight_t, arr_res2, arr_res1[indexFlight_t][1], arr_res1[indexFlight_t][2], arr_statictis[1])
        v3 = (arr_statictis[0][1])/arr_statictis[0][2]
        v4 = (arr_statictis[1][1])/arr_statictis[1][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res1 = arr_res2
            arr_statictis[0] = arr_statictis[1]
        elif max_value == v1 or max_value == v2:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res1, arr_res2)
            if max_value == v2:
                arr_statictis[0] = arr_statictis[1]
                arr_res1 = arr_res2

        v1 = glo_Objective_Function(indexFlight_t, arr_res3, arr_res4[indexFlight_t][1], arr_res4[indexFlight_t][2], arr_statictis[2])
        v2 = glo_Objective_Function(indexFlight_t, arr_res4, arr_res3[indexFlight_t][1], arr_res3[indexFlight_t][2], arr_statictis[3])
        v3 = (arr_statictis[2][1])/arr_statictis[2][2]
        v4 = (arr_statictis[3][1])/arr_statictis[3][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_statictis[1] = arr_statictis[3]
            arr_res2 = arr_res4
        elif max_value == v3:
            arr_res2 = arr_res3
            arr_statictis[1] = arr_statictis[2]
        elif max_value == v1:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res3, arr_res4)
            arr_res2 = arr_res3
            arr_statictis[1] = arr_statictis[2]
        else:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res3, arr_res4)
            arr_res2 = arr_res4
            arr_statictis[1] = arr_statictis[3]

        ################################################################
        
        v1 = glo_Objective_Function(indexFlight_t, arr_res1, arr_res2[indexFlight_t][1], arr_res2[indexFlight_t][2], arr_statictis[0])
        v2 = glo_Objective_Function(indexFlight_t, arr_res2, arr_res1[indexFlight_t][1], arr_res1[indexFlight_t][2], arr_statictis[1])
        v3 = (arr_statictis[0][1])/arr_statictis[0][2]
        v4 = (arr_statictis[1][1])/arr_statictis[1][2]
        max_value = max(v1, v2, v3, v4)
        if max_value == v4:
            arr_res1 = arr_res2
            arr_statictis[0] = arr_statictis[1]
        elif max_value == v1 or max_value == v2:
            count_CrossOver += 1
            sub.swap_chromosome(indexFlight_t, arr_res1, arr_res2)
            if max_value == v2:
                arr_statictis[0] = arr_statictis[1]
                arr_res1 = arr_res2

        arr_final_result.append([indexFlight_t + 1, arr_res2[indexFlight_t][1], arr_res2[indexFlight_t][2], arr_res2[indexFlight_t][3], arr_res2[indexFlight_t][4], arr_res2[indexFlight_t][5], arr_res2[indexFlight_t][6], arr_res2[indexFlight_t][7]])
        indexFlight_t += 1

for row in arr_final_result:
    print(row)

####################################################################################################################################
####################################################################################################################################
if len(arr_codeFlights) == len(arr_schedule) == len(arr_timeDeparture) == len(arr_timeArrival) == len(arr_last_colum):
    print("\nInput Okay")
print("-------- Result---------------")
print("Remove parking:", arr_statictis[0][0])
print("Average taxi:", arr_statictis[0][3] / arr_statictis[0][2])
print("Waiting flights:", '0')
print("Objective_function value:", arr_statictis[0][1] / arr_statictis[0][2])

print("\nNumber of Crossing over:", count_CrossOver)
stop = timeit.default_timer()
print('Time: ', stop - start)  