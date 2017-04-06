import codecs
import traceback
from collections import *
from collections import defaultdict
from io import BlockingIOError

from Feature1 import address_count, top10_address
from Feature2 import resource_count, top10_resource
from Feature3 import visit_time_list, top10_busiest
from Feature4 import block_check
from utility import line_split
#from target_busiest_month import target_busiest_month, target_time,print_table


class Block:
    block_table = defaultdict()
    failed_log_table = defaultdict()


def process_log(filename):
    try:
        address_table = Counter()
        resource_table = Counter()
        resource_time_table = Counter()
        address_time_table = Counter()
        log_time_list = deque([])
        block_list = Block
        with codecs.open(filename, encoding="ISO-8859-1") as file:
            try:
                for log in file:
                    try:
                        (address, log_time, resource, code, visit_bytes) = line_split(log)
                        address_table = address_count(address_table, address)
                        resource_table = resource_count(resource_table, resource, visit_bytes)
                        log_time_list=visit_time_list(log_time_list, log_time)
                        block_check(block_list, log)
                        #*********this is for the additional feature, you may comment it when testing feature 1 through 4***
                        #(resource_time_table , address_time_table)= target_time ( address , resource , log_time , resource_time_table , address_time_table )
                    except BlockingIOError:
                        traceback.print_exc()
            except BlockingIOError:
                traceback.print_exc()
        # Read file finished, handle data if needed
        print("Read file finished")
        # Feature1
        top10_address_table = top10_address(address_table)
        # Feature2
        top10_resource_table = top10_resource(resource_table)
        # Feature3
        top10_busiest(log_time_list, 3600)# the busiest 60 minutes
        # Feature4
        # No needed here, already print while read file
        print("Congratulations, feature 1-4 finished!")

        print("Bonus Features.....")
        #address_busy_table = target_busiest_month ( address_time_table, top10_address_table)
        #print_table(address_busy_table)
        #resource_busy_table = target_busiest_month ( resource_time_table, top10_resource_table)
        #print_table(resource_busy_table )
    except IOError:
        traceback.print_exc()
    except ValueError:
        traceback.print_exc()