#-*- coding: UTF-8 -*-
import sys
import csv
from Util import *
import statistics as stats
import re

'''   
[(userid, (mode, query, answer)] 
'''

#date,userid,deviceid,mode,query,answer
def load_csv(prefix):
    lines = []
    filename = str(prefix)+".csv"
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)
        header_len = len(next(reader)) #skip header
        for r in reader:
            if len(r) == header_len:
                lines.append((r[1],(r[3],r[4],r[5])))
    return lines


#logid,date,userid,deviceid,mode,query,answer
def load_csv2(prefix):
    lines = []
    filename = str(prefix)+".csv"
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)
        header_len = len(next(reader)) #skip header
        for r in reader:
            if len(r) == header_len:
                lines.append((r[2],(r[4],r[5],r[6])))
    return lines

#get the user antiporn data
def load_ap_csv(prefix):
    lines = []
    filename = str(prefix) + "_ap.csv"
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)
        for r in reader:
            if len(r) == 5:
                if r == "---------server_ap---------":
                    break
                lines.append(((r[0],r[1]),1))
    return lines

#write each day's stats into csv file
def write_result(prefix,result):
    filename = str(prefix)+"_stats.csv"
    with open(filename, 'w', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in result.items():
            writer.writerow([key, value])
    csv_file.close()


if __name__ == "__main__":

    for i in range(19,27):
        if i <= 23:
            # todo:load csv
            lines = load_csv(i)
        else:
            lines = load_csv2(i)

        # todo: get user_num
        '''(userid, num)'''
        user_num = aggregate(lines,len)

        #todo:(max,min,low,high,std,median,invalid_mean)
        result_dict = analyze_stats(dict(user_num))
        result_dict['user number'] = len(user_num)

        # todo: select valid values
        low = result_dict['99%_confidence_interval_min']  #99%置信区间最小值
        high = result_dict['99%_confidence_interval_max'] #99%置信区间最大值
        valid_value =  [(k,v) for (k,v) in user_num if (v <= high and v >= low)]
        result_dict['user_num_within_99%CI'] = len(valid_value) #99%置信区间内的用户数量
        # print("valid user num :" + str(len(valid_value)))
        valid_mean = stats.mean(dict(valid_value).values())
        result_dict['avg_query_num_within_99%CI'] = valid_mean #99%置信区间内的平均值


        # todo: get quit、user_query_num per round
        pattern = r"退出"
        user_quit = select(lines, lambda t: re.search(pattern,t[1][1]))
        user_quit_num = aggregate(user_quit,len)
        avg_round = stats.mean(list(dict(user_quit_num).values()))
        result_dict['avg_round'] = avg_round #用户平均对话轮数
        # print("用户平均对话轮数: " + str(user_quit_avg))

        sel = select(product(user_quit_num,user_num), lambda t: t[0][0] == t[1][0])
        user_query_per_round = project(sel,lambda t:(t[0][0],t[1][1]/t[0][1]))
        avg_query_per_round = stats.mean(list(dict(user_query_per_round).values()))
        result_dict['avg_query_per_round'] = avg_query_per_round #用户平均每轮query量
        # print("用户平均每轮query量: " + str(user_q_r_avg))

        # todo: user antiporn
        ap_lines = load_ap_csv(i)
        user_ap = aggregate(ap_lines, sum)
        result_dict['user_with_porn'] = len(user_ap) #有黄反的用户数量

        mode_ap = aggregate(project(user_ap, lambda t: (t[0][1], 1)), sum)
        result_dict['user_w/_porn_with_mode'] = mode_ap #不同模式黄反用户数量

        # todo: kid vs default
        mode = project(lines, lambda t: (t[1][0],1))
        # [(userid, (mode, query, answer)]
        mode_sum = aggregate(mode, sum)
        # print("mode_su" + str(mode_sum))
        tmp = aggregate(project(lines, lambda t: ((t[1][0], t[0]),1)), len)
        # print(tmp)
        mode_num = aggregate(project(tmp,lambda t:(t[0][0], 1)),len)

        # print(mode_num)
        # print(ts)
        result_dict['query_with_mode'] = mode_sum #不同模式query数量
        result_dict['user_num_with_mode'] = mode_num #不同模式用户数量

        # todo: write
        print(result_dict)
        write_result(i, result_dict)


        # todo: get sentimental analysis
        # need NLP

        # break
