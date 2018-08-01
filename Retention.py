#-*- coding: UTF-8 -*-
import sys
import csv
from Util import *
import statistics as stats
import re
import json


#get user_id from csv file
def load_csv(prefix):
    lines = []
    filename = "log/" + str(prefix) + ".csv"
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)
        header_len = len(next(reader)) #skip header
        for r in reader:
            if len(r) == header_len:
                lines.append(r[1])
    return lines

#get user_id from csv file
def load_csv2(prefix):
    lines = []
    filename = "log/" + str(prefix) + ".csv"
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)
        header_len = len(next(reader)) #skip header
        for r in reader:
            if len(r) == header_len:
                lines.append(r[2])
    return lines

#write user_id & user_num into txt file
def write_result(result):
    with open('user.txt', 'w') as f:
        f.write(str(result))
    f.close()

#next_day_retention_rate = retention_user_num/first_day_user_num
def next_day_retention(first):
    first_day_user = user_total_dict[first]['user_list']
    first_day_user_num = user_total_dict[first]['user_num']
    print("first day user number: " + str(first_day_user_num))

    next_day_user = user_total_dict[first+1]['user_list']
    next_day_user_num = user_total_dict[first+1]['user_num']
    print("next day user number: " + str(next_day_user_num))

    retention_user = first_day_user & next_day_user
    retention_user_num = len(retention_user)
    print("next day retention user number: " + str(retention_user_num))

    retention_rate = len(retention_user) / first_day_user_num
    print("next day retention rate: " + str(retention_rate))

#seven_day_retention_rate = the_7th_day_retention_user_num/first_day_user_num
def seven_day_retention(first):
    first_day_user = user_total_dict[first]['user_list']
    first_day_user_num = user_total_dict[first]['user_num']

    seven_day = first + 6
    seven_day_user = user_total_dict[seven_day]['user_list']
    seven_day_user_num = user_total_dict[seven_day]['user_num']
    print("the 7th day user number: " + str(seven_day_user_num))

    retention_user = first_day_user & seven_day_user
    retention_user_num = len(retention_user)
    print("retention user number at the 7th day :  " + str(retention_user_num))

    retention_rate = len(retention_user) / first_day_user_num
    print("the 7th day retention rate:  " + str(retention_rate))

#in_seven_day_retention_rate = within_seven_day_retention_user_num/first_day_user_num
def in_seven_day_retention(first):
    first_day_user = user_total_dict[first]['user_list']
    first_day_user_num = user_total_dict[first]['user_num']

    #get all the user_id in 6 days
    six_day_user = []
    for i in range(first+1, first+7):
        six_day_user.extend(list(user_total_dict[i]['user_list']))

    retention_user = first_day_user & set(six_day_user)
    retention_user_num = len(retention_user)
    print("retention user number within 7 days: " + str(retention_user_num))

    retention_rate = len(retention_user) / first_day_user_num
    print("within 7 days retention rate: " + str(retention_rate))


if __name__ == "__main__":

    user_total_dict = {}
    # get the user_id & user_num of each day
    for i in range(19,31):
        if i <= 23:
            lines = load_csv(i)
        else:
            lines = load_csv2(i)[:-1]
        user_list = set(lines)
        user_num = len(user_list)
        single_log_dict = {}
        single_log_dict['user_list'] = user_list
        single_log_dict['user_num'] = user_num
        user_total_dict[i]= single_log_dict
    # write_result(user_total_dict)

    for start in range(19, 25):
        print("first day： " + str(start))
        # 次日留存
        next_day_retention(start)

        # 七日留存
        seven_day_retention(start)

        # 七日内留存
        in_seven_day_retention(start)
        # break

