# Import 
# from Users.khanhquang.Downloads.AirCraft_MODEL.Again.cur import Objective_Function
import pandas as pd
import re


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


# FUNC: ARR_CODEFLIGHTS ARRAY ~ colum index = 3
def create_arr_codeflights(df, def_arr_codeFlights, def_numberOfFlights):
    for i in range(0, def_numberOfFlights):
        string = df[3][i][0:2] # always 2 first letters
        test_string = df[3][i] # temp string 
        res = [int(i) for i in test_string.split() if i.isdigit()] # get all numbers from the index 3 

        if len(res) == 0:
            def_arr_codeFlights.append([test_string, str("-")])
        elif len(res) == 1:
            def_arr_codeFlights.append([string+str(res[0]), str("-")])
        elif len(res) == 2:
            def_arr_codeFlights.append([string+str(res[0]), string+str(res[1])])
        else:
            print("Fault at decode def_arr_codeFlights")


# FUNC: ARR_SCHEDULE ARRAY ##########################################################
def create_arr_schedule(df, def_arr_schedule, def_numberOfFlights):
    for x in range(0, def_numberOfFlights):
        temp = df[4][x]
        if len(temp) != 7 and len(temp) != 11:
            print("Fault at decode arr_arr_schedule at index:", x+1, "with",  temp)

        if len(temp) == 7:
            if temp[0:3] == "SGN":
                def_arr_schedule.append('3')
            else:
                def_arr_schedule.append('4')
        else:
            if temp[4:7] == "SGN":
                def_arr_schedule.append('1')
            else:
                def_arr_schedule.append('2')


# FUNC: ARR_TIMEDEPARTURE ARRAY #####################################################
def create_arr_timeDeparture(df, def_arr_timeDeparture, def_numberOfFlights):
    # Add time without check the next day 
    for x in range(0, def_numberOfFlights):
        # next_day(str(df[6][x]))
        time = re.findall('[0-9]+', str(df[5][x]))
        try:
            time[0]
        except:
            def_arr_timeDeparture.append(-1)
        else:
            def_arr_timeDeparture.append(decode_time(time[0]))

    # Check again the next day 
    for search in range(0, len(def_arr_timeDeparture)):
        if next_day(str(df[5][search])) == True:
            def_arr_timeDeparture[search] += 1440


# FUNC: ARR_TIMEARRIVAL ARRAY #######################################################
def create_arr_timeArrival(df, def_arr_timeArrival, def_numberOfFlights):
    # Add time without check the next day 
    for x in range(0, def_numberOfFlights):
        time = re.findall('[0-9]+', str(df[6][x]))
        try:
            time[0]
        except:
            def_arr_timeArrival.append(-1)
        else:
             def_arr_timeArrival.append(decode_time(time[0]))
    
    # Check again the next day 
    for search in range(0, len(def_arr_timeArrival)):
        if next_day(str(df[5][search])) == True:
            def_arr_timeArrival[search] += 1440


# FUNC: THE LAST COLUM INTO ARR_LAST_COLUM
def create_arr_lastColum(df, def_arr_last_colum, def_numberOfFlights):
    # FUNC: THE LAST_COLUM ARRAY ########################################################
    for last in range(0, def_numberOfFlights):
        def_arr_last_colum.append(str(df[7][last]))   #Ép kiểu thành string luôn cho nhanh


####################################################################################################################################
#################################### ------ TAXI_ARRAY --> df_taxi ------ ##########################################################
df_taxi = pd.read_csv('taxi.csv', sep=';', header=None)
# print(df_taxi)

# Find the average and maximum value taxi for each aircraft ----> FOR ONLY OBJECTIVE FUNCTION 
def findTaxi(position):
    for searchTaxi in range(0, 104):
        if df_taxi[0][searchTaxi] == position:
            if str(df_taxi[1][searchTaxi]) != "nan":
                return float(df_taxi[1][searchTaxi]), float(df_taxi[2][searchTaxi])
            else:
                print("Position wasnot exist in finding TAXI at", position)
                return -1, -1


#######################################################################################################################
############################## ------ LOUNGE_ARRAY --> df_lounge  ------ ##############################################
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


def create_initial_level(arr_1, len_1, arr_2, len_2, arr_3, len_3, arr_4, len_4):
    for i in range(0, len_1):
        arr_1.append([-5,"-","-"])
    for i in range(0, len_2):
        arr_2.append([-5,"-","-"])
    for i in range(0, len_3):
        arr_3.append([-5,"-","-"])
    for i in range(0, len_4):
        arr_4.append([-5,"-","-"])

################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################ 
################################################################################################################################
                

