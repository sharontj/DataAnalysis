import statistics as stats
import numpy as np, scipy.stats as st

def union(R, S):
    return R + S


def difference(R, S):
    return [t for t in R if t not in S]


def intersect(R, S):
    return [t for t in R if t in S]


def project(R, p):
    return [p(t) for t in R]


def select(R, s):
    return [t for t in R if s(t)]


def product(R, S):
    return [(t, u) for t in R for u in S]


def aggregate(R, f):
    keys = {r[0] for r in R}
    return [(key, f([v for (k, v) in R if k == key])) for key in keys]


def map(f, R):
    return [t for (k, v) in R for t in f(k, v)]


def reduce(f, R):
    keys = {k for (k, v) in R}
    return [f(k1, [v for (k2, v) in R if k1 == k2]) for k1 in keys]


def analyze_stats(info):
    value_list = list(info.values())
    max_value = max(value_list)
    min_value = min(value_list)
    mean = stats.mean(value_list)
    std = stats.stdev(value_list)
    median_value = stats.median(value_list)
    low, high = confidence_interval(value_list)
    result_dict = dict()
    result_dict['single_user_max_query_num'] = max_value #单个用户最大query值
    result_dict['single_user_min_query_num'] = min_value #单个用户最小query值
    result_dict['query_num_standard_deviation'] = std #query标准差
    result_dict['query_num_mean'] = mean #query平均值
    result_dict['query_num_median'] = median_value #query中位数
    result_dict['99%_confidence_interval_min'] = low
    result_dict['99%_confidence_interval_max'] = high
    return result_dict


def normalize(value, low, high):
    return float((value-low)/(high-low))

def confidence_interval(value_list):
    low, high = st.t.interval(0.995, len(value_list) - 1, loc=np.mean(value_list), scale=st.sem(value_list))
    return low, high