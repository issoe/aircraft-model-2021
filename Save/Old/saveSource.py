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

    # if order_r == 1:
    #     arr_res1 = arr_res
    # if order_r == 2:
    #     arr_res2 = arr_res
    # elif order_r == 3:
    #     arr_res3 = arr_res
    # elif order_r == 4:
    #     arr_res4 = arr_res
    # elif order_r == 5:
    #     arr_res5 = arr_res
    # elif order_r == 6:
    #     arr_res6 = arr_res
    # elif order_r == 7:
    #     arr_res7 = arr_res
    # elif order_r == 8:
    #     arr_res8 = arr_res
    # elif order_r == 9:
    #     arr_res9 = arr_res
    # elif order_r == 10:
    #     arr_res10 = arr_res
    # elif order_r == 11:
    #     arr_res11 = arr_res
    # elif order_r == 12:
    #     arr_res12 = arr_res
    # elif order_r == 13:
    #     arr_res13 = arr_res
    # elif order_r == 14:
    #     arr_res14 = arr_res
    # elif order_r == 15:
    #     arr_res15 = arr_res
    # elif order_r == 16:
    #     arr_res16 = arr_res
    # elif order_r == 17:
    #     arr_res17 = arr_res
    # elif order_r == 18:
    #     arr_res18 = arr_res
    # elif order_r == 19:
    #     arr_res19 = arr_res
    # elif order_r == 20:
    #     arr_res20 = arr_res
# Sort
# try:
#     arr_res1.sort(key = sub.takeThree)
#     arr_res2.sort(key = sub.takeThree)
#     arr_res3.sort(key = sub.takeThree)
#     arr_res4.sort(key = sub.takeThree)
#     arr_res5.sort(key = sub.takeThree)
#     arr_res6.sort(key = sub.takeThree)
#     arr_res7.sort(key = sub.takeThree)
#     arr_res8.sort(key = sub.takeThree)
#     arr_res9.sort(key = sub.takeThree)
#     arr_res10.sort(key = sub.takeThree)
#     arr_res11.sort(key = sub.takeThree)
#     arr_res12.sort(key = sub.takeThree)
#     arr_res13.sort(key = sub.takeThree)
#     arr_res14.sort(key = sub.takeThree)
#     arr_res15.sort(key = sub.takeThree)
#     arr_res16.sort(key = sub.takeThree)
#     arr_res17.sort(key = sub.takeThree)
#     arr_res18.sort(key = sub.takeThree)
#     arr_res19.sort(key = sub.takeThree)
#     arr_res20.sort(key = sub.takeThree)

# except:
#     print("Fault sort at Crossing over ")




def glo_Objective_Function(var_idx, arr_1, ele1, ele2, stat):
    R1 = stat[0] / stat[2]

    R2 = stat[3] / stat[2]

    R3 = 0


    tempOne = arr_1[var_idx][1] 
    tempTwo = arr_1[var_idx][2]
    arr_1[var_idx][1] = ele1
    arr_1[var_idx][2] = ele2

    valu, _, _, _ = Objective_Function(arr_1[var_idx][5], 0)
    valu += stat[1] # minus what????

    arr_1[var_idx][1] = tempOne
    arr_1[var_idx][2] = tempTwo
    return valu / stat[2]