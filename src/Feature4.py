# Block module
# Read log and write to block list if the IP access failed 3 times in 20 sec
#
import traceback

from utility import time_dif_in_sec, line_split


# Block check
# using block table to identify blocked IP
def block_check(block_list, log):
    try:
        block_table = block_list.block_table
        (address, log_time, Resource, code, use_bytes) = line_split(log)
        if address in block_table:
            block_info = block_table[address]
            last_log_time = block_info[0]
            sec_dif = time_dif_in_sec(last_log_time, log_time)
            if sec_dif > 60 * 5:
                del block_table[address]
            else:
                write_to_block_list(log)
        else:
            if code == '401':
                update_failed_log(block_list, address, log_time)
    except Exception as e:
        print(log, ", exception:", e)
    return block_list


#
# write log to blocked list
#
def write_to_block_list(log):
    try:
        with open('log_output/blocked.txt', 'a') as file:
            file.writelines(log)
    except IOError:
        traceback.print_exc()


#
# update failed access address to failed log table
# value store the failed time
def update_failed_log(block_list, address, log_time):
    try:
        block_table = block_list.block_table
        failed_log_table = block_list.failed_log_table
        if address in failed_log_table:
            failed_info = failed_log_table[address]
            last_log_time = failed_info[0]
            sec_dif = time_dif_in_sec(last_log_time, log_time)
            if sec_dif < 20:
                if len(failed_info) == 2:
                    del failed_log_table[address]
                    block_info = []
                    block_info.append(log_time)
                    block_table[address] = block_info
                else:
                    failed_log_table[address].append(log_time)
            else:
                count_log = len(failed_info)
                if count_log == 1:
                    del failed_log_table[address]
                else:
                    second_log_time = failed_info[1]
                    sec_dif = time_dif_in_sec(second_log_time, log_time)
                    if sec_dif > 20:
                        del failed_log_table[address]
                    else:
                        failed_log_table[address].pop()
                        failed_log_table[address].append(log_time)

        else:
            failed_info = []
            failed_info.append(log_time)
            failed_log_table[address] = failed_info
        return block_list
    except IOError:
        traceback.print_exc()
    except ValueError:
        traceback.print_exc()
