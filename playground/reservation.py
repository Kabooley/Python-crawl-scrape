import json
import requests
# from timetable import createtable
import os
import datetime
import time
from HLSgetter import HLSGetter

MULTI_FOR_MINUTE = int(60)
MULTI_FOR_HOUR = int(3600)
MULTI_FOR_DAY = int(86400)
FILE_PATH = os.getcwd()
RECORD_THRESHOLD = 20

def loop():
    make_reserves()
    print(reservelist)
    #202104041700

    while(1):
        for i in range(len(reservelist)):
            starttime_str = str(reservelist[i]['ft'])
            starttime_int = (int(starttime_str[6:8]) * MULTI_FOR_DAY) + (int(starttime_str[8:10]) * MULTI_FOR_HOUR)+ (int(starttime_str[10:12]) * MULTI_FOR_MINUTE)
            finishtime_str = str(reservelist[i]['to'])
            finishtime_int = (int(finishtime_str[6:8]) * MULTI_FOR_DAY) + (int(finishtime_str[8:10]) * MULTI_FOR_HOUR)+ (int(finishtime_str[10:12]) * MULTI_FOR_MINUTE)
            duration = finishtime_int - starttime_int

            t_now = datetime.datetime.now()
            now_in_seconds = int(t_now.day * MULTI_FOR_DAY) + int(t_now.hour * MULTI_FOR_HOUR) + int(t_now.minute * MULTI_FOR_MINUTE)
            print(f"now : {now_in_seconds}, abs = {t_now.day}/{t_now.hour}:{t_now.minute}") #Debug

            title = f"{t_now.month}_{t_now.day}_{t_now.year}_{t_now.hour}-{t_now.minute}"
            name = reservelist[i]['title']

            if (starttime_int - now_in_seconds) < RECORD_THRESHOLD and (starttime_int - now_in_seconds) >= 0:
                print(f"{name} is about to begin!")
                if reservelist[i]['flag'] == False:
                    HLSGetter.recode_hls((duration + (starttime_int - (now_in_seconds + t_now.second))), f"{FILE_PATH}/Output/{title}_{t_now.month}-{t_now.day}-{t_now.year}")
                    reservelist[i]['flag'] = True
            elif (starttime_int - now_in_seconds) < 0 and (-1 * (starttime_int - now_in_seconds)) < duration:
                print("streaming radio found")
                if reservelist[i]['flag'] == False:
                    HLSGetter.recode_hls((duration - (-1 * (starttime_int - now_in_seconds))), f"{FILE_PATH}/Output/{title}_{t_now.month}-{t_now.day}-{t_now.year}")
                    reservelist[i]['flag'] = True
            elif (starttime_int - now_in_seconds) < 0 and (-1 * (starttime_int - now_in_seconds)) >= duration:
                #print("paststream found")
                if reservelist[i]['flag'] == True:
                    reservelist[i]['flag'] = False

            print(f"Until {name} start : {starttime_int - (now_in_seconds + t_now.second)}")
            print(f"{name}'s starttime in sec : {starttime_int}seconds")      #Debug
            print(f"{name}'s finishtime in sec : {finishtime_int}seconds")    #Debug
            print(f"{name}'s duration in sec : {duration}seconds\n")          #Debug

        time.sleep(20) #Wait a 20 sec for next check


# 自前関数
# create_table()を取得する
def get_tables():
    

if __name__ == "__main__": 
    #Use main function only for debug or start loops.
    #Do NOT write any meaningful code here.
    loop()