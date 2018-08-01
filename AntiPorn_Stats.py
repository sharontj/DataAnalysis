#-*- coding: UTF-8 -*-
import json
import sys
import time
import csv
import requests
import codecs

#the antiporn api takes at most 10 queries once, so load the csv file as chunks with size 5
def load_csv(prefix, chunk_size = 5):
    chunk_list = []
    count = 0
    chunk = []
    filename = str(prefix)+".csv"
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for r in reader:
            if len(r) != 6:
                continue
            count += 1
            chunk.append(r)
            if count % chunk_size == 0:
                chunk_list.append(chunk)
                chunk = []
    print(count)
    return chunk_list


def load_csv2(prefix, chunk_size = 5):
    chunk_list = []
    count = 0
    chunk = []
    filename = str(prefix)+".csv"
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for r in reader:
            if len(r) != 7:
                continue
            count += 1
            chunk.append(r)
            if count % chunk_size == 0:
                chunk_list.append(chunk)
                chunk = []
    print(count)
    return chunk_list

def CallAntiPorn(body):
    url = #AntiPorn Api
    tmpdata = '''
     {
        "logid":"1234",
        "queries":'''+body+'''
        }'''

    # print(data)
    data = tmpdata.encode('utf-8')
    response = requests.post(url, data=data)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response.json()
    else:
        # print(response.status_code)
        return


def get_result(chunk_list):
    user_ap_num = 0
    user_ap = []
    both_ap_num = 0
    both_ap = []
    server_ap_num = 0
    server_ap = []
    tick = 0
    for chunk in chunk_list:
        tick += 1
        query_answer = []
        for s in chunk:
            query_answer.append(s[4])
            query_answer.append(s[5])
        body = str(query_answer).replace("'", "\"")
        result = CallAntiPorn(body)
        # print(result)
        try:
            print(tick)
            for i in range(0, 10, 2):
                realindex = int(i / 2)

                if result['data'][i]['result'] == 0 and result['data'][i + 1]['result'] > 0:
                    server_ap_num += 1
                    match = result['data'][i + 1]['details'][u'matched_terms']
                    server_ap.append(chunk[realindex][1] + "," + chunk[realindex][3] + "," + \
                                 chunk[realindex][4] + "," + chunk[realindex][5] + "," + str(match) + "\n")
                elif result['data'][i]['result'] > 0 and result['data'][i + 1]['result'] == 0:
                    user_ap_num += 1
                    match = result['data'][i]['details'][u'matched_terms']
                    user_ap.append(chunk[realindex][1] + "," + chunk[realindex][3] + "," + \
                                   chunk[realindex][4] + "," + chunk[realindex][5] + "," + str(match) + "\n")
                elif result['data'][i]['result'] > 0 and result['data'][i + 1]['result'] > 0:
                    both_ap_num += 1
                    match = result['data'][i]['details'][u'matched_terms'] + "->" \
                            + result['data'][i + 1]['details'][u'matched_terms']
                    both_ap.append(chunk[realindex][1] + "," + chunk[realindex][3] + "," + \
                                   chunk[realindex][4] + "," + chunk[realindex][5] + "," + str(match) + "\n")

        except (IOError, ValueError, TypeError):
            print("No valid integer! Please try again ..." + str(tick))
        time.sleep(0.5)
        # if tick == 5:
        #     break

    print("user_ap: " + str(user_ap_num) + "\n" + "server_ap: " + str(server_ap_num) + "\nboth_ap: " + str(both_ap_num))
    return server_ap,user_ap,both_ap


def get_result2(chunk_list):
    user_ap_num = 0
    user_ap = []
    both_ap_num = 0
    both_ap = []
    server_ap_num = 0
    server_ap = []
    tick = 0
    for chunk in chunk_list:
        tick += 1
        query_answer = []
        for s in chunk:
            query_answer.append(s[5])
            query_answer.append(s[6])
        body = str(query_answer).replace("'", "\"")
        result = CallAntiPorn(body)
        try:
            print(tick)
            for i in range(0, 10, 2):
                realindex = int(i / 2)

                if result['data'][i]['result'] == 0 and result['data'][i + 1]['result'] > 0:
                    server_ap_num += 1
                    match = result['data'][i + 1]['details'][u'matched_terms']
                    server_ap.append(chunk[realindex][2] + "," + chunk[realindex][4] + "," + \
                                 chunk[realindex][5] + "," + chunk[realindex][6] + "," + str(match) + "\n")
                elif result['data'][i]['result'] > 0 and result['data'][i + 1]['result'] == 0:
                    user_ap_num += 1
                    match = result['data'][i]['details'][u'matched_terms']
                    user_ap.append(chunk[realindex][2] + "," + chunk[realindex][4] + "," + \
                                   chunk[realindex][5] + "," + chunk[realindex][6] + "," + str(match) + "\n")
                elif result['data'][i]['result'] > 0 and result['data'][i + 1]['result'] > 0:
                    both_ap_num += 1
                    match = result['data'][i]['details'][u'matched_terms'] + "->" \
                            + result['data'][i + 1]['details'][u'matched_terms']
                    both_ap.append(chunk[realindex][2] + "," + chunk[realindex][4] + "," + \
                                   chunk[realindex][5] + "," + chunk[realindex][6] + "," + str(match) + "\n")

        except (IOError, ValueError, TypeError):
            print("No valid integer! Please try again ..." + str(tick))
        time.sleep(0.5)  #sleep 500ms after calling api
        # if tick == 10:
        #     break
    print("server_ap: " + str(server_ap_num) + "\nuser_ap: " + str(user_ap_num)  + "\nboth_ap: " + str(both_ap_num))
    return server_ap,user_ap,both_ap


def write_result(prefix,server_ap,user_ap,both_ap):
    filename = str(prefix)+"_ap.csv"
    f = codecs.open(filename, 'w', encoding='utf-8')  # 必须事先知道文件的编码格式，这里文件编码是使用的utf-8
    f.write("---------server_ap---------"+"\n")
    for server in server_ap:
        f.write(server)
    f.write("---------user_ap---------" + "\n")
    for user in user_ap:
        f.write(user)
    f.write("---------both_ap---------" + "\n")
    for both in both_ap:
        f.write(both)
    f.write("---------stats---------" + "\n")

    f.close()
    # break


if __name__ == "__main__":
    chunk_size = 5
#     chunk_list = load_csv(23, chunk_size)
    
    #read a series of files 
    for prefix in range(24,27):
        chunk_list = load_csv2(prefix,chunk_size)
        # print(chunk_list)
        # test(1)
        server_ap, user_ap, both_ap = get_result2(chunk_list)
        write_result(prefix, server_ap,user_ap,both_ap)

        print(str(server_ap) + "\n")
        print(str(user_ap) + "\n")
        print(str(both_ap) + "\n")
        # break

    


