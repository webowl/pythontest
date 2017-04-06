# top_10_busiest_60m_slots() calculates top 10 busiest 60 minutes
# A sliding bar is used to calculate the moving sum in given time window
# The visiting records are pushed into sliding_bar, a deque.
# The corresponding visiting count equals to the length of sliding_bar.
# (time, visiting count) is saved in heapq for the top 10 records
import time
import datetime
import traceback
import heapq
from _heapq import heappush, heappop
from collections import deque
from utility import write_to_file


def visit_time_list(log_time_list, log_time):
    try:
        fmt = '%d/%b/%Y:%H:%M:%S'
        cur_time = int(time.mktime(datetime.datetime.strptime(log_time, fmt).timetuple()))  #####
        log_time_list.append(cur_time)
        return log_time_list
    except :
        return None


def top_10_busiest_60m_slots(log_time_list , time_window ):
    table_len = len(log_time_list)
    visited_time_count = []  # save counted results

    sliding_bar = deque()

    # first sliding bar 3600 seconds
    first_point = log_time_list[0]
    dif = 0
    i = 0
    while dif <= time_window:
        sliding_bar.append(log_time_list[i])
        i += 1
        if i <= table_len - 1:
            dif = log_time_list[i] - first_point
        else:
            break

    bar_length = i
    if table_len < i:
        end_point_location = i
    else:
        end_point_location = i - 1
    heappush(visited_time_count, (i, first_point))

    # next time counts
    first_point_location = 0
    left_end_flag = 0
    if table_len != bar_length:
        right_end_flag = 0
    else:
        right_end_flag = 1
    while first_point_location < end_point_location:  # should be: len_remained >= 0
        # pop left
        while sliding_bar[0] == first_point:
            sliding_bar.popleft()
            bar_length -= 1
            first_point_location += 1
            if bar_length == 0:
                left_end_flag = 1
                break
        if left_end_flag == 1:  # sliding bar is empty
            return visited_time_count
        first_point = sliding_bar[0]

        # right entry here
        next_point = log_time_list[end_point_location]
        delta_time = next_point - first_point

        while delta_time <= time_window and right_end_flag != 1:
            next_point = end_point = log_time_list[end_point_location]
            while next_point == end_point:
                sliding_bar.append(next_point)
                bar_length += 1
                if first_point_location == end_point_location:
                    return visited_time_count
                if end_point_location == table_len - 1:
                    # reach right end of the table
                    right_end_flag = 1
                    break
                end_point_location += 1
                next_point = log_time_list[end_point_location]
            delta_time = next_point - first_point
        if len(visited_time_count) < 10:
            heappush(visited_time_count, (bar_length, first_point))
        elif visited_time_count[0][0]< (end_point_location-first_point_location):
            if visited_time_count[0][0] < bar_length:
                heappop(visited_time_count)
                heappush(visited_time_count, (bar_length, first_point))
        else:
            return visited_time_count


def top10_busiest(log_time_list,time_window):
    try:
        fmt = '%d/%b/%Y:%H:%M:%S'
        top10_busy_time = top_10_busiest_60m_slots(log_time_list,time_window)
        top10_busy_time = heapq.nlargest(10, top10_busy_time, key=lambda x: x[0])
        i = 0
        table_len = len(top10_busy_time)
        while i < table_len:
            item = top10_busy_time[i]
            format_time = datetime.datetime.fromtimestamp(item[1])
            counted_qty = item[0]
            line = format_time.strftime(fmt) + " -0400," + repr(counted_qty)
            write_to_file('log_output/hours.txt', line)
            i += 1
    except ValueError:
        traceback.print_exc()