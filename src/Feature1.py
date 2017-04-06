#
# List the top 10 most active host/IP addresses that have accessed the site.
# Part 1: address_count() calculate each address visit frequency
# Part 2: top10_address() get the top 10 address

#  #
import operator
import traceback

from utility import write_to_file


def address_count(address_table, address):
    if address not in address_table:
        address_table[address] = 1
    else:
        address_table[address] += 1
    return address_table


#
#
#   get addresses,sorted in the decending order
def top10_address(address_table):
    try:
        for item in address_table.most_common(10):
            address = item[0]
            visit_count = item[1]
            line = address + "," + repr(visit_count)
            write_to_file('log_output/hosts.txt', line)
    except ValueError:
        traceback.print_exc()


